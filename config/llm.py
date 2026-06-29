from langchain_openai import ChatOpenAI
from config.settings import settings

def get_llm(temperature: float = 0.2):
    """
    Returns a configured LLM client used across all agents.
    Centralizing this lets us swap models/providers in one place.
    """
    return ChatOpenAI(
        model=settings.LLM_MODEL,
        temperature=temperature,
        api_key=settings.OPENAI_API_KEY,
    )