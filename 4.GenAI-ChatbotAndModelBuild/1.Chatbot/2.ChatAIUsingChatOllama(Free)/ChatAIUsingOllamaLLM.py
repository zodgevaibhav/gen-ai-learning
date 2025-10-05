from langchain_ollama import OllamaLLM

# Pull Model
# Model Run
# REST API
llm = OllamaLLM(
    model="llama3",
    max_tokens=100
)
prompt = "What is the capital of France?"
# Call the Ollama API
response = llm.invoke(prompt)
print(response)

prompt = "Previous Response : "+response+", What is good in it ? "
# Call the Ollama API
response = llm.invoke(prompt)
print(response)