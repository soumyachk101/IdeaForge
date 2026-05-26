"""Synthesizer Agent - matches trends with RAG data to find opportunities."""
from crewai import Agent

from tools.rag_tools import RAGRetrieverTool
from llm.ollama_client import get_crewai_llm
from llm.prompts import SYNTHESIZER_PROMPT


def create_synthesizer_agent() -> Agent:
    return Agent(
        role="Idea Synthesizer",
        goal="Match current trends with historical monetization data and case studies to identify the strongest micro-SaaS opportunities",
        backstory=SYNTHESIZER_PROMPT,
        tools=[
            RAGRetrieverTool(),
        ],
        llm=get_crewai_llm(),
        verbose=True,
        allow_delegation=False,
    )
