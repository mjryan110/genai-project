from neo4j_graphrag.types import RetrieverResultItem
from neo4j_graphrag.retrievers import VectorRetriever

from neo4j import Record

class VectorRetrieverBuilder:
    def __init__(self, driver, database, index_name, embedder):
        self.driver = driver
        self.database = database
        self.index_name = index_name
        self.embedder = embedder

    def build(self):

        def result_formatter(record: Record) -> RetrieverResultItem:
            node = record.get("node")
            if not node:
                return RetrieverResultItem(content="⚠️ Missing node", metadata={"score": record.get("score")})

            name = node.get("GO_name", "[no name]")
            desc = node.get("GO_defn", "[no definition]")
            score = record.get("score")

            return RetrieverResultItem(
                content=f"{name}\n{desc}",
                metadata={"score": score}
            )

        return VectorRetriever(
            driver=self.driver,
            neo4j_database=self.database,
            index_name=self.index_name,
            embedder=self.embedder,
            result_formatter=result_formatter
        )