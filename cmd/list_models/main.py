from google import genai
from google.genai import types  # type: ignore
import os

MODEL = "gemini-2.0-flash"
CONFIG = types.GenerateContentConfig(
    temperature=1.0,
    # max_output_tokes=100,
    # system_instruction="keep your reponses to within 20 words.",
)


def main():
    cl = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    print_model_list(cl)


def print_model_list(cl: genai.Client) -> None:
    for m in cl.models.list():
        print_model_info(m)
        print("---")
    
def print_model_info(m):
    print(f"{m.name}: {m.display_name}\n{m.description}\ntoken limits: in: {m.input_token_limit} out: {m.output_token_limit}, actions: {m.supported_actions}")


if __name__ == "__main__":
    main()
