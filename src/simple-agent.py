from langgraph.prebuilt import create_react_agent
from langchain_community.agent_toolkits.openapi.toolkit import RequestsToolkit
from langchain_community.utilities.requests import TextRequestsWrapper
from helpers.response_callback import ResponseCallback
from langchain_ollama.llms import OllamaLLM

tools = RequestsToolkit(
    requests_wrapper=TextRequestsWrapper(headers={}),
    allow_dangerous_requests=True,
).get_tools()


SYSTEM_PROMPT = """
You are my personal bug bounty hunting assistant. \
You will help me find vulnerabilities in web applications.
"""

agent = create_react_agent(
    model=OllamaLLM(base_url="http://192.168.222.220:11434", model="phi4:latest"),
    tools=tools,
    prompt=SYSTEM_PROMPT,
)

USER_PROMPT = """
Try to find vulnerabilities in the following web application: \
http://localhost:3000/
"""

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": USER_PROMPT,
            }
        ]
    },
    {"recursion_limit": 100, "callbacks": [ResponseCallback()]},
)
