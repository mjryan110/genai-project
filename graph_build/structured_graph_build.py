import os
import re
import pandas as pd
from typing import List, Dict, Any, Callable, Iterator
from neo4j import GraphDatabase

def batch_parameters(lst: List[Any], batch_size: int) -> Iterator[List[Any]]:
    for i in range(0, len(lst), batch_size):
        yield lst[i:i + batch_size]

def filter_null_params(record: Dict) -> Dict:
    return {
        k: v for k, v in record.items()
        if v is not None and not (isinstance(v, float) and pd.isna(v))
    }

def has_all_required_keys(record: Dict, required_keys: List[str]) -> bool:
    return all(
        key in record and record[key] is not None and not (isinstance(record[key], float) and pd.isna(record[key]))
        for key in required_keys
    )

def parse_sg_string(s: str) -> List[str]:
    if not isinstance(s, str):
        return []
    s = s.strip("[]")
    return [sg.strip() for sg in s.split() if sg.strip()]

REQUIRED_KEYS = {
    "_create_server": ["Servers", "State", "Region", "Availability_Zone", "Root_Device_Name", "Root_Volume_ID",
                       "Tag_aws_autoscaling_groupName", "Tag_aws_ec2launchtemplate_id", "Tag_aws_ec2launchtemplate_version"],
    "_create_product": ["Product"],
    "_create_product_owner": ["Product_Owner"],
    "_create_supporting_product_owner": ["Supporting_Product_Owner"],
    "_create_product_team": ["Tag_product_team"],
    "_create_vpc": ["VPC_ID"],
    "_create_security_groups": ["SecurityGroupsParsed"],
    "_rel_server_runs_product": ["Servers", "Product"],
    "_rel_server_owned_by_owner": ["Servers", "Product_Owner"],
    "_rel_product_supported_by_owner": ["Product", "Supporting_Product_Owner"],
    "_rel_product_belongs_to_team": ["Product", "Tag_product_team"],
    "_rel_server_part_of_vpc": ["Servers", "VPC_ID"],
    "_rel_server_uses_sg": ["Servers", "SecurityGroupsParsed"]
}

