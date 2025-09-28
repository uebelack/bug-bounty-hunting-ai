from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph import StateGraph, START, END
from typing import List, TypedDict
from pydantic import BaseModel, Field


class Task(BaseModel):
    title: str = Field(
        description="Descriptive title for this specific security assessment task \
            (e.g., 'Directory Enumeration', 'Authentication Testing', 'Input Validation Analysis')",
    )
    instructions: str = Field(
        description="Detailed instructions that guide the bug bounty hunter agent on how to \
            execute this specific task, including objectives, methodologies, tools to use, \
            success criteria, and expected deliverables. Please include all relevant information \
            needed to execute the task from the reconnaissance phase onward.",
    )


class Plan(BaseModel):
    tasks: List[Task] = Field(
        description="List of tasks to be executed during the bug bounty engagement",
    )


class State(TypedDict):
    base_url: str
    reconnaissance: str
    plan: List[Task]


SYSTEM_PROMPT = """
You are a planning assistant for an authorized bug-bounty team. 
The reconnaissance phase has already been completed and the reconnaissance report 
will be provided as input. Use only information from that reconnaissance report 
(do not perform or suggest any further reconnaissance).

You will generate a prioritized set of test tasks aimed at discovering vulnerabilities
on the target website. Tasks must be actionable for a security tester but must not contain
step-by-step exploit scripts or instructions that would enable malicious actors. 
Keep guidance high-level and focused on objectives, prerequisites and expected observations.

Scope (what to cover)

- Authentication & credential handling — password reset, account enumeration, MFA, leaked creds.
- Session management — session fixation, expiry, Secure/HttpOnly/SameSite, rotation on privilege change.
- Broken access control / authorization — horizontal/vertical privilege escalation, IDORs.
- Input validation & injection families — SQLi, NoSQL/LDAP, command/OS injection, template injection.
- Cross-Site Scripting (XSS) — reflected, stored, DOM contexts (HTML, attribute, JS, URL).
- Cross-Site Request Forgery (CSRF) — state-changing endpoints without anti-CSRF tokens, SameSite issues.
- Clickjacking / UI redress — missing X-Frame-Options / CSP frame-ancestors on sensitive pages.
- CORS / cross-origin misconfiguration — overly permissive origins, credentials with wildcard.
- Insecure direct object references (IDOR) — predictable IDs, missing server-side checks.
- File upload & parsing — MIME/type checks, executable uploads, image processing vulnerabilities.
- Server-Side Request Forgery (SSRF) — URL fetchers, open-redirect-supported fetches, metadata endpoints.
- Open redirect / URL handling — unvalidated redirect parameters, canonicalization issues.
- Security headers & TLS config — HSTS, CSP, Referrer-Policy, TLS versions/ciphers.
- Directory Traversal and Information Disclosure Testing
- Token-based auth & JWT issues — signing, alg none, audience/issuer checks, token lifetime.
- API-specific checks (REST / GraphQL / WebSockets) — object-level auth, introspection, WebSocket auth.
- Rate limiting & brute-force protections — account lockout, IP throttling, CAPTCHA.
- Business-logic & workflow abuse — order manipulation, refunds, race conditions.
- Data exposure & privacy — sensitive data in responses, verbose errors, backups.
- Dependency & component vulnerabilities — outdated libs, known CVEs.
- Insecure deserialization & object tampering — client-accepted serialized objects.
- XML-related risks (XXE) — XML parsers, SOAP endpoints.
- Client-side storage & secrets — tokens in localStorage, API keys in JS.

Also include any additional relevant test areas suggested by the reconnaissance report.

"""


def create_planning_graph(llm: BaseChatModel):
    def plan(state: State):
        print(f"🛠️ Planning ...")
        response = llm.with_structured_output(Plan).invoke(
            [
                SystemMessage(content=(SYSTEM_PROMPT)),
                HumanMessage(
                    content=f"The reconnaissance report is: {state['reconnaissance']}"
                ),
                HumanMessage(content=f"The target website is {state['base_url']}."),
            ]
        )

        return {"plan": response.tasks}

    graph_builder = StateGraph(State)
    graph_builder.add_node("plan", plan)

    graph_builder.add_edge(START, "plan")
    graph_builder.add_edge("plan", END)

    result = graph_builder.compile()
    print(result.get_graph().draw_mermaid())
    return result
