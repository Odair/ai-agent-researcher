from crewai import Agent, LLM

from app.tools.classify_tool import ClassifyTool
from app.tools.scrape_tool import ScrapeTool
from app.tools.search_tool import SearchTool

llm = LLM(
    model="anthropic/claude-sonnet-4-5-20250929",
    max_tokens=4096,
    temperature=0.7
)

def create_research_agent() -> Agent:
    return Agent(
        llm=llm,
        role="Financial Research Analyst",
        goal=(
            "Pesquisar notícias financeiras de empresas e tickers da B3, "
            "ler o conteúdo completo dos artigos e classificar o sentimento de cada um."
        ),
        backstory=(
            "Você é um analista financeiro especializado no mercado brasileiro. "
            "Usa ferramentas de busca e scraping para coletar informações atualizadas "
            "e classifica o impacto de cada notícia para o investidor."
        ),
        tools=[SearchTool(), ScrapeTool(), ClassifyTool()],
        verbose=True,
    )
