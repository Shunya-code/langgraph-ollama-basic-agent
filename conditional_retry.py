
from typing import TypedDict
from langchain_ollama import ChatOllama
from langgraph.graph import START,END,StateGraph

class AgentState(TypedDict):
    message:str
    response:str
    status:str
    retry_count:int

llm=ChatOllama(
    model="llama3.2:latest",
    temperature=0
)


def call_model(state:AgentState):
    print(">>>LLM MODE")
    result=llm.invoke(state["message"])
    return {
        "response":result.content
     }

def second_node(state:AgentState):
    print(">>> SECOND NODE")
    return {
        "status":"completed"
    }
def router(state:AgentState):
    print(">>>Router")
    print("retry_count:",state["retry_count"])

    if state["retry_count"]<1:
        return "retry"

    return "done"
def retry_node(state:AgentState):
    print(">>>Retry Node")

    return {
        "retry_count":state["retry_count"]+1
    }

graph=StateGraph(AgentState)
graph.add_node("llm",call_model)
graph.add_node("second",second_node)
graph.add_node("retry",retry_node)

graph.add_edge(START,"llm")
graph.add_edge("llm","second")

graph.add_conditional_edges(
    "second",
    router,
    {
    "retry":"retry",
    "done":END
    }
)          
graph.add_edge("retry","llm")
agent=graph.compile()

result=agent.invoke({
    "message":"Explain what an ai agent is?",
    "response":"",
    "status":"",
    "retry_count":0


})
print("\nFINAL STATE")
print(result)
