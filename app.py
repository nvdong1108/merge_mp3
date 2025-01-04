import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from flask import Flask, request, jsonify, render_template, send_from_directory
from gtts import gTTS
from controller.audio.text_to_speech import text_to_speech

app = Flask(__name__)

# Trang chính
@app.route('/')
def home():
    return render_template('index.html')



@app.route('/text-to-speech', methods=['POST'])
def post_text_to_speech():
    text = request.get_json()['text']
    path = text_to_speech(text)
    return jsonify({'url': f"http://127.0.0.1:8080/{path}"})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
