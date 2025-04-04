from google import genai
from google.genai import types  # type: ignore
import os

MODEL = "gemini-2.0-flash"
# MODEL = "gemma-3-27b-it"
CONFIG = types.GenerateContentConfig(
    temperature=1.0,
    # max_output_tokes=100,
    # system_instruction="keep your reponses to within 20 words.",
)


def main():
    cl = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    # print(prompt(cl, "why is the sky blue?"))
    for chunk in stream(
        cl,
        """Read the question below:
Prepare a response in the style of William Shakespeare.
Check your response and replace all old English term with modern equivalents,
then output your response.
Check that the modernized version has the same nuances as your original response.
If not prepare an improved response and repeat the process.

Also translate your final response to Chinese, providing both the chinese text and pinyin versions.
Question:
What is the meaning of life?""",
    ):
        print(chunk.text, end="")


def prompt(cl: genai.Client, s: str) -> str:
    print(f"prompt: {s}")
    return cl.models.generate_content(model=MODEL, config=CONFIG, contents=s).text


def stream(cl: genai.Client, s: str) -> str:
    print(f"prompt: {s}")
    print("streaming response:")
    return cl.models.generate_content_stream(model=MODEL, config=CONFIG, contents=s)


if __name__ == "__main__":
    main()
