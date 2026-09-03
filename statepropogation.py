from typing import TypedDict
from langgraph.graph import START,END,StateGraph
from langchain_ollama import ChatOllama

class AgentState(TypedDict):

    message:str
    response:str
    status: str


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
    print(">>>> SECOND NODE")
    print("STATE INSIDE SEOCND NODE")
    #print(state)
    #return {
     #   "response": "FINAL"+state["response"]
    #}
    return {
        "status":"completed"
    }

graph=StateGraph(AgentState)

graph.add_node("llm",call_model)
graph.add_node("second",second_node)

graph.add_edge(START,"llm")
graph.add_edge("llm","second")

agent=graph.compile()

result=agent.invoke({
    "message":"Explain what an ai agent is ?",
    "response":"",
    "status": ""
})
print("\nFinal State")
print(result)
