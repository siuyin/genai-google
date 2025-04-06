from langchain_google_genai import ChatGoogleGenerativeAI
import os

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    api_key=os.getenv("GOOGLE_API_KEY"),
)
print("GOOGLE_API_KEY=****")


def main():
    # print(prompt(llm, "Weather : Bukit Timah, Singapore"))
    print(prompt(llm, "Weather : Gambu town, Gerterbbabbang"))
    # print(prompt(llm, "Weather forecast for Shewsberry GW5XP2, Glandon"))


from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

# messages = [SystemMessage(content="Keep your responses brief and to the point.")]
messages = [
    SystemMessage(
        content="""You are an entertainment AI that
tells interesting stories based on the weather.
You MUST start by providing the weather forecast by calling the appropriate tool(s) 
Then add some background on the place.
If you do not know, make up some fictional content.
then weave a story around the current weather.
Include a male protagonist and a female love interest
End with a disclaimer that your content is completely fictional purely for entertainment
"""
    )
]


def prompt(model, prompt: str) -> any:
    messages.append(HumanMessage(prompt))
    r = model.invoke(messages)
    messages.append(r)
    r = execute_tool_calls(model, r)
    return r.content


def execute_tool_calls(model, r) -> any:
    # print(r.tool_calls)
    if len(r.tool_calls) == 0:
        print("**************** no tools called")
        return r

    for tc in r.tool_calls:
        if tc["name"] == "weather":
            messages.append(
                ToolMessage(
                    tool_call_id=tc["id"], content=weather(tc["args"]["location"])
                )
            )
            r = model.invoke(messages)
            messages.append(r)
            continue
        if tc["name"] == "weatherWithPostcode":
            messages.append(
                ToolMessage(
                    tool_call_id=tc["id"],
                    content=weatherWithPostcode(
                        tc["args"]["location"], tc["args"]["postcode"]
                    ),
                )
            )
            r = model.invoke(messages)
            messages.append(r)
            continue

    return r


def weather(location: str) -> str:
    """weather returns the weather forecast for the given location.

    Args:
        location: a place name. eg. Bukit Jalil or Bukit Jalil, Kuala Lumpur, Malaysia.
    """
    return f"{location}: sunny, 50% chance rain."


def weatherWithPostcode(location: str, postcode: str) -> str:
    """weatherWithPostcode returns the weather for a given location and postcode.

    Args:
        location: a place name. eg. Bukit Jalil or Bukit Jalil, Kuala Lumpur, Malaysia.
        postcode: a location postcode. eg. 5GWLPW Glandon or Singapore 587967
    """
    return f"{location} {postcode}: rainy, 50% chance of sun."


llm = llm.bind_tools([weather, weatherWithPostcode])


if __name__ == "__main__":
    main()
