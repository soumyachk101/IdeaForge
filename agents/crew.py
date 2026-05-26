"""CrewAI crew orchestration - ties all 3 agents together."""
from crewai import Crew, Process, Task
from agents.trend_scraper import create_trend_scraper_agent
from agents.synthesizer import create_synthesizer_agent
from agents.vc_agent import create_vc_agent


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
            "Take the top opportunity from the synthesizer's analysis and create a complete, "
            "actionable micro-SaaS proposal. Include:\n"
            "1. Problem statement with direct user quotes\n"
            "2. Solution description\n"
            "3. Target audience with buyer persona\n"
            "4. Exact tech stack (frontend, backend, database, hosting)\n"
            "5. Pricing model with specific dollar amounts\n"
            "6. Step-by-step go-to-market strategy\n"
            "7. Revenue projections (Year 1 and Year 2)\n"
            "8. Competitive advantage analysis"
        ),
        agent=vc_agent,
        expected_output="A complete micro-SaaS business proposal in the specified format with all sections filled.",
        context=[task_synthesize],
    )

    crew = Crew(
        agents=[trend_scraper, synthesizer, vc_agent],
        tasks=[task_scrape, task_synthesize, task_refine],
        process=Process.sequential,
        verbose=True,
    )

    return crew


def run_idea_generation(niche: str = "developer tools") -> str:
    """Runs the full IdeaForge pipeline and returns the result."""
    crew = create_ideaforge_crew(niche=niche)
    result = crew.kickoff(inputs={"niche": niche})
    return str(result)


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    result = run_idea_generation("developer tools")
    print("\n" + "=" * 80)
    print("IDEAFORGE RESULT")
    print("=" * 80)
    print(result)
