# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a bug bounty hunting AI assistant built with LangGraph and LangChain. It uses graph-based agent architectures to perform reconnaissance, planning, and execution phases for security testing web applications.

## Key Architecture

The project uses a multi-phase agent architecture:

1. **Reconnaissance Phase**: Passive information gathering about the target using tools like Wappalyzer and HTTP requests
2. **Planning Phase**: Creates test plans based on reconnaissance data
3. **Execution Phase**: Executes the test plan items
4. **Reporting Phase**: Generates vulnerability reports

Main agent implementations:
- `src/simple-agent.py`: Basic ReAct agent using RequestsToolkit
- `src/extendend-agent.py`: Multi-phase state graph with subgraphs for each phase

## Development Commands

```bash
# Run the simple agent
python src/simple-agent.py

# Run the extended agent (uncomment the invoke() call first)
python src/extendend-agent.py

# Start the test target (Juice Shop)
docker run -p 3000:3000 --rm bkimminich/juice-shop

# Install dependencies
pip install -r requirements.txt
```

## Core Components

### State Graphs (`src/graphs/`)
- `reconnaissance_graph.py`: Passive OSINT gathering with Wappalyzer integration
- `planning_graph.py`: Test plan generation with Task dataclass
- `execution_graph.py`: Test execution logic
- `reporting_graph.py`: Vulnerability report generation

### Helpers (`src/helpers/`)
- `response_callback.py`: LangChain callback handler
- `cached.py`: Caching utilities

## Important Notes

- Default LLM is Claude Sonnet (`anthropic:claude-sonnet-4-20250514`)
- Requires Python 3.13+ (see `.python-version`)
- Test target runs on `http://localhost:3000`
- Graphs can output Mermaid diagrams via `graph.get_graph().draw_mermaid()`