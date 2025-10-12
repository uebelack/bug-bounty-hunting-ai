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
* Not great at hacking — but curious!
* Reality: I write Java POJOs every day.

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
* Last year developer conference, needed a side project to learn all this new nice AI stuff

5'

Attempt #1

* Just use chat GPT "Please hack tesla.com"
* Doesn't really work, you can make Chat GPT to a simple security scan of your own website
* And it's violating the terms of Chat GPT

What is an LLM?

* A LLM is made to create human like text
* You send a text to the model and you get an answer
* The model is static, i can't learn or rember something by itself 

What is an Agent?

* An agent takes a goal: e.g. find the best restaurant in basel
* Has access to a llm and tools like a web search engine
* repeatedly calls the llm and tools until it has achieved the goal

LangChain & LangGraph

* LangChain: tools & connectors for LLMs
* LangGraph: orchestration of complex agent workflows
* Python oss but pendants for JS and Java
* Lize Raes


Juice Shop

* Most insecure web application out there
* Provided by OWASP for training purposes

7'

Attempt #2 — Result

* Very little effort, impressive result

12'

Attempt #3

* Three-phase agent application
* Reconnaissance (analysis)
* Planning of small hacking tasks
* Execution using an additional analysis tool
* Creating a report that includes everything needed, such as steps to reproduce

Attempt #3 — Result

* My dream of having an agent that automatically performs 24/7 bug-bounty hunting was no longer realistic — too expensive.
* Researched whether others had the same idea.
* All companies providing security tools are also integrating AI.
* Found one promising open-source security tool I want to show you briefly at the end.

14'

Cybersecurity AI (CAI)

* Open source
* A lot of included tools
* Extensible
* An assistant that works like GitHub Copilot or Claude Code
* From AliasRobotics, which does security testing of robots

18'

Key takeaways

* Too expensive for fully automated bug-bounty hunting
* Context size limits are a problem
* Models differ significantly
* Cybersecurity attacks have become easier to carry out
* Impressive how much can be achieved with very little effort
* Like us developers, security experts need to keep up with developments to avoid falling behind malicious attackers