class Neo4jWriter:
    def __init__(self, driver: GraphDatabase.driver, df: pd.DataFrame, batch_size: int = 1000):
        self.df = df
        self.batch_size = batch_size
        self.driver = driver

        print(f"[INFO] Initializing Neo4jWriter with {len(df)} rows.")
        print(f"[DEBUG] Original columns: {list(df.columns)}")

        self.df.columns = [self.normalize_column_name(col) for col in self.df.columns]
        print(f"[DEBUG] Normalized columns: {list(self.df.columns)}")

        self._parse_security_groups()

    def close(self):
        self.driver.close()

    @staticmethod
    def normalize_column_name(name: str) -> str:
        name = name.strip()
        name = re.sub(r"[^\w]", "_", name)
        return re.sub(r"__+", "_", name)

    def _parse_security_groups(self):
        sg_col = "Security_Groups"
        if sg_col in self.df.columns:
            print(f"[INFO] Parsing Security Groups from column: {sg_col}")
            self.df["SecurityGroupsParsed"] = self.df[sg_col].apply(parse_sg_string)
            print(f"[DEBUG] Sample SGs: {self.df['SecurityGroupsParsed'].head().tolist()}")
        else:
            print("[WARN] No Security_Groups column found for parsing.")

    def create_indexes(self):
        print("[INFO] Creating Neo4j indexes...")
        constraints = [
            "CREATE CONSTRAINT IF NOT EXISTS FOR (s:Server) REQUIRE (s.name) IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (p:Product) REQUIRE (p.name) IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (o:ProductOwner) REQUIRE (o.name) IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (t:ProductTeam) REQUIRE (t.name) IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (sg:SecurityGroup) REQUIRE (sg.id) IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (v:VPC) REQUIRE (v.id) IS UNIQUE"
        ]
        with self.driver.session(database='neo4j') as session:
            for constraint in constraints:
                print(f"[DEBUG] Executing constraint: {constraint}")
                session.run(constraint)

    def write_all_structured_data(self):
        print("[INFO] Starting to write all structured data.")
        records = self.df.to_dict(orient="records")
        print(f"[DEBUG] Total records to process: {len(records)}")
        vpc_records = [r for r in records if r.get("VPC_ID") not in (None, "", "null") and not pd.isna(r.get("VPC_ID"))]
        print(f"[DEBUG] Records with valid VPC_ID: {len(vpc_records)}")

        self.write_batches_serial(records, self._create_server)
        self.write_batches_serial(records, self._create_product)
        self.write_batches_serial(records, self._create_product_owner)
        self.write_batches_serial(records, self._create_supporting_product_owner)
        self.write_batches_serial(records, self._create_product_team)
        self.write_batches_serial(vpc_records, self._create_vpc)
        self.write_batches_serial(records, self._create_security_groups)

        self.write_batches_serial(records, self._rel_server_runs_product)
        self.write_batches_serial(records, self._rel_server_owned_by_owner)
        self.write_batches_serial(records, self._rel_product_supported_by_owner)
        self.write_batches_serial(records, self._rel_product_belongs_to_team)
        self.write_batches_serial(records, self._rel_server_part_of_vpc)
        self.write_batches_serial(records, self._rel_server_uses_sg)

    def write_batches_serial(self, data: List[Dict], tx_function: Callable[[Any, Dict[str, List[Dict]]], None]):
        func_name = tx_function.__name__
        required = REQUIRED_KEYS.get(func_name, [])
        print(f"\n[INFO] Writing batches for: {func_name}")
        print(f"[DEBUG] Required keys: {required}")
        total_written, total_skipped = 0, 0

        for batch_index, batch in enumerate(batch_parameters(data, self.batch_size), start=1):
            filtered = []
            for r in batch:
                if has_all_required_keys(r, required):
                    filtered.append(self.ensure_keys_exist(filter_null_params(r), required))
                else:
                    missing = [k for k in required if k not in r or pd.isna(r[k])]
                    print(f"[SKIP] Missing keys in record: {missing}")
                    total_skipped += 1

            print(f"[DEBUG] Batch {batch_index}: {len(filtered)} valid, {total_skipped} skipped so far")
            if not filtered:
                print(f"[WARN] Skipping batch {batch_index} for {func_name}, no valid records.")
                continue

            with self.driver.session(database='neo4j') as session:
                try:
                    session.execute_write(tx_function, {'params': filtered})
                    print(f"[INFO] Successfully wrote {len(filtered)} records in batch {batch_index} for {func_name}")
                    total_written += len(filtered)
                except Exception as e:
                    print(f"[ERROR] Error writing batch {batch_index} for {func_name}: {e}")

        print(f"[INFO] Finished writing {func_name}. Total written: {total_written}, total skipped: {total_skipped}")

    def ensure_keys_exist(self, record: Dict, required_keys: List[str]) -> Dict:
        return {k: record.get(k) for k in required_keys} | record


    # === Node Creators ===

    @staticmethod
    def _create_server(tx, params):
        tx.run("""
        UNWIND $params AS param
        MERGE (s:Server {name: param.Servers})
        SET s.state = param.State,
            s.region = param.Region,
            s.az = param.AvailabilityZone,
            s.root_device = param.RootDeviceName,
            s.root_volume = param.RootVolumeID,
            s.autoscaling_group = param.Tag_aws_autoscaling_groupName,
            s.launch_template_id = param.Tag_aws_ec2launchtemplate_id,
            s.launch_template_version = param.Tag_aws_ec2launchtemplate_version
        """, parameters=params)

    @staticmethod
    def _create_product(tx, params):
        tx.run("UNWIND $params AS param MERGE (:Product {name: param.Product})", parameters=params)

    @staticmethod
    def _create_product_owner(tx, params):
        tx.run("UNWIND $params AS param MERGE (:ProductOwner {name: param.Product_Owner})", parameters=params)

    @staticmethod
    def _create_supporting_product_owner(tx, params):
        tx.run("UNWIND $params AS param MERGE (:ProductOwner {name: param.Supporting_Product_Owner})", parameters=params)

    @staticmethod
    def _create_product_team(tx, params):
        tx.run("UNWIND $params AS param MERGE (:ProductTeam {name: param.Tag_product_team})", parameters=params)

    @staticmethod
    def _create_vpc(tx, params):
        tx.run("UNWIND $params AS param MERGE (:VPC {id: param.VPC_ID})", parameters=params)

    @staticmethod
    def _create_security_groups(tx, params):
        tx.run("""
        UNWIND $params AS param
        UNWIND param.SecurityGroupsParsed AS sgid
        WITH trim(sgid) AS sgid
        WHERE sgid <> ''
        MERGE (:SecurityGroup {id: sgid})
        """, parameters=params)

    # === Relationship Creators ===

    @staticmethod
    def _rel_server_runs_product(tx, params):
        tx.run("""
        UNWIND $params AS param
        MATCH (s:Server {name: param.Servers}), (p:Product {name: param.Product})
        MERGE (s)-[:RUNS]->(p)
        """, parameters=params)

    @staticmethod
    def _rel_server_owned_by_owner(tx, params):
        tx.run("""
        UNWIND $params AS param
        MATCH (s:Server {name: param.Servers}), (o:ProductOwner {name: param.Product_Owner})
        MERGE (s)-[:OWNED_BY]->(o)
        """, parameters=params)

    @staticmethod
    def _rel_product_supported_by_owner(tx, params):
        tx.run("""
        UNWIND $params AS param
        MATCH (p:Product {name: param.Product}), (o:ProductOwner {name: param.Supporting_Product_Owner})
        MERGE (p)-[:SUPPORTED_BY]->(o)
        """, parameters=params)

    @staticmethod
    def _rel_product_belongs_to_team(tx, params):
        tx.run("""
        UNWIND $params AS param
        MATCH (p:Product {name: param.Product}), (t:ProductTeam {name: param.Tag_product_team})
        MERGE (p)-[:BELONGS_TO_TEAM]->(t)
        """, parameters=params)

    @staticmethod
    def _rel_server_part_of_vpc(tx, params):
        tx.run("""
        UNWIND $params AS param
        MATCH (s:Server {name: param.Servers}), (v:VPC {id: param.VPC_ID})
        MERGE (s)-[:PART_OF_VPC]->(v)
        """, parameters=params)

    @staticmethod
    def _rel_server_uses_sg(tx, params):
        tx.run("""
        UNWIND $params AS param
        UNWIND param.SecurityGroupsParsed AS sgid
        MATCH (s:Server {name: param.Servers}), (sg:SecurityGroup {id: sgid})
        MERGE (s)-[:USES_SECURITY_GROUP]->(sg)
        """, parameters=params)
