# A simple agent without a memory

from langgraph.graph import END, START, StateGraph
from typing import TypedDict, List
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

class AgentState(TypedDict):
    messages: List[HumanMessage]

graph = StateGraph(AgentState)

def process_node(state: AgentState) -> AgentState:
    llm = ChatOpenAI(model='gpt-4o')
    
    response = llm.invoke(state['messages'])

    print(f"\nAi: {response.content}")

    return state

graph.add_node('process_node', process_node)
graph.add_edge(START, 'process_node')
graph.add_edge("process_node", END)

app = graph.compile()

user_input = input("Enter: ")

while user_input != 'exit':
    result = app.invoke({'messages': [HumanMessage(content= user_input)]})
    user_input = input("Enter: ")


