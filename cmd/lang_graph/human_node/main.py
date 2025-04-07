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
    done: bool


def cust(state: State) -> State:
    # agent_response = state["messages"][-1]
    # print(f"Customer service agent: {agent_response.content}")

    print()
    cust_input = input("Please enter your request/feedback (q to quit): ")
    if cust_input in ["q", "quit", "exit", "bye"]:
        state["done"] = True
        return state
    return {
        "messages": cust_input
    }  # langgraph's add_messages will append this to state.


from langchain_core.messages.ai import AIMessage

def print_cust_svc_prefix():
    print()
    print("Customer service agent: ",end="")
def bot(state: State) -> State:
    welcome = "Welcome to ACME corp. How may I help you?"
    if len(state["messages"]) == 0:
        print_cust_svc_prefix()
        return {"messages": AIMessage(welcome)}
    
    print_cust_svc_prefix()
    return {"messages": llm.invoke(state["messages"])}


from langgraph.graph import StateGraph, START, END


def to_bot_or_quit(state: State) -> any:
    if state["done"]:
        return END
    return "bot"


def graph() -> any:
    g = StateGraph(State)  # g defines the graph
    g.add_node("bot", bot)
    g.add_edge(START, "bot")

    g.add_node("cust", cust)
    g.add_edge("bot", "cust")
    g.add_conditional_edges("cust", to_bot_or_quit)
    return g.compile()  # c is the compiled, invokeable graph


from pprint import pprint


def execute_graph(c) -> None:
    """Runs a compiled langgraph graph, c"""
    state: State = {"messages": [], "done": False}
    # state = c.invoke(state) # non-streaming

    for chunk,metadata in c.stream(state,stream_mode="messages"):
        print(chunk.content, end="")

    # print(f"number of messages = {len(state['messages'])}")
    # pprint(state["messages"])


def main():
    c = graph()
    execute_graph(c)


if __name__ == "__main__":
    main()
