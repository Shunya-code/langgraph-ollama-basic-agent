from typing import TypedDict
from langgraph.graph import StateGraph,START,END
from langchain_ollama import ChatOllama

class AgentState(TypedDict):

    message:str
    response:str

llm=ChatOllama(
    model="llama3.2:latest",
    temperature=0
)

def call_model(state:AgentState):

    result=llm.invoke(state["message"])

    return {
        "response":result.content
    }

graph=StateGraph(AgentState)
graph.add_node("llm",call_model)
graph.add_edge(START,"llm")
graph.add_edge("llm",END)
agent=graph.compile()


if __name__=="__main__":
    result=agent.invoke({
        "message":"Explain what an Ai agent is in one sentence"
    })
    print(result['response'])

