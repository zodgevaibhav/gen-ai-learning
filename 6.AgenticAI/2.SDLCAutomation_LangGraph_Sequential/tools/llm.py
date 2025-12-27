from openai import OpenAI
import subprocess
from langchain_ollama import OllamaLLM
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

client = OpenAI()
useLocal = True

def call_llm(system_prompt: str, user_input: str) -> str:
    if useLocal:
        return call_local_llm_ollama(system_prompt, user_input)
    else:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.1  # Low temperature for more deterministic responses meaning less randomness
        )
        return response.choices[0].message.content


def call_local_llm_ollama(system_prompt: str, user_input: str) -> str:
    """
    Call a local Ollama LLM via LangChain using the llama3 model.
    Only accepts system_prompt and user_input.
    """
    llm = OllamaLLM(model="llama3", max_tokens=1000)
    messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_input)]
    response = llm.invoke(messages)
    return response
