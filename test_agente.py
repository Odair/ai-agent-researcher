from crewai import Task, Crew                                                 
from app.agents.research_agent import create_research_agent                   
  
agent = create_research_agent()                                               
task = Task(                                              
        description="Pesquise notícias sobre PETR4, leia o conteúdo dos artigos e classifique o sentimento.",                                                   
        agent=agent,
        expected_output="Lista de notícias com sentiment (positive/negative/noise) e razão."                                                                    
      )
crew = Crew(agents=[agent], tasks=[task])                                     
print(crew.kickoff())