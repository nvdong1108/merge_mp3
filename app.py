import sys
import os
from flask_socketio import SocketIO
import time

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import threading
from flask import Flask, request, jsonify, render_template, send_from_directory
from gtts import gTTS
from controller.audio.text_to_speech import text_to_speech

app = Flask(__name__)

socketio = SocketIO(app, cors_allowed_origins="*")  # Cho phép mọi origin kết nối WebSocket


# Trang chính
@app.route('/')
def home():
    return render_template('index.html')

def list_files_recursive(folder_path):
    file_list = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            relative_path = os.path.relpath(os.path.join(root, file), folder_path)
            file_list.append(relative_path)
    return file_list


def list_files(folder_path):
    try:
        return [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    except Exception as e:
        return []
    
folder_path = './static/project_videos/'


def watch_folder():
    previous_files = set(list_files(folder_path))
    while True:
        time.sleep(1)  # Kiểm tra thư mục mỗi giây
        current_files = set(list_files(folder_path))
        if current_files != previous_files:
            added = current_files - previous_files
            removed = previous_files - current_files
            previous_files = current_files
            # Gửi thông tin thay đổi qua WebSocket
            socketio.emit('file_update', {
                'added': list(added),
                'removed': list(removed),
                'current': list(current_files)
            })

threading.Thread(target=watch_folder, daemon=True).start()



@app.route('/files')
def list_files():
    folder_path = './static/project_videos/'  
    try:
        files = list_files_recursive(folder_path)
        return jsonify(files)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/text-to-speech', methods=['POST'])
def post_text_to_speech():
    text = request.get_json()['text']
    path = text_to_speech(text)
    return jsonify({'url': f"http://127.0.0.1:5000/{path}"})


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
