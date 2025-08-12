import json
from typing import Optional, Dict, Any
from neo4j import Driver

from neo4j_graphrag.schema import get_schema
from neo4j_graphrag.indexes import retrieve_fulltext_index_info

from ..llm import BaseLLMAdapter
from ..pydantictypes import RoutingDecision


class RetrieverRouter:
    def __init__(
        self,
        llm: BaseLLMAdapter,
        driver: Driver,
        database: str,
        fulltext_index_config: Optional[Dict[str, Any]] = None
    ):
        self.llm = llm
        self.driver = driver
        self.database = database

        self.neo4j_schema = get_schema(driver, is_enhanced=True, database=self.database)
        self.vector_index_infos = self._list_vector_indexes()

        self.fulltext_index_info = (
            retrieve_fulltext_index_info(
                driver,
                index_name=fulltext_index_config["index_name"],
                label_or_type=fulltext_index_config["label_or_type"],
                text_properties=fulltext_index_config.get("text_properties", [])
            ) if fulltext_index_config else None
        )

    def decide(self, question: str) -> RoutingDecision:
        prompt: str = self._build_prompt(question)
        try:
            response = self.llm.ask(prompt)

            cleaned = (
                response.strip()
                .removeprefix("```json")
                .removeprefix("```")
                .removesuffix("```")
                .strip()
            )

            data = json.loads(cleaned)
            index_name = data.get("index_name")

            if data.get("route") == "vector" and not self._is_known_vector_index(index_name):
                print(f"⚠️ LLM suggested unknown vector index: {index_name}, falling back to text2cypher")
                return RoutingDecision(route="text2cypher", question=question, fallback_reason="vector index not found")

            return RoutingDecision(question=question, **data)

        except Exception as e:
            print(f"[Router fallback] Failed to route with LLM: {e}")
            return RoutingDecision(route="text2cypher", question=question, fallback_reason=str(e))

    def _build_prompt(self, question: str) -> str:
        sections = ["""
    You are a retriever router for an Agentic system using Neo4j. You are the entry node within LangGraph.

    Based on the schema and available indexes, decide which retriever is best suited to answer the user's question.

    If there is no corresponding vector index please fall back to the Text2Cypher retrieval method.

    You MUST return a JSON object using this structure:
    - If using "text2cypher":         { "route": "text2cypher" }
    - If using "vector":              { "route": "vector", "index_name": "<RECOMMENDED_INDEX>" }

    Retriever Options:
    - "text2cypher": For structured questions about entities, properties, or relationships.
    - "vector": For vague, unstructured, or semantic/document-style questions.
    """]

        if self.neo4j_schema:
            sections.append(f"Neo4j Schema:\n{self.neo4j_schema}")

        if self.vector_index_infos:
            sections.append("Available Vector Indexes:\n" + json.dumps(self.vector_index_infos, indent=2))

        if self.fulltext_index_info:
            sections.append("Available Fulltext Index:\n" + json.dumps(self.fulltext_index_info, indent=2))

        sections.append(f"User Question:\n{question}")

        return "\n\n".join(sections)

    def _list_vector_indexes(self) -> list[Dict[str, Any]]:
        result = self.driver.execute_query(
            query_="""
            SHOW INDEXES YIELD name, type, entityType, labelsOrTypes, properties, options
            WHERE type = 'VECTOR'
            RETURN name, type, entityType, labelsOrTypes, properties, options
            """,
            parameters_={}
        )
        return [record.data() for record in result.records]

    def _is_known_vector_index(self, index_name: Optional[str]) -> bool:
        return any(index.get("name") == index_name for index in self.vector_index_infos)
