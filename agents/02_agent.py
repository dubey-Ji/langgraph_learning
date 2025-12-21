# Objective
# Agent with conversational history data

from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import START, StateGraph, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from typing import TypedDict, Union, List

load_dotenv()

class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]

graph = StateGraph(AgentState)
llm = ChatOpenAI(model='gpt-4o')

def process(state: AgentState) -> AgentState:
    result = llm.invoke(state['messages'])

    print(f"\nAI: {result.content}")
    state['messages'].append(AIMessage(content=result.content))

    return state

graph.add_node('process', process)
graph.add_edge(START, 'process')
graph.add_edge('process', END)

app = graph.compile()

conversation_history = []
user_input = input("Enter: ")
conversation_history.append(HumanMessage(user_input))
while user_input != 'exit':
    response = app.invoke({"messages": conversation_history})
    print(response)
    user_input = input("Enter: ")
    conversation_history.append(HumanMessage(content=user_input))