from abc import ABC, abstractmethod


class BaseLLMAdapter(ABC):
    @abstractmethod
    def ask(self, prompt: str) -> str:
        """Uniform interface to get a response from the LLM"""
        pass
