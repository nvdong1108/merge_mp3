from gtts import gTTS
from tqdm import tqdm
import os
import uuid
import datetime


def read_text_file():
    with open('assets/text/book.txt', 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def file_name_uuid():
    date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = uuid.uuid4().hex[:8]
    return f"{date}_{file_name}.mp3"

def text_to_speech(content):
    tts = gTTS(text=content, lang='en', slow=False, tld='co.uk')
    file_name = file_name_uuid()
    path = os.path.join("static", "audio", "gtts")
    path = os.path.join(path, f"{file_name}")
    tts.save(path)
    return path

if __name__ == "__main__":
    content = read_text_file()
    text_to_speech(content)
    # file_name = file_name_uuid()
    # print(f"file_name: {file_name}")
