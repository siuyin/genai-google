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


from langgraph.graph import StateGraph, START, END
from pprint import pprint

def main():
    g = StateGraph(State)  # g defines the graph
    g.add_node("bot", bot)
    g.add_edge(START, "bot")
    c = g.compile()  # c is the compiled, invokeable graph

    state: State = {"messages":["why is the sky blue?"]}
    print(f"number of messages = {len(state['messages'])}")
    state = c.invoke(state)
    print(f"number of messages = {len(state['messages'])}")
    # pprint(state)
    print(state["messages"][1].content)


if __name__ == "__main__":
    main()
