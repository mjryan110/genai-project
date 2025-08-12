from pydantic import BaseModel
from typing import Optional, Any, List, Dict
from neo4j_graphrag.types import RetrieverResultItem, RawSearchResult


class RoutingDecision(BaseModel):
    route: str
    question: str
    index_name: Optional[str] = None
    fulltext_index_name: Optional[str] = None
    fallback_reason: Optional[str] = None


class Text2CypherRetrieverOutput(BaseModel):
    cypher: str
    results: List[RetrieverResultItem]


class RetrieverOutput(BaseModel):
    results: List[RetrieverResultItem]


class AppState(BaseModel):
    question: str
    decision: Optional[RoutingDecision] = None
    results: Optional[Text2CypherRetrieverOutput | RetrieverOutput] = None
    formatted_response: Optional[str] = None
    llm_only_response: Optional[str] = None


class MultiTurnState(BaseModel):
    """State for multi-turn conversation with clarification capabilities"""
    current_question: str
    conversation_history: List[Dict[str, Any]] = []
    turn_number: int = 1
    
    # Text2Cypher results
    results: Optional[Text2CypherRetrieverOutput] = None
    cypher_generated: Optional[str] = None
    records_found: int = 0
    
    # Error handling
    error_message: Optional[str] = None
    
    # Clarification logic
    needs_clarification: bool = False
    clarification_request: Optional[str] = None
    
    # Response formatting
    formatted_response: Optional[str] = None
    llm_only_response: Optional[str] = None


class AskRequest(BaseModel):
    question: str


class ClarificationRequest(BaseModel):
    clarification: str
    previous_state: Dict[str, Any]
