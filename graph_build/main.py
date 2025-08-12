import os
import uuid
import asyncio
import pandas as pd
from dotenv import load_dotenv, dotenv_values
from typing import Dict

from langchain_openai import ChatOpenAI
from langchain_core.language_models import BaseChatModel
from langchain_community.chat_models.ollama import ChatOllama

from neo4j import GraphDatabase

from graph_build.pdf_extractor import PDFTextExtractor
from graph_build.structured_graph_build import Neo4jWriter
from graph_build.utils import normalize_column_name
from graph_build.graphrag_graph_extractor import GraphRAGExtractor
from neo4j_graphrag.experimental.components.types import TextChunk, TextChunks
from neo4j_graphrag.embeddings.base import Embedder
from neo4j_graphrag.embeddings.openai import OpenAIEmbeddings
from neo4j_graphrag.embeddings.sentence_transformers import SentenceTransformerEmbeddings


def main():
    load_dotenv()
    env_vars = dotenv_values()
    print("[DEBUG] Loaded .env values:", env_vars)

    print("[INFO] Starting PDF text extraction...")
    pdf_extractor = PDFTextExtractor()
    extracted_texts: Dict[str, str] = pdf_extractor.extract_texts()

    print("[INFO] Wrapping raw text into TextChunk objects...")
    chunk_list = []
    for filename, full_text in extracted_texts.items():
        paragraphs = full_text.split("\n\n")
        for idx, para in enumerate(paragraphs):
            cleaned = para.strip()
            if cleaned:
                chunk = TextChunk(
                    text=cleaned,
                    index=idx,
                    uid=str(uuid.uuid4()),
                    metadata={"filename": filename}
                )
                chunk_list.append(chunk)

    chunk_nodes: TextChunks = TextChunks(chunks=chunk_list)

    embedder: Embedder = (
        OpenAIEmbeddings(env_vars.get("TEXT_EMBEDDING_MODEL"))
        if env_vars.get("LOCAL_MODE") == "False"
        else SentenceTransformerEmbeddings(env_vars.get("TEXT_EMBEDDING_MODEL"))
    )

    print("[INFO] Initializing LLM and GraphRAG extractor...")
    llm: BaseChatModel = (
        ChatOllama(model="llama3.1:8b")
        if env_vars.get("LOCAL_MODE") == "True"
        else ChatOpenAI(model="gpt-4o-mini", temperature=0)
    )

    driver = GraphDatabase.driver(
        os.getenv("NEO4J_URI"),
        auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
    )

    graph_extractor = GraphRAGExtractor(
        llm=llm,
        driver=driver,
        embedder=embedder
    )

    print("[INFO] Extracting knowledge graph structure from text chunks...")
    asyncio.run(graph_extractor.extract_graph_data(chunk_nodes))

    print("[INFO] Loading structured Excel data...")
    structured_data_path = os.getenv("STRUCTURED_DATA_PATH")
    structured_data = pd.read_excel(structured_data_path)
    structured_data.columns = [normalize_column_name(col) for col in structured_data.columns]

    neo4j_writer = Neo4jWriter(df=structured_data, driver=driver, batch_size=1000)

    print("[INFO] Creating indexes for structured node types...")
    neo4j_writer.create_indexes()

    print("[INFO] Writing structured nodes and relationships to Neo4j...")
    neo4j_writer.write_all_structured_data()

    neo4j_writer.close()
    graph_extractor.close()
    print("[✅ DONE] All structured and unstructured graph data written successfully.")


if __name__ == "__main__":
    main()
