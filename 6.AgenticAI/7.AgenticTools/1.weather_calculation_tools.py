## Tools : In agentic systems, the LLM requests tools using IDs, developers execute them, and results are returned in the same message flow for safe and controlled reasoning.
# Tools execute real logic; the LLM only decides when to use them.
# The LLM never runs tools directly
# Message history must be preserved and hence tool results must be sent back in the same conversation thread.
# tool_call_id links intent to execution, every tool response must reference the exact tool call that requested it.
# Order of messages is strictly enforced. assistant(tool_calls) → tool(tool_call_id) → assistant(reasoning).

from openai import OpenAI
import json


# -------------------------------------------------
# 1. Tool: Weather Service (Non-AI, deterministic)
# -------------------------------------------------
def fetch_weather(city: str) -> dict:
    """
    Simulates a weather API.
    This represents real-world logic outside the LLM.
    """
    weather_data = {
        "Pune": {"temp_c": 32, "humidity": 55, "condition": "Sunny"},
        "Mumbai": {"temp_c": 30, "humidity": 78, "condition": "Humid"},
        "Delhi": {"temp_c": 38, "humidity": 40, "condition": "Hot"},
    }

    return weather_data.get(
        city,
        {"temp_c": 25, "humidity": 50, "condition": "Unknown"}
    )


# -------------------------------------------------
# 2. Tool Specification (What the LLM is allowed to use)
# -------------------------------------------------
WEATHER_TOOL = [
    {
        "type": "function",
        "function": {
            "name": "fetch_weather",
            "description": "Fetch current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"}
                },
                "required": ["city"]
            }
        }
    }
]


# -------------------------------------------------
# 3. Agent Logic (LLM + Tool Orchestration)
# -------------------------------------------------
def run_weather_agent(user_question: str) -> str:
    """
    Runs a single-turn agent:
    1. LLM decides whether a tool is needed
    2. Developer executes the tool
    3. Tool result is sent back to LLM
    4. LLM produces final answer
    """
    client = OpenAI()

    # Conversation memory (must be preserved)
    messages = [
        {"role": "system", "content": "You are a helpful weather assistant."},
        {"role": "user", "content": user_question}
    ]

    # Step 1: Let LLM decide if a tool is required
    first_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=WEATHER_TOOL,
        tool_choice="auto"
    )

    assistant_message = first_response.choices[0].message
    messages.append(assistant_message)

    # Step 2: If the LLM asked for a tool, execute it
    if assistant_message.tool_calls:
        tool_call = assistant_message.tool_calls[0]

        tool_arguments = json.loads(tool_call.function.arguments)
        weather_result = fetch_weather(**tool_arguments)

        # IMPORTANT:
        # tool_call_id links this tool response to the LLM's request
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(weather_result)
        })

        # Step 3: Ask LLM to reason over tool output
        final_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        return final_response.choices[0].message.content

    # If no tool was needed
    return assistant_message.content


# -------------------------------------------------
# 4. Program Entry Point
# -------------------------------------------------
if __name__ == "__main__":
    question = "What is the weather in Pune? Is it good for a morning walk?"
    result = run_weather_agent(question)

    print("\nWeather Agent Response:\n")
    print(result)
