import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from ui.cli import start_cli
from graph.hero_journey_graph import create_hero_journey_graph

# Load environment variables
load_dotenv()

def main():
    # Initialize Anthropic API
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    if not anthropic_api_key:
        raise ValueError("Please set the ANTHROPIC_API_KEY environment variable")
    
    llm = ChatAnthropic(model="claude-3-opus-20240229", api_key=anthropic_api_key)
    
    # Create the hero's journey graph
    graph = create_hero_journey_graph(llm)
    
    # Start the CLI interface
    start_cli(graph)

if __name__ == "__main__":
    main()