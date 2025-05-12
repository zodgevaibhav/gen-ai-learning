# Import required libraries
import os 
from langchain_openai import ChatOpenAI

# Create object of ChatOpenAI to access OpenAI API
llm = ChatOpenAI(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o",
    max_tokens=6,
)

prompt = "What is the capital of France?"

# Call the OpenAI API
response = llm.invoke(prompt)
print(response.content)
