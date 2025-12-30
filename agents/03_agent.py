# Objective: ReAct Agent

from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import END, StateGraph
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

graph = StateGraph(AgentState)

@tool
def add(a: int, b: int) -> int:
    """ This is used to add two numbers and return a sum """
    return a + b

tools = [add]

model = ChatOpenAI(model="gpt-4o").bind_tools(tools=tools)

def process(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(
        content="You are ai assistant, please answer my query to the best of your ability"
    )
    result = model.invoke([system_prompt] + state['messages'])

    return {"messages": [result]}

def should_continue(state: AgentState) -> str:
    messages = state['messages']
    last_message = messages[-1]
    if not last_message.tool_calls:
        return 'end'
    else:
        return 'continue'

tool_node = ToolNode(tools=tools)
graph.add_node('process', process)
graph.add_node('tools', tool_node)
graph.set_entry_point('process')
graph.add_conditional_edges(
    'process',
    should_continue,
    {
        'continue': 'tools',
        'end': END
    }
)

graph.add_edge('tools', 'process')
app = graph.compile()

inputs = {"messages": [HumanMessage(content="what is the 2 plus 2. What is 3 plus 6")]}
result = app.invoke(inputs)
print(result['messages'])

