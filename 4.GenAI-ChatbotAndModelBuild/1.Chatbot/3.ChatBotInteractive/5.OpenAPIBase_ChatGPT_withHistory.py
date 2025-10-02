from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import base64
import os
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_text(prompt):
    """Generate text using GPT-4o-mini."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )
    return response.choices[0].message.content

def generate_image(prompt):
    """Generate image using DALL·E."""
    response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024"
    )
    print(response.data[0])
    return response.data[0].url

def generate_audio(prompt):
    """Generate audio (TTS) and return static file path."""
    os.makedirs("static", exist_ok=True)
    filename = "static/output.mp3"
    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=prompt
    )
    response.stream_to_file(filename)
    return filename

def generate_video(prompt):
    """Stubbed video generator (replace with real API if available)."""
    # For demo, we can just return a placeholder video path
    os.makedirs("static", exist_ok=True)
    return "static/sample_video.mp4"  # Put a sample mp4 in static folder

# ---- Routes ---- #

@app.route('/', methods=['GET'])
def index():
    return render_template('chatgpt.html')  # The HTML we created

@app.route('/generate', methods=['POST'])
def generate():
    """
    Accept JSON with { "prompt": "...", "type": "text|image|audio|video" }
    """
    data = request.get_json()
    prompt = data.get("prompt", "").strip()
    gen_type = data.get("type", "text")

    if not prompt:
        return jsonify({"error": "Prompt required"}), 400

    try:
        if gen_type == "text":
            result = generate_text(prompt)
        elif gen_type == "image":
            result = generate_image(prompt)
        elif gen_type == "audio":
            result = generate_audio(prompt)
        elif gen_type == "video":
            result = generate_video(prompt)
        else:
            return jsonify({"error": "Invalid type"}), 400

        return jsonify({"result": result})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5400, debug=True)
