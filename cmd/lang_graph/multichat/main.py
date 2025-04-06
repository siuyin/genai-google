from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
print("GOOGLE_API_KEY=****")

from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

# State is derived from a TypedDict: See https://peps.python.org/pep-0589/
class State(TypedDict):
    messages: Annotated[
        list, add_messages
    ]  # messages is list with a note (for langgraph) to add messages instead of replacing them.

def bot(state: State) -> State:
    return {"messages": llm.invoke(state["messages"])}

from pprint import pprint
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

def main():
    c=graph()
    execute_graph(c)

def graph() -> any:
    g = StateGraph(State)  # g defines the graph
    g.add_node("bot", bot)
    g.add_edge(START, "bot")
    g.add_edge("bot", END)
    return g.compile(MemorySaver())  # the compiled, invokeable graph saving state in memory

def execute_graph(c) -> None:
    """Runs a compiled langgraph graph, c"""

    state: State = {"messages":["why is the sky blue?"]}
    print(f"number of messages = {len(state['messages'])}")

    config = {"configurable": {"thread_id": "abc123"}} # this is needed my the memory checkpoint saver to that it can save the different conversation threads.
    # state = c.invoke(state,config) # non-streaming
    for chunk,checkpoint_metadata in c.stream(state,config,stream_mode="messages"):
        print(chunk.content, end="")
        # pprint(checkpoint_metadata)
    
    print()
    print(f"number of messages = {len(state['messages'])}")
    # pprint(state)
    # print(state["messages"][1].content)
    

if __name__ == "__main__":
    main()
