Introduction

* Hello everyone, thanks for joining my talk.
* Topic: Bug Bounty Hunting with AI Agents

About Me

* I’m David, a software developer.
* Software architect at nag in Basel (nag.ch).
* Small but great company, good employer and IT partner.
* 20+ years experience in web & mobile development.
* Still struggling with encodings as you can see on my lastname.
* Contact: ueblacker.dev or scan the QR code.

Hacker Dreams

* Always dreamed of being a notorious hacker.
* Reality: I write Java POJOs every day.
* Not great at hacking — but curious!

Bug Bounty as a Hobby

* Got into bug bounty hunting out of interest in pentesting.
* It’s like solving puzzles — and you can get paid!
* Helps developers avoid security mistakes.

What is Bug Bounty Hunting?

* Find & report security vulnerabilities before attackers do.
* Companies create programs with clear rules & scope.
* Legal & ethical hacking — rewards include money or recognition.

Where to Start

* Platforms: HackerOne, BugCrowd, BugBountySwitzerland.
* Learn with Hack The Box, TryHackMe.
* Ask ChatGPT or your favorite LLM.
* Must-know: OWASP and the Juice Shop app (intentionally insecure).
* Juice Shop = perfect testing ground for my AI agents.

Attempt #1

* Just use chat GPT "Please hack tesla.com"
* Doesn't really work, you can make Chat GPT to a simple security scan of your own website
* And it's violating the terms of Chat GPT

What is an LLM?

* AI trained to understand and generate text
* static knowlegde, doesn't learn during conversations
* But the results are really impresive
* We tend to expect far more from LLM's than they are capable of
* You can build or use tools around LLM's that can reduce the limitations

What is an Agent?

* An agent takes a goal: e.g. find the best restaurant in basel
* Has access to a llm and tools like a web search engine
* Gives the goal with the tools to the llm and the llm decides when the goal is achieved

LangChain & LangGraph

* LangChain: tools & connectors for LLMs
* LangGraph: orchestration of complex agent workflows
* Python oss but pendants for JS and Java

Attempt #2


