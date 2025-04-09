from pydantic import BaseModel
class Response(BaseModel):
    abstract: str
    body: str
    conclusion: str


from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage


def main():
    sys = """You are a helpful research assisted tasked in a structured manner by
providing an abstract, body and conclusion.
First silently write out your response in full.
The create an abstract to entice and lead the reader to read the full body of your response.
To write your body revise your original response to make it more concise, keeping the language simple and ensuring a good flow though the points you are making.
Finaly write your conclusion to summarize in a short paragraph your findings.                          
"""

    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    print("GOOGLE_API_KEY=****")

    # filterwarnings("ignore", message="ChatGoogleGenerativeAI.with_structured_output")
    structured_output_llm = llm.with_structured_output(Response)
    # print(structured_output_llm.invoke("Why is the sky blue?"))
    # print(structured_output_llm.invoke("Why is the meaning of life? Respond in the style of Sun Tzu."))
    msgs = sys + "What is the meaning of life? Respond in the style of Confucius."
    print(structured_output_llm.invoke(msgs))


if __name__ == "__main__":
    main()
