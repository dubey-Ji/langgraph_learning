# Objective:
# Loop
# We have achieved loop between guess node and hint node through conditional edge

from langgraph.graph import StateGraph, END, START
from typing import TypedDict, List
import random

class AgentState(TypedDict):
    player_name: str
    guesses: List[int]
    attempts: int
    lower_bound: int
    upper_bound: int
    target_number: int
    message: str

graph = StateGraph(AgentState)

def setup_node(state: AgentState) -> AgentState:
    state['attempts'] = 0
    state['lower_bound'] = 1
    state['upper_bound'] = 20
    state['target_number'] = 9
    # state['message'] = f"Hello {state['player_name']}"
    # print(state['message'])

    return state


def guess_node(state: AgentState) -> AgentState:
    number = random.randint(state['lower_bound'], state['upper_bound'])
    state['guesses'].append(number)
    state['attempts'] += 1

    return state

def hint_node(state: AgentState) -> AgentState:
    if state['attempts'] >= 7:
        return 'end'
    if state['guesses'][len(state['guesses']) - 1] == state['target_number']:
        return "end"
    elif state['guesses'][len(state['guesses']) - 1] < state['target_number']:
        state['lower_bound'] = state['guesses'][len(state['guesses']) - 1]
        print(f"lower bound: {state['lower_bound']}")
        return 'guess_node'
    elif state['guesses'][len(state['guesses']) - 1] > state['target_number']:
        state['upper_bound'] = state['guesses'][len(state['guesses']) - 1]
        print(f"upper bound: {state['upper_bound']}")
        return 'guess_node'


graph.add_node("guess_node", guess_node)
graph.add_node("setup_node", setup_node)
graph.add_node("hint_node", lambda state: state)

graph.add_edge(START, 'setup_node')
graph.add_edge('setup_node', 'guess_node')
graph.add_edge('guess_node', 'hint_node')
graph.add_conditional_edges(
    'hint_node',
    hint_node,
    {
        'guess_node': 'guess_node',
        "end": END
    }
)
graph.add_edge('hint_node', END)
app = graph.compile()

result = app.invoke({'player_name': 'ashutosh', 'guesses': []})
print(result)