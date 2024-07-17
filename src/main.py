import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from src.ui.cli import start_cli
from src.graph.hero_journey_graph import create_hero_journey_graph

# Load environment variables
load_dotenv()

def main():
    # Initialize OpenAI API
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("Please set the OPENAI_API_KEY environment variable")
    
    llm = ChatOpenAI(api_key=openai_api_key)
    
    # Create the hero's journey graph
    graph = create_hero_journey_graph(llm)
    
    # Start the CLI interface
    start_cli(graph)

if __name__ == "__main__":
    main()
