from .base_adapter import BaseLLMAdapter
from langchain_openai import ChatOpenAI


class LangchainLLMAdapter(BaseLLMAdapter):
    def __init__(self, model: ChatOpenAI):
        self.model = model

    def ask(self, prompt: str) -> str:
        return self.model.invoke(prompt).content
