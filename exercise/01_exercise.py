from typing import TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    message: str

graph = StateGraph(AgentState)

def compliment_node(state: AgentState) -> AgentState:
    """ Simple node used to compliment """
    
    state['message'] = f"{state['message']}, you're doing an amazing job learning langgraph"

    return state

graph.add_node("compliment", compliment_node)

graph.set_entry_point("compliment")
graph.set_finish_point("compliment")

app = graph.compile()

result = app.invoke({"message": "Bob"})

print(result['message'])