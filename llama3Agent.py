from langchain_community.llms import Ollama
from Agent import Agent

# Define the LLaMA 3 agent
class LLaMA3Agent(Agent):
    def act(self, query: str, context : str) -> dict:
        llm = Ollama(model='llama3')
        query = query
        context = context
        response = llm.invoke(query)
        return response