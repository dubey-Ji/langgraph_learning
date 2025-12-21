# Objective:
# Conditional edge

from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# State
class AgentState(TypedDict):
    number1: int
    number2: int
    operation1: str
    finalNumber1: int
    number3: int
    number4: int
    operation2: str
    finalNumber2: int


# Nodes
def adder_node(state: AgentState) -> AgentState:
    """ This node is used to perform addition """
    state['finalNumber1'] = state['number1'] + state['number2']

    return state

def subtractor_node(state: AgentState) -> AgentState:
    """ This node is used to perform subtraction """
    state['finalNumber1'] = state['number1'] - state['number2']

def router_node(state: AgentState) -> AgentState:
    if state['operation1'] == "+":
        return "addition_path"
    elif state['operation1'] == "-":
        return "subtraction_path"

graph = StateGraph(AgentState)
graph.add_node("addition_node", adder_node)
graph.add_node("subtractor_node", subtractor_node)
graph.add_node("router_node", lambda state: state) # we are using lambda function because it is like a passthrough because we are taking state in router node but not returning it, that's why. This lambda function tells what is the input state that is the only output state.

graph.add_edge(START, "router_node")
graph.add_conditional_edges(
    "router_node",
    router_node,
    {
        "addition_path": "addition_node",
        "subtraction_path": "subtractor_node"
    }
)

# Node for second operations
def adder_node2(state: AgentState) -> AgentState:
    """ This node is used to perform addition """
    state['finalNumber2'] = state['number3'] + state['number4']

    return state

def subtractor_node2(state: AgentState) -> AgentState:
    """ This node is used to perform subtraction """
    state['finalNumber2'] = state['number3'] - state['number4']

    return state

def router_node2(state: AgentState) -> AgentState:
    if state["operation2"] == "+":
        return "addition_path2"
    elif state['operation2'] == "-":
        return "subtraction_path2"

graph.add_node("additon_node2", adder_node2)
graph.add_node("subtractor_node2", subtractor_node2)
graph.add_node("router_node2", lambda state: state)

graph.add_edge( "addition_node", "router_node2")
graph.add_edge("subtractor_node", "router_node2")

graph.add_conditional_edges(
    "router_node2",
    router_node2,
    {
        "addition_path2": "additon_node2",
        "subtraction_path2": "subtractor_node2"
    }
)

graph.add_edge("additon_node2", END)
graph.add_edge("subtractor_node2", END)

app = graph.compile()

result = app.invoke({"number1": 1, "number2": 2, "operation1": "+", "number3": 4, "number4": 2, "operation2": "-"})
print(result['finalNumber1'])
print(result['finalNumber2'])