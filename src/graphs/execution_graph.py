def execute_plan_item(state: State):
    print(f"🛠️ Executing plan item {state['plan_item_index']} ...")
    print(f"🛠️ Plan: {state['plan'].items}")
    plan_item = state["plan"].items[state["plan_item_index"]]
    print(f"🛠️ Plan item: {plan_item.title}")
    print(f"🛠️ Plan item prompt: {plan_item.prompt}")

    response = llm.invoke(
        [
            SystemMessage(content=plan_item.prompt),
            HumanMessage(
                content=f"The target website is {state['base_url']}. The plan item is {plan_item.title}."
            ),
        ]
    )
    return {"plan_item": response, "plan_item_index": state["plan_item_index"] + 1}
