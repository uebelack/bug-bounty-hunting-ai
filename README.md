# Bug Bounty Hunting with AI Agents

Demo code and presentation materials for the talk "Bug Bounty Hunting with AI Agents" at Basel One 2025.

## 🎯 Talk Abstract

Can AI agents automate bug bounty hunting? This talk explores the potential and limitations of using AI-powered agents to discover security vulnerabilities in web applications. Through live demonstrations using OWASP Juice Shop, we'll examine different approaches - from simple LLM prompts to sophisticated multi-phase agent architectures built with LangGraph.

## 📁 Repository Contents

### Presentation (`/presentation`)
Slidev-based presentation covering:
- Introduction to bug bounty hunting
- AI agents and LLM fundamentals
- Live demo attempts with increasing complexity
- Results, costs, and learnings
- Alternative approaches (Cybersecurity AI framework)

### Demo Code (`/src`)
Three demonstration approaches showing the evolution of AI bug hunting:

1. **Simple Agent** (`simple-agent.py`) - Basic ReAct agent using LangChain
2. **Extended Agent** (`extendend-agent.py`) - Multi-phase workflow with reconnaissance, planning, and execution

## 🚀 Running the Demos

### Prerequisites
- Python 3.13+
- Docker (for OWASP Juice Shop)

### Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start OWASP Juice Shop (the target):
```bash
docker run -p 3000:3000 --rm bkimminich/juice-shop
```

3. Run demos:
```bash
# Simple agent demo
python src/simple-agent.py

# Extended multi-phase agent
python src/extendend-agent.py
```

### View Presentation

```bash
cd presentation
yarn install
yarn dev  # Opens at http://localhost:3030
```

## 🔗 Resources

- **Talk**: Basel One 2025
- **Speaker**: David Übelacker (nag informatik ag)
- **Website**: [uebelacker.dev](https://uebelacker.dev)
- **Security Testing Assistant**: [Cybersecurity AI (CAI)](https://aliasrobotics.github.io/cai/)

## ⚠️ Disclaimer

These demonstrations are for educational purposes only. Always obtain proper authorization before testing any systems. The code is designed to work with intentionally vulnerable applications like OWASP Juice Shop.

## 📜 License

MIT License. See LICENSE for more information.