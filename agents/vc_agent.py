"""VC/Monetization Agent - refines ideas into actionable proposals."""
from crewai import Agent

from tools.rag_tools import RAGRetrieverTool
from llm.ollama_client import get_crewai_llm
from llm.prompts import VC_ADVISOR_PROMPT


def create_vc_agent() -> Agent:
    return Agent(
        role="Micro-SaaS Founder Advisor",
        goal="Refine identified opportunities into actionable micro-SaaS proposals with exact tech stacks, pricing models, and go-to-market strategies",
        backstory=VC_ADVISOR_PROMPT,
        tools=[RAGRetrieverTool()],
        llm=get_crewai_llm(),
        verbose=True,
        allow_delegation=False,
    )
