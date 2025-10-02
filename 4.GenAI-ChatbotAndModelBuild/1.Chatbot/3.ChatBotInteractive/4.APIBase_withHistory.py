from flask import Flask, request, jsonify, render_template
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage


llm = ChatOllama(
    model="llama3",
    max_tokens=100
)

messages = []

app = Flask(__name__)

def root():
    return render_template('index.html')

@app.route('/', methods=['GET'])
def index():
    return root()


@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')
    
    # Here you would typically call your LLM model to get a response
    # For demonstration, we'll just echo the user message
    print("******** User message : "+user_message)
    return jsonify({'response': getChatResponse(user_message)})



def getChatResponse(prompt):
    messages.append(HumanMessage(prompt)) # The user message is added to the history so that the model can use it to generate a more relevant response to the next user input
    response = llm.invoke(messages)
    messages.append(AIMessage(response.content)) # The AI message is added to the history so that the model can use it to generate a more relevant response to the next user input.
    return response.content



app.run(host="0.0.0.0", port=5400, debug=True)


