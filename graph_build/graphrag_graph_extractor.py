from typing import Dict, List
from langchain_core.language_models.base import BaseLanguageModel
from neo4j import Driver
import asyncio
from neo4j_graphrag.experimental.components.kg_writer import Neo4jWriter
from neo4j_graphrag.experimental.pipeline import Pipeline
from neo4j_graphrag.experimental.components.entity_relation_extractor import (
    LLMEntityRelationExtractor,
    ERExtractionTemplate,
    SchemaEnforcementMode,
    OnError,
)
from neo4j_graphrag.experimental.components.embedder import TextChunkEmbedder
from neo4j_graphrag.experimental.components.types import (
    TextChunk,
    TextChunks,
    Neo4jGraph,
)
from neo4j_graphrag.experimental.components.kg_writer import Neo4jWriter as GraphRAGNeo4jWriter
from neo4j_graphrag.experimental.components.schema import (
    SchemaBuilder,
    SchemaEntity,
    SchemaProperty,
    SchemaRelation,
    SchemaConfig,
)
from neo4j_graphrag.embeddings.base import Embedder


class GraphRAGExtractor:
    def __init__(
        self,
        llm: BaseLanguageModel,
        driver: Driver,
        embedder: Embedder,
    ):
        self.driver = driver
        self.neo4j_writer = Neo4jWriter(self.driver)
        self.graph_writer = GraphRAGNeo4jWriter(self.driver)
        self.chunk_embedder = TextChunkEmbedder(embedder)
        
        self.entities = [
            SchemaEntity(
                label="System",
                description="A system or component in the architecture.",
                properties=[SchemaProperty(name="name", type="STRING", description="System name")],
            ),
            SchemaEntity(
                label="API",
                description="An exposed API.",
                properties=[SchemaProperty(name="name", type="STRING", description="API name")],
            ),
            SchemaEntity(
                label="Storage",
                description="A database or storage system.",
                properties=[SchemaProperty(name="name", type="STRING", description="Storage name")],
            ),
        ]

        self.relations = [
            SchemaRelation(label="USES", description="One system uses another."),
            SchemaRelation(label="EXPOSES_API", description="A system exposes an API."),
            SchemaRelation(label="CALLS_API", description="A system calls an API."),
            SchemaRelation(label="HOSTED_ON", description="A system is hosted on a storage component."),
        ]

        self.potential_schema = [
            ("System", "USES", "System"),
            ("System", "EXPOSES_API", "API"),
            ("System", "CALLS_API", "API"),
            ("System", "HOSTED_ON", "Storage"),
        ]

        self.schema_builder = SchemaBuilder()

        self.entity_relation_extractor = LLMEntityRelationExtractor(
            llm=llm,
            prompt_template=ERExtractionTemplate(),
            create_lexical_graph=True,
            enforce_schema=SchemaEnforcementMode.STRICT,
            on_error=OnError.IGNORE,
            max_concurrency=5,
        )

        self.pipeline = Pipeline()
        self.pipeline.add_component(self.neo4j_writer, name="writer")
        self.pipeline.add_component(self.chunk_embedder, name="embedder")
        self.pipeline.add_component(self.schema_builder, name="schema")
        self.pipeline.add_component(self.entity_relation_extractor, name="extractor")
        
        self.pipeline.connect("schema", "extractor", input_config={"schema": "schema"})
        self.pipeline.connect("embedder", "extractor", input_config={"chunks": "embedder"})
        self.pipeline.connect("extractor", "writer", input_config={"graph": "extractor"})

        self.last_graphs: List[Neo4jGraph] = []



    async def extract_and_write_graphs(self, chunk_list: TextChunks) -> None:
        pipe_inputs = {
            "schema": {
                "entities": self.entities,
                "relations": self.relations,
                "potential_schema": self.potential_schema,
            },
            "embedder": {
                "text_chunks": chunk_list
            }
        }

        return await self.pipeline.run(pipe_inputs)

    async def extract_graph_data(self, chunk_nodes: TextChunks) -> List[Neo4jGraph]:
        await self.extract_and_write_graphs(chunk_nodes)
        return self.last_graphs

    def build_chunk_entity_links(self, chunk_nodes: List[Dict], entity_nodes: List[Dict]) -> List[Dict]:
        links = []
        for chunk in chunk_nodes:
            chunk_text = chunk.get("text", "").lower()
            chunk_id = chunk.get("id")
            for entity in entity_nodes:
                entity_id = entity.get("id")
                entity_name = entity.get("name", "").lower()
                if entity_name and entity_name in chunk_text:
                    links.append({
                        "start_id": chunk_id,
                        "end_id": entity_id,
                        "type": "MENTIONS"
                    })
                    print(f"[MATCH] Chunk '{chunk_id}' mentions entity '{entity_name}'")
        return links

    def close(self):
        self.driver.close()
