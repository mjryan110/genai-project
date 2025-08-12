from neo4j_graphrag.llm import OpenAILLM
from neo4j_graphrag.llm.ollama_llm import OllamaLLM
from langchain_openai import ChatOpenAI
from ragas.llms import LangchainLLMWrapper


from .neo4j_adapter import Neo4jLLMAdapter
from .langchain_adapter import LangchainLLMAdapter
from .base_adapter import BaseLLMAdapter



class LLMRegistry:
    def __init__(self, model_name="gpt-4o", temperature=0, local_mode = False):
        self.model_name = model_name
        self.temperature = temperature
        self.local_mode = local_mode
        self._init_models()

    def _init_models(self):
        if self.local_mode:
            self.neo4j_llm = OllamaLLM(
                model_name=self.model_name,
                model_params={"temperature": self.temperature}
            )
        else:
            self.neo4j_llm = OpenAILLM(
                model_name=self.model_name,
                model_params={"temperature": self.temperature}
            )

        self.langchain_llm = ChatOpenAI(
            model=self.model_name,
            temperature=self.temperature
        )

        self.ragas_llm = LangchainLLMWrapper(self.langchain_llm)

        self.adapters = {
            "neo4j": Neo4jLLMAdapter(self.neo4j_llm),
            "langgraph": LangchainLLMAdapter(self.langchain_llm)
        }

    def get_adapter(self, mode: str = "langgraph") -> BaseLLMAdapter:
        return self.adapters[mode]

    def get_ragas_llm(self):
        return self.ragas_llm
