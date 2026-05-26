"""CrewAI crew orchestration - ties all 3 agents together."""
import logging
from crewai import Crew, Process, Task
from agents.trend_scraper import create_trend_scraper_agent
from agents.synthesizer import create_synthesizer_agent
from agents.vc_agent import create_vc_agent

logger = logging.getLogger("ideaforge.crew")


def create_ideaforge_crew(niche: str = "developer tools") -> Crew:
    """Creates and returns the IdeaForge crew with all 3 agents."""
    trend_scraper = create_trend_scraper_agent()
    synthesizer = create_synthesizer_agent()
    vc_agent = create_vc_agent()

    task_scrape = Task(
        description=(
            f"Scrape the latest trends, products, and user complaints from all 4 sources "
            f"(Product Hunt, Hacker News, Reddit, Indie Hackers) focusing on the niche: {niche}. "
            f"Compile a comprehensive report of:\n"
            f"1. Top trending products/tools\n"
            f"2. User pain points and complaints (direct quotes)\n"
            f"3. Emerging technology trends\n"
            f"4. Market gaps identified"
        ),
        agent=trend_scraper,
        expected_output="A detailed trend report with specific products, user complaints, and market gaps.",
    )

    task_synthesize = Task(
        description=(
            f"Using the trend analysis from the previous step, search the RAG knowledge base for:\n"
            f"1. Matching monetization frameworks for each identified opportunity\n"
            f"2. Similar pain points and how they were monetized\n"
            f"3. Relevant startup case studies\n\n"
            f"Then score each opportunity by: market size, competition level, technical complexity, "
            f"willingness to pay. Propose the top 3-5 micro-SaaS ideas."
        ),
        agent=synthesizer,
        expected_output="A ranked list of 3-5 micro-SaaS ideas with monetization framework matches and scoring.",
        context=[task_scrape],
    )

    task_refine = Task(
        description=(
            f"Take the top opportunities from the synthesizer's analysis and create complete, "
            f"actionable micro-SaaS proposals. For each proposal include:\n"
            f"1. Problem statement with direct user quotes\n"
            f"2. Solution description and one-liner\n"
            f"3. Target audience with buyer persona\n"
            f"4. Exact tech stack (frontend, backend, database, AI/ML, hosting)\n"
            f"5. Pricing model with specific dollar amounts ($10-$50/month range)\n"
            f"6. MVP features (3-5 core features)\n"
            f"7. Step-by-step go-to-market strategy\n"
            f"8. Why this will work (evidence-based reasoning)\n\n"
            f"Propose 3-5 ideas. Each must be achievable by a solo developer in 2-4 weeks."
        ),
        agent=vc_agent,
        expected_output="3-5 detailed micro-SaaS proposals with tech stacks, pricing, features, and GTM strategies.",
        context=[task_synthesize],
    )

    crew = Crew(
        agents=[trend_scraper, synthesizer, vc_agent],
        tasks=[task_scrape, task_synthesize, task_refine],
        process=Process.sequential,
        verbose=True,
    )

    return crew


def run_idea_pipeline(niche: str = "developer tools") -> str:
    """Runs the full IdeaForge pipeline and returns the result."""
    logger.info(f"Starting idea pipeline for niche: {niche}")
    crew = create_ideaforge_crew(niche=niche)
    result = crew.kickoff(inputs={"niche": niche})
    logger.info("Idea pipeline completed")
    return str(result)


if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)
    niche = sys.argv[1] if len(sys.argv) > 1 else "developer tools"
    result = run_idea_pipeline(niche)
    print("\n" + "=" * 80)
    print("IDEAFORGE — Generated Micro-SaaS Proposals")
    print("=" * 80)
    print(result)
