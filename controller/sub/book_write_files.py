
import time
import os
import re
import whisper
from googletrans import Translator

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["SB_LOCAL_STRATEGY"] = "copy"

def wrap_text(text, max_chars_per_line):
    """
    Chia text thành các dòng dựa trên số lượng ký tự tối đa trên mỗi dòng.
    
    Args:
        text (str): Chuỗi văn bản cần chia.
        max_chars_per_line (int): Số lượng ký tự tối đa mỗi dòng.

    Returns:
        str: Text đã được chia thành nhiều dòng.
    """
    words = text.split()  # Tách text thành danh sách từ
    lines = []
    current_line = []

    for word in words:
        # Nếu thêm từ vào dòng hiện tại vượt quá giới hạn, xuống dòng mới
        if sum(len(w) for w in current_line) + len(word) + len(current_line) > max_chars_per_line:
            lines.append(" ".join(current_line))
            current_line = [word]
        else:
            current_line.append(word)

    # Thêm dòng cuối cùng
    if current_line:
        lines.append(" ".join(current_line))

    # Kết hợp các dòng lại với ký tự xuống dòng
    return "\n".join(lines)



def load_subtitles(file_name):
    file_path = fr"assets\subtitle\{file_name}.txt"
    # print(f"================= >>>>>>  load_subtitles file_path: {file_path}")
    subtitles = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(" # ")
            if len(parts) > 2:
                # speaker = parts[0]
                start_time = float(parts[0].strip())
                end_time = float(parts[1].strip())
                text = parts[2].strip()
                subtitles.append({"start": start_time
                                  , "end": end_time
                                  , "text_en":text})
    return subtitles


def write_to_file(file_path, content):
    """
    Ghi nội dung mới vào tệp, xóa nội dung cũ trước khi ghi.
    
    Args:
        file_path (str): Đường dẫn đến tệp cần ghi.
        content (str): Nội dung cần ghi vào tệp.
    """
    try:
        # Mở tệp ở chế độ ghi (write mode), xóa nội dung cũ
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
    except Exception as e:
        print(f"Lỗi khi ghi tệp: {e}")




def translate_text(text , language="vi", retries=3, wait_time=1):
    if not text.strip():
        return text
    translator = Translator()
    for attempt in range(retries):
        try:
            translated = translator.translate(text, dest=language)
            if translated:
                return translated.text
        except Exception as e:
            print(f"Attempt {attempt+1}/{retries} failed: {str(e)}")
        if attempt < retries - 1:
            time.sleep(wait_time) 
            
    return text      


def load_audio_file(audio_path):
    try:
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"File audio not found: {audio_path}")
        # audio_clip = AudioFileClip(audio_path)
        return None

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None

    except Exception as e:
        print(f"Error when open audio file : {e}")
        return None
    


def write_subtitle_to_file(subtitles,file_name):
    
    output_file = f"assets/subtitle/{file_name}.txt"

    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    try:
        with open(output_file, 'a', encoding='utf-8') as file:
            file.write(subtitles) 
    except Exception as e:
        print(f"An error occurred while writing subtitles: {e}")



def main():
    file_name = "timemachinewells_01_ae_64kb" 
    

    output_folder = os.path.join("assets", "subtitle", "book", f"{file_name}")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    subtitles = load_subtitles(file_name)

    for i, subtitle in enumerate( subtitles):
        text = subtitle['text_en']
        wrapped_text = wrap_text(text, max_chars_per_line=50)
        # temp_file = f"{file_name}_{i}.txt"
        temp_file = os.path.join(output_folder, f"{file_name}_{i}.txt")
        write_to_file(temp_file, wrapped_text)
    
    print(f"write_to_file has been created.")
    print("=========================================")    
    

            

if __name__ == "__main__":
    main()    