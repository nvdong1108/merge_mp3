import sys
import os
from flask_socketio import SocketIO
import time
from flask_cors import CORS
from threading import Thread, Semaphore

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_socketio import SocketIO, emit
from gtts import gTTS
from controller.audio.text_to_speech import text_to_videos
from flask import Flask, request, jsonify

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="http://localhost:5000",async_mode="eventlet")

# socketio = SocketIO(app)
# socketio = SocketIO(app, cors_allowed_origins="*")  
# CORS(app, resources={r"/*": {"origins": "*"}})
# 
MAX_TASKS = 3
task_semaphore = Semaphore(MAX_TASKS)



# Trang chính
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/text-to-speech')
def text_to_speech():
    return render_template('index.html')


@app.route('/short-videos')
def short_videos():
    return render_template('short-videos.html')


@app.route('/templates/<path:filename>')
def serve_template_files(filename):
    return send_from_directory('templates', filename)


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


# def watch_folder():
#     previous_files = set(list_files(folder_path))
#     while True:
#         time.sleep(1)  # Kiểm tra thư mục mỗi giây
#         current_files = set(list_files(folder_path))
#         if current_files != previous_files:
#             added = current_files - previous_files
#             removed = previous_files - current_files
#             previous_files = current_files
#             # Gửi thông tin thay đổi qua WebSocket
#             socketio.emit('file_update', {
#                 'added': list(added),
#                 'removed': list(removed),
#                 'current': list(current_files)
#             })

# threading.Thread(target=watch_folder, daemon=True).start()



# @app.route('/files')
# def list_files():
#     folder_path = './static/project_videos/'  
#     try:
#         files = list_files_recursive(folder_path)
#         return jsonify(files)
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


def process_videos(text, socketio):
    with task_semaphore: 
        try:
            text_to_videos(text, socketio)
        except Exception as e:
            print(f"Error during video processing: {e}")



@app.route('/text-to-speech', methods=['POST'])
def post_text_to_speech():

    if task_semaphore._value == 0:  
        return jsonify({"message": "Server is busy, please wait for a slot."}), 429
    
    text = request.get_json()['text']
    Thread(target=process_videos, args=(text, socketio)).start()

    return jsonify({"message": f"Video processing started Thread {task_semaphore._value}!"})
    


@app.route('/list-assist-files', methods=['GET'])
def list_assist_files():
    file_list = []
    for root, dirs, files in os.walk('assist'):  # Duyệt toàn bộ thư mục assist
        for file in files:
            relative_path = os.path.relpath(os.path.join(root, file), 'assist')
            file_list.append(relative_path)
    return jsonify(file_list)


@app.route('/assist/<path:filename>')
def serve_assist_file(filename):
    return send_from_directory('assist', filename)



if __name__ == '__main__':
    # app.run(debug=True, host='127.0.0.1', port=5000)
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
