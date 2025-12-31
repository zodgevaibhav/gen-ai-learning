from openai import OpenAI

client = OpenAI()

def call_llm(system_prompt: str, user_input: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0.1 # Low temperature for more deterministic responses meaning less randomness
    )
    return response.choices[0].message.content
