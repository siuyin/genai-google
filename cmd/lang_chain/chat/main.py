from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
print("GOOGLE_API_KEY=****")

from langchain_core.messages import HumanMessage, SystemMessage


def prompt(model, prompt: str) -> str:
    # r = model.invoke([HumanMessage(prompt)])
    r = model.invoke(prompt)
    return r.content


def stream(model, prompt) -> any:
    return model.stream([HumanMessage(prompt)])


def main():
    print(prompt(llm, "Why is the sky blue?"))

    # for chunk in stream(llm, "Why is the sky blue?"):
    #     print(chunk.content, end="")
    # print()


if __name__ == "__main__":
    main()
