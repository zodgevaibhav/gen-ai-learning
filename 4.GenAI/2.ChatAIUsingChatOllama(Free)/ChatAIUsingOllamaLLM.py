from langchain_ollama import OllamaLLM

llm = OllamaLLM(
    model="llama3",
    max_tokens=100
)
prompt = "What is the capital of France?"
# Call the Ollama API
response = llm.invoke(prompt)
print(response)