import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))


from pydub import AudioSegment
from gtts import gTTS
from tqdm import tqdm
from moviepy.config import change_settings
import os
import time
import uuid
import datetime
import json
from moviepy.editor import ImageClip, AudioFileClip, TextClip, CompositeVideoClip
from controller.common.file_untils import write_to_file, create_folder_new_project, convert_text_to_json
import ffmpeg
import subprocess
from flask_socketio import SocketIO


change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})



# class Content:
#     def __init__(self, es, en):
#         self.es = es
#         self.en = en

def read_text_file():
    with open('assets/text/book.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def file_name_uuid(i=0):
    date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = uuid.uuid4().hex[:8]
    i_str = str(i).zfill(2)
    return f"{date}_{i_str}_{file_name}"

def text_to_speech(content, output_folder):
    tts_es = gTTS(text=content['es'], lang='es', slow=False)
    file_name_es = file_name_uuid()

    path_es = os.path.join(output_folder, f"{file_name_es}.mp3")
    tts_es.save(path_es)

    tts_en_1 = gTTS(text=content['en'], lang='en', slow=False, tld='co.uk')
    file_name_en_1 = file_name_uuid()
    path_en_1 = os.path.join(output_folder, f"{file_name_en_1}.mp3")
    tts_en_1.save(path_en_1)


    tts_en_2 = gTTS(text=content['en'], lang='en', slow=True, tld='co.uk')
    file_name_en_2 = file_name_uuid()
    path_en_2 = os.path.join(output_folder, f"{file_name_en_2}.mp3")
    tts_en_2.save(path_en_2)

    tts_en_3 = gTTS(text=content['en'], lang='en', slow=False, tld='co.uk')
    file_name_en_3 = file_name_uuid()
    path_en_3 = os.path.join(output_folder, f"{file_name_en_3}.mp3")
    tts_en_3.save(path_en_3)

    audio_es = AudioSegment.from_mp3(path_es)
    audio_en_1 = AudioSegment.from_mp3(path_en_1)
    audio_en_2 = AudioSegment.from_mp3(path_en_2)
    audio_en_3 = AudioSegment.from_mp3(path_en_3)

    silence1 = AudioSegment.silent(duration=2000)
    silence_end = AudioSegment.silent(duration=3000)
    
    combined = audio_es + silence1 + audio_en_1 + silence1 + audio_en_2 + silence1 + audio_es + silence1 + audio_en_3 + silence_end

    final_file_name = file_name_uuid()
    final_path = os.path.join(output_folder, f"{final_file_name}.mp3")
    combined.export(final_path, format="mp3")

    os.remove(path_es)
    os.remove(path_en_1)
    os.remove(path_en_2)
    os.remove(path_en_3)

    return final_path
    

def create_videos(audio_path, image_path, sentence, files_videos_output):
    try:
        audio  = AudioFileClip(audio_path)   
        image_clip = ImageClip(image_path).set_duration(audio.duration)
        image_clip = image_clip.set_audio(audio)
        screen_width = image_clip.size[0]
        screen_height = image_clip.size[1]
        text_clips = []

        txt_clip_es = TextClip(sentence['es'], fontsize=60, color='red', font='Comic-Sans-MS'
                            ,method='caption', align='South', size=(screen_width*0.9, None))
        txt_clip_es = txt_clip_es.set_position(('center',0.1),relative=True).set_duration(audio.duration)

        txt_clip_en = TextClip(sentence['en'], fontsize=75, color='#48c290', font='Comic-Sans-MS'
                            ,method='caption', align='South', size=(screen_width*0.9, None))
        rows = round(txt_clip_es.h / screen_height, 2) + 0.1
        txt_clip_en = txt_clip_en.set_position(('center',rows),relative=True).set_duration(audio.duration)


        text_clips.append(txt_clip_es) 
        text_clips.append(txt_clip_en)
        

        video = CompositeVideoClip([image_clip] + text_clips)
        
        video.write_videofile(files_videos_output, fps=24, threads=4)
       

    except FileNotFoundError as e:
        print(f"Error: {e}")

    finally:
        audio.close()



def merge_videos(filelist, output_file):
    command = f"ffmpeg -f concat -safe 0 -i {filelist} -c copy {output_file}"
    subprocess.run(command, shell=True)

def test_(socketio):
    total = 10 
    for i in range(total):
        socketio.sleep(1)
        socketio.emit('progress', {'progress': i*10})    


def json_to_videos(content,socketio):
    image_path = r"assets\image\2.png"
    output_folder = create_folder_new_project()
    files_txt_name_videos = os.path.join(output_folder, "filelist.txt")
    total_sentences = len(content)
    for i,sentence in enumerate(tqdm(content, desc="Processing sentences", unit="sentence")):
        progress = int((i + 1) / total_sentences * 100)
        print(f"\n\n\n=================== >>>>> Progress {progress} ====================================\n\n")
        # socketio.emit('progress', {'progress': progress}, broadcast=True)
        path_audio = text_to_speech(sentence, output_folder)
        audio = AudioSegment.from_file(path_audio)
        file_name  =f"{file_name_uuid(i)}"

        files_audio_output = os.path.join(output_folder, f"{file_name}.mp3")
        audio.export(files_audio_output, format="mp3")
        
        # create audio done continute create videos
        files_videos_output = os.path.join(output_folder, f"{file_name}.mp4")
        create_videos(files_audio_output, image_path, sentence, files_videos_output)

        line_name_vides = f"file '{os.path.abspath(files_videos_output)}'\n"
        write_to_file(files_txt_name_videos, line_name_vides , False)

    # end file 
    line_name_vides = f"file 'D:\CODE\DONGNV\git\merge_mp3\static\common\the_end.mp4'\n"
    write_to_file(files_txt_name_videos, line_name_vides , False)

    files_result = os.path.join(output_folder, f"result_{file_name_uuid()}.mp4")
    merge_videos(files_txt_name_videos,files_result)
    
    print(f"Done: {files_result}")
    return files_result


def text_to_videos(text, socketio):
    # thực tết 
    json = convert_text_to_json(text)
    # socketio.emit('progress', {'progress': 1}, broadcast=True)
    # test_(socketio)
    path = json_to_videos(json,socketio)
    # socketio.emit('progress', {'progress': 100}, broadcast=True)

    print("\n\ndone===================================\n\n\n\n")
    return path
    # test 

    


if __name__ == "__main__":
    content = read_text_file()
    socketio = SocketIO()
    json_to_videos(content,socketio)

    

    


    

