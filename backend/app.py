# backend/app.py
from flask import Flask, jsonify, request
from chatbot import Chatbot
import os
from flask_cors import CORS
import threading

app = Flask(__name__)
CORS(app)
chatbot = Chatbot()  # Instantiate your Chatbot class

# Define the path to the React build folder
react_build_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'build')

# Serve the static files from the React build folder
@app.route('/')
def index():
    return app.send_static_file(react_build_path + 'index.html')

@app.route('/api/pet', methods=['POST'])
def generate_meditation():
    data = request.json
    voice = data.get('voice')
    prompt = data.get('description')
        
    # Process the prompt using your chatbot
    answer = chatbot.answer(prompt)
    #answer = "test"

    # Turn the reponse into audio and then play it
    audio_thread = threading.Thread(target=play_audio_async, args=(answer, voice))
    audio_thread.start()

    # Render the index.html template with the response
    return jsonify({"petText": answer})

def play_audio_async(answer, voice="random"):
    # Turn the response into audio and then play it
    speech_file_path = chatbot.text_to_audio(answer, voice)
    chatbot.speak(speech_file_path)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
