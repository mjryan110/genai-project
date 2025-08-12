from fastapi import FastAPI, HTTPException
from neo4j import GraphDatabase
from neo4j_graphrag.embeddings import OpenAIEmbeddings
from neo4j_graphrag.embeddings.base import Embedder
from neo4j_graphrag.embeddings.sentence_transformers import SentenceTransformerEmbeddings
from .agentservice import AgentService
from .llm import LLMRegistry
from .pydantictypes import AskRequest, ClarificationRequest, MultiTurnState
from dotenv import load_dotenv
import os
import logging

# Silence Neo4j info and warning logs
logging.getLogger("neo4j").setLevel(logging.ERROR)

# 🔃 Load .env variables
load_dotenv()

# 🌍 Env vars (capitalized to distinguish)
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o")
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.0))
TEXT_EMBEDDING_MODEL = os.getenv("TEXT_EMBEDDING_MODEL")
LOCAL_MODE = os.getenv("LOCAL_MODE", "False")

# 🔌 Neo4j driver
driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)

# 🧠 LLM Registry
llm_registry = LLMRegistry(model_name=MODEL_NAME, temperature=TEMPERATURE)

# 🧠 Embedder
embedder = OpenAIEmbeddings(model=TEXT_EMBEDDING_MODEL)

# 🕸️ Agent Service
agent_service = AgentService(
    llm_registry=llm_registry,
    driver=driver,
    database=NEO4J_DATABASE,
    embedder=embedder
)

app = FastAPI(
    title="CBRE Neo4j Agentic RAG API",
    description="Real estate knowledge graph API for CBRE using Neo4j and agentic RAG",
    version="1.0.0"
)

# 🚨 REST Endpoints
@app.post("/ask")
def ask_agent(request: AskRequest):
    """Initial question endpoint - starts a new conversation"""
    try:
        print(f"➡️ Received question: {request.question}")
        state = agent_service.run(request.question)
        
        return {
            "question": state.current_question,
            "needs_clarification": state.needs_clarification,
            "clarification_request": state.clarification_request,
            "results": state.results,
            "llm_only_response": state.llm_only_response,
            "formatted_response": state.formatted_response,
            "cypher_generated": state.cypher_generated,
            "records_found": state.records_found,
            "turn_number": state.turn_number,
            "conversation_history": state.conversation_history
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/clarify")
def clarify_question(request: ClarificationRequest):
    """Clarification endpoint - continues conversation with additional context"""
    try:
        print(f"➡️ Received clarification: {request.clarification}")
        print(f"➡️ Previous state: {request.previous_state}")
        
        # Reconstruct the previous state
        previous_state = MultiTurnState(**request.previous_state)
        
        # Add clarification to conversation
        updated_state = agent_service.add_to_conversation(previous_state, request.clarification)
        
        return {
            "question": updated_state.current_question,
            "needs_clarification": updated_state.needs_clarification,
            "clarification_request": updated_state.clarification_request,
            "results": updated_state.results,
            "llm_only_response": updated_state.llm_only_response,
            "formatted_response": updated_state.formatted_response,
            "cypher_generated": updated_state.cypher_generated,
            "records_found": updated_state.records_found,
            "turn_number": updated_state.turn_number,
            "conversation_history": updated_state.conversation_history
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




