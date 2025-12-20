# Objective:
# Create a multiple node

from langgraph.graph import StateGraph
from typing import TypedDict, List

class AgentState(TypedDict):
    name: str
    age: str
    skills: List
    result: str

def fist_node(state: AgentState) -> AgentState:
    """ This is the first node """
    state['result'] = f"{state['name']}, welcome to the system."

    return state

def second_node(state: AgentState) -> AgentState:
    """ This is the second node """
    state['result'] = state['result'] + f" You are {state['age']} years old!"

    return state

def third_node(state: AgentState) -> AgentState:
    """ This is the third node """
    state['result'] = state['result'] + f" You have skills in {', '.join(state['skills'])}"

    return state


graph = StateGraph(AgentState)

graph.add_node("first_node", fist_node)
graph.add_node("second_node", second_node)
graph.add_node("third_node", third_node)
graph.add_edge("first_node", "second_node")
graph.add_edge("second_node", "third_node")

graph.set_entry_point("first_node")
graph.set_finish_point("third_node")

app = graph.compile()

result = app.invoke({"name": "Ashutosh", "age": "27", "skills": ["python", "langchain", "langgraph"]})
print(result['result'])