from langchain_core.callbacks import BaseCallbackHandler
from typing import Any, Dict


class ResponseCallback(BaseCallbackHandler):
    def on_llm_end(self, response: Any, **kwargs: Any) -> None:
        if hasattr(response, "generations") and response.generations:
            content = response.generations[0][0].text
            print(f"🤖 {content}\n")

    def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> None:
        tool_name = serialized.get("name", "Unknown Tool")
        print(f"🌎 {tool_name}: {input_str}")
        print("---------------------------------------------")
