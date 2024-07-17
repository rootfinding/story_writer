# Hero Journey Writer

An interactive story writing game based on Joseph Campbell's Hero's Journey, powered by LangGraph.

## Overview

Hero Journey Writer is a Python-based interactive storytelling application that guides users through creating their own hero's journey narrative. Using the structure of Joseph Campbell's monomyth, this tool combines AI-generated content with user input to craft unique and engaging stories.

## Features

- Interactive command-line interface
- AI-assisted story generation based on the hero's journey structure
- User decision points that affect the story's direction
- Multiple story paths and outcomes
- Final story compilation and display

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/hero-journey-writer.git
   cd hero-journey-writer
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use 
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up your OpenAI API key:
   Create a `.env` file in the project root and add your API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

Run the main script to start the interactive story writing process:

```
python src/main.py
```

Follow the prompts to make choices and shape your hero's journey!

## Project Structure

- `src/`: Source code for the application
  - `main.py`: Entry point of the application
  - `ui/`: User interface modules
  - `story/`: Story generation and template modules
  - `graph/`: LangGraph implementation of the hero's journey
  - `utils/`: Utility functions and helpers
- `tests/`: Unit tests for the application
- `requirements.txt`: Required Python packages
- `.env`: Environment variables (not tracked by git)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
