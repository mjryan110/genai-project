from .base_adapter import BaseLLMAdapter
from neo4j_graphrag.llm import OpenAILLM, LLMResponse


class Neo4jLLMAdapter(BaseLLMAdapter):
    def __init__(self, model: OpenAILLM):
        self.model = model

    def ask(self, prompt: str) -> LLMResponse:
        return self.model.invoke(prompt)

    def invoke(self, input: str, **kwargs) -> LLMResponse:
        return self.model.invoke(input, **kwargs)
