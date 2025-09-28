---
layout: cover
colorSchema: light
fonts:
  sans: Fira Code
  serif: Roboto Slab
  mono: Fira Code
---

# Bug Bounty Hunting with AI Agents

### Can AI Agents Automate Bug Bounty Hunting?

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

::left::

### Why?

- Improves security 🔐
- Prevents cyberattacks 🚨
- Rewards hackers 💰

<br>

### How does it work?

- Hackers find bugs 🐞
- Report them responsibly 📩
- Get rewarded 🎉

::right::

### Popular Platforms

- HackerOne (https://www.hackerone.com/)
- Bugcrowd (https://www.bugcrowd.com/)
- Intigriti (https://www.intigriti.com/)
- 🇨🇭 Bug Bounty Switzerland (https://www.bugbounty.ch/)

---
layout: two-cols-header
---

# How to learn hacking

You can learn hacking by understanding cybersecurity fundamentals, practicing ethical hacking on platforms like Hack The Box and TryHackMe, exploring web security (OWASP Top 10), and developing problem-solving skills to identify and fix vulnerabilities.

::left::

- Web security (OWASP - The Open Worldwide Application Security Project) https://owasp.org/
- Hack The Box https://www.hackthebox.com/
- Try Hack Me https://tryhackme.com/
- Ask ChatGPT

::right::

<img src="./images/juice.png"/>

---
layout: fact
---

# Attempt #1

---

<img src="./images/violation.png"/>

---

# What is a LLM?

**A Large Language Model (LLM) is a type of artificial intelligence designed to understand, predict, and generate human-like text.**

<img src="./images/llm.svg" style="margin-top: 50px;"/>

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

* 🧠 Multiple LLM providers
* 📦 Document and vector stores
* 🛠️ External tools and APIs

::right::

### LangGraph

A framework for building complex, stateful AI agent workflows with advanced orchestration.

- 🗃️ **State management** - Persistent memory across steps
- 🔵 **Nodes** - Workflow components
- ➡️ **Edges** - Conditional logic

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

# Attempt #2

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

* **Reconnaissance**: Identify vulnerabilities and attack vectors through systematic target analysis
* **Plan**: Develop prioritized, actionable tasks based on reconnaissance findings
* **Execute & Report**: Execute planned tasks and generate comprehensive vulnerability reports

<img src="./images/extended-agent.svg" style="padding-top: 30px;"/>


https://github.com/uebelack/bug-bounty-hunting-ai
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

* 🤖 300+ AI Models (OpenAI, Anthropic, DeepSeek, Ollama, …)
* 🔧 Built-in security tools (reconnaissance, exploitation, privilege escalation)
* 🏆 Battle-tested (HackTheBox, bug bounties, real-world cases)
* 🎯 Agent-based modular architecture
* 🛡️ Guardrails: protection against prompt injection & dangerous commands
* 📚 Research foundation for democratizing Cybersecurity AI

<div style="padding-top: 50px;"/>
https://github.com/aliasrobotics/cai

---
layout: center
---

TBD

---
layout: center
---

# Learnings

* Can be really expensive, but cheap compared to a human
* Prompt, Context too long, js files
* Model really behave differently, don't expect your are application works the same way with different models
* Can't see that one was better than another
* Perhaps another approach would be give access to a browser and to burp suite
* Because of the context limitation its hard to make sure that the agent to do the same thing again and again
* You can give a LLM a big task you have to split it up into small ones, the smaller and more detailed the instrucations the better the results


---
<div style="display: flex; flex-direction: column; align-items: center;">
  <img src="./images/questions.jpg" style="width: 80%;"/>
</div>

---

# News

<div style="display: flex; flex-direction: column; align-items: center; gap: 5px;">
  <img src="./images/news02.jpg" style="width: 70%;"/>
  <img src="./images/news03.jpg" style="width: 70%;"/>
  <img src="./images/news01.jpg" style="width: 70%;"/>
</div>
