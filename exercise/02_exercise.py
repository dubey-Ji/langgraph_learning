# Objective to achieve:
# Handling multiple values in state.


from math import prod
from langgraph.graph import StateGraph
from typing import TypedDict, List

class AgentState(TypedDict):
    values: List
    name: str
    operation: str
    result: str

def process_the_value(state: AgentState) -> AgentState:
    """ Used to process the value """
    if state["operation"] == "+":
        state['result'] = f"Hi, {state['name']} your answer is {sum(state['values'])}"
    elif state["operation"] == "*":
        state['result'] = f"Hi, {state['name']} your answer is {prod(state['values'])}"
    else:
        state['result'] = f"Hi, {state['name']} can't calculate the answer as operation is invalid"
        

    return state

graph = StateGraph(AgentState)

graph.add_node("process", process_the_value)
graph.set_entry_point("process")
graph.set_finish_point("process")

app = graph.compile()

result = app.invoke({"values": [1,2,3,4], "name": "Ashutosh", "operation": "-"})

print(result['result'])