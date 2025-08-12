from typing import Dict, List, Optional
from langchain_core.documents import Document
from langchain_core.language_models.base import BaseLanguageModel
from langchain_experimental.graph_transformers.llm import LLMGraphTransformer
from langchain_community.graphs.graph_document import GraphDocument
from collections import defaultdict


class GraphExtractor:
    def __init__(
        self,
        llm: BaseLanguageModel,
        allowed_nodes: Optional[List[str]] = None,
        allowed_relationships: Optional[List[str]] = None,
    ):
        self.transformer = LLMGraphTransformer(
            llm=llm,
            allowed_nodes=allowed_nodes or [],
            allowed_relationships=allowed_relationships or [],
            strict_mode=True,
        )

    def extract_graphs(self, text_chunks: Dict[str, str]) -> Dict[str, GraphDocument]:
        """
        text_chunks should be in the form:
        {
            "filename_0.pdf": "full text...",
            "filename_1.pdf": "full text...",
            ...
        }
        """
        graph_documents: Dict[str, GraphDocument] = {}
        for chunk_id, text in text_chunks.items():
            doc = Document(page_content=text, metadata={"chunk_id": chunk_id})
            graph_doc = self.transformer.process_response(doc)
            graph_documents[chunk_id] = graph_doc
        return graph_documents

    def serialize_graph_documents(self, graph_documents: Dict[str, GraphDocument]) -> Dict[str, List[Dict]]:
        nodes, relationships = [], []
        for graph_doc in graph_documents.values():
            for node in graph_doc.nodes:
                nodes.append({
                    "id": str(node.id),
                    "type": node.type,
                    "properties": node.properties or {},
                })
            for rel in graph_doc.relationships:
                relationships.append({
                    "source_id": str(rel.source.id),
                    "source_type": rel.source.type,
                    "target_id": str(rel.target.id),
                    "target_type": rel.target.type,
                    "rel_type": rel.type,
                    "properties": rel.properties or {},
                })
        return {"nodes": nodes, "relationships": relationships}
    

    def build_chunk_entity_links(self, chunk_nodes, entity_nodes):
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

    

    @staticmethod
    def group_graph_data(graph_dict: Dict[str, List[Dict]]) -> Dict:
        grouped = {
            "nodes_by_type": defaultdict(list),
            "relationships_by_type": defaultdict(list),
        }

        for node in graph_dict["nodes"]:
            node_type = node["type"]
            grouped["nodes_by_type"][node_type].append({
                "id": node["id"],
                **node.get("properties", {})
            })

        for rel in graph_dict["relationships"]:
            rel_type = rel["rel_type"]
            grouped["relationships_by_type"][rel_type].append({
                "source_id": rel["source_id"],
                "source_type": rel["source_type"],
                "target_id": rel["target_id"],
                "target_type": rel["target_type"],
                **rel.get("properties", {})
            })

        return grouped
        
    

