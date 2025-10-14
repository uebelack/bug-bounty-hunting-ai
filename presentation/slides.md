---
layout: cover
colorSchema: dark
favicon: https://uebelacker.dev/favicon.ico
fonts:
  sans: Fira Code
  serif: Roboto Slab
  mono: Fira Code
---

# Bug Bounty Hunting with AI Agents

### Can I automate bug bounty hunting using AI agents?

<div class="absolute bottom-10">
  <span class="font-700">
    David Übelacker
  </span>
</div>

---

# 👨‍💻 Who am I?

- **David �belacker**
- Software Architect @ nag informatik ag in Basel
- 20+ years of experience in web and mobile application development

<div class="absolute bottom-10">
  <div class="flex items-end">
    <img src="./images/nag.svg" style="width: 20%" />
    <div style="width:45%"></div>
    <div style="width: 30%; display: flex; flex-direction: column; align-items: center;">
      <img src="./images/qr.svg" style="width: 100%;"/>
      <div>uebelacker.dev</div>
    </div>
  </div>
</div>

---

# What I dream of doing

<img src="./images/hacker.png"/>

---

# What I'm actually doing

<img src="./images/pojo.png"/>

---
layout: two-cols-header
---

# What is Bug Bounty Hunting?

Companies pay ethical hackers to find and report security vulnerabilities.

<div style="padding-top: 40px;"/>

::left::

### Popular Platforms

- HackerOne (https://www.hackerone.com/)
- Bugcrowd (https://www.bugcrowd.com/)
- Intigriti (https://www.intigriti.com/)
- 🇨🇭 Bug Bounty Switzerland (https://www.bugbounty.ch/)

::right::

### How to learn hacking


- Web security (OWASP - The Open Worldwide Application Security Project) https://owasp.org/
- Hack The Box https://www.hackthebox.com/
- Try Hack Me https://tryhackme.com/
- Ask ChatGPT

---
layout: fact
---

### Can I automate bug bounty hunting using AI agents?

---

# Attempt #1

<img src="./images/chatgpt.png"/>

---

<img src="./images/violation.png"/>

<!-- ---

# What is a LLM?

**A Large Language Model (LLM) is a type of artificial intelligence designed to understand, predict, and generate human-like text.**

<img src="./images/llm.svg" style="margin-top: 50px;"/> -->

---
layout: fact
---

# Attempt #2

---

# What is an AI Agent?

An AI agent is a system that takes a goal, uses a large language model (LLM) and tools, and iterates until the goal is achieved.

<img src="./images/agents.svg" style="padding-bottom: 20px;"/>


---
layout: two-cols-header
---

# 🦜 LangChain & LangGraph  

::left::

### LangChain

A framework for building applications powered by LLMs. 

<div class="emoji-list">

* 🧠 Multiple LLM providers
* 📦 Document and vector stores
* 🛠️ External tools and APIs

</div>

::right::

### LangGraph

A framework for building complex, stateful AI agent workflows with advanced orchestration.

<div class="emoji-list">

* 🗃️ **State management** - Persistent memory
* 🔵 **Nodes** - Workflow components
* ➡️ **Edges** - Conditional logic

</div>

::bottom::

Both are frameworks for Python, but there are equivalents for JavaScript / TypeScript (**LangChain.js**) and Java (**LangChain4j**).

---
layout: two-cols-header
---

# 🧃 OWASP Juice Shop

::left::

OWASP Juice Shop is a modern, insecure web app used for security training, with hacking challenges and as a 'guinea pig' for security tools.

::right::

<img src="./images/juice.png"/>

::bottom::
https://owasp.org/www-project-juice-shop/

---
layout: fact
---

# Demo

---
layout: two-cols-header
---

# Attempt #2 - Result

::left::

* Runtime: **2.5m**
* Tokens: **1.144.127**
* Costs: **3.47$**
* Hacking Challenges Solved: **11**

::right::

<img src="./images/attempt-2-juice.png" style="width: 85%"/>


---

# Attempt #3

Three-phase workflow agent

* Phase 1: **Reconnaissance**
* Phase 2: **Plan**
* Phase 3: **Execute & Report**

<img src="./images/extended-agent.svg" style="padding-top: 60px;"/>

---
layout: two-cols-header
---

# Attempt #3 - Result

::left::

* Runtime: **73m**
* Tokens: **21'242'728**
* Costs: **65.59$**
* Hacking Challenges Solved: **18**


::right::

<img src="./images/attempt-3-juice.png" style="width: 85%"/>

---

# Cybersecurity AI (CAI)

Lightweight, open-source framework for AI-powered offensive & defensive automation. De facto AI Security framework, used by thousands of users & hundreds of organizations.

<div style="padding-top: 40px;"/>

<div class="emoji-list">

* 🤖 300+ AI Models (OpenAI, Anthropic, DeepSeek, Ollama, …)
* 🔧 Built-in security tools (reconnaissance, exploitation, privilege escalation)
* 🏆 Battle-tested (HackTheBox, bug bounties, real-world cases)
* 🎯 Agent-based modular architecture
* 🛡️ Guardrails: protection against prompt injection & dangerous commands
* 📚 Research foundation for democratizing Cybersecurity AI

</div>

<div style="padding-top: 50px;"/>

https://github.com/aliasrobotics/cai<br>
https://aliasrobotics.com/

---
layout: fact
---

# Demo

---

# Key Takeaways

These key takeaways highlight both the opportunities and challenges of using AI in security.

<div style="padding-top: 40px;"/>

<div class="emoji-list">

* 💸 **Expensive** costs more than you earn in bounties
* 📏 **Context limits** — analysis of a lot of data runs fast into context limits
* 🔄 **Different models** — models behave differently, don't expect the same results
* 🚨 **Easy** — unskilled hackers can launch easily AI-powered attacks
* ⚡ **Keep up** — security experts need to use AI in their daily work

</div>

---
layout: fact
---

# Questions?

<div style="display: flex; flex-direction: column; align-items: center;">
  <img src="./images/qr2.svg" style="width: 25%; margin-bottom: 20px;"/>
  
  https://github.com/uebelack/bug-bounty-hunting-ai

</div>