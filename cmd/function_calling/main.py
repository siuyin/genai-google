from google import genai
from google.genai import types  # type: ignore
import os


def get_current_weather(location: str) -> str:
    """Returns the current weather.

    Args:
      location: The city and state, e.g. San Francisco, CA
      postcode: Postal code, eg. 587967

    Returns:
      The current weather.
    """
    return f"{location}: rainy with a 50% chance of sunshine"


def get_current_weather_with_postcode(location: str, postcode: str) -> str:
    """Returns the current weather.

    Args:
      location: The city and state, e.g. San Francisco, CA
      postcode: Postal code, eg. 587967

    Returns:
      The current weather.
    """
    return f"{location}: {postcode}: cloudy with a 50% chance of rain"


MODEL = "gemini-2.0-flash"
CONFIG = types.GenerateContentConfig(
    temperature=1.0,
    # max_output_tokes=100,
    system_instruction="Consider the user's request, check your tools, find one that matches the count of data provided in the user's request, then call the matching tool.",
    tools=[get_current_weather, get_current_weather_with_postcode],
)


def main():
    cl = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    get_weather(cl, "What is the weather like in Shrewsberry, 23X57J Glandon?")
    get_weather(cl, "What is the weather like in Bukit Timah, Singapore?")


def get_weather(cl: genai.Client, prompt: str) -> None:
    print(f"Prompt: {prompt}")
    print(
        cl.models.generate_content(
            model=MODEL,
            config=CONFIG,
            contents=prompt,
        ).text
    )


if __name__ == "__main__":
    main()
