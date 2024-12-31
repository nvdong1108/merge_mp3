

import nltk
from nltk.tokenize import sent_tokenize ,word_tokenize
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
        print(f"Đã ghi nội dung mới vào tệp: {file_path}")
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
    

def sub_word_to_file(segment):
    nltk.download('punkt_tab')

    sentences = sent_tokenize(segment)
    count = 0
    line1 = None
    line2  = ""
    tmp = ""

    if len(sentences) == 1:
        words = word_tokenize(sentence)
        for word in words:
            if line1 is None:
                tmp = tmp + words + ""
                count = count  + 1

                if re.search(r'[,]',word) or count > 40 :
                    if count > 15 and count < 40 or count > 40:
                        line1 = tmp
            else:
                line2 = line2 + words
    else:
        for sentence in sentences:
            words = word_tokenize(sentence)
            word_count = len([word for word in words if word.isalnum()]) 
            if line1 is None:
                count = count + word_count
                tmp = tmp +  sentence + ""
                # break_word = segment[-1]
            else:
                line2 = line2 +  sentence + ""

            if count > 15 and count < 40 and line1 is None:
                line1 = tmp

    print(f"line1: {line1}")                    
    print(f"line2: {line2}")                    
    return  line1 , line2 , count
    


def write_subtitle_to_file(subtitles,file_name):
    
    output_file = f"assets/subtitle/{file_name}.txt"

    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    try:
        with open(output_file, 'a', encoding='utf-8') as file:
            file.write(subtitles) 
    except Exception as e:
        print(f"An error occurred while writing subtitles: {e}")


def subtitels_all(audio_path , file_name):

    model = whisper.load_model("base")

    result = model.transcribe(audio_path, word_timestamps=True)
    start_time = None
    segment_samples = ""

    count_words = 0

    last_word_backup = []
    
    print(f"here")

    for  i,  segment in  enumerate(result['segments']):

        for word_info in segment['words']:   
            word = word_info['word']

            segment_samples += word+ ""
            last_word_backup.append(word_info)
            count_words += 1

            if start_time is None:
                start_time = word_info['start']

            if ( re.search(r'[.!?]',word) and count_words > 30 )    or (count_words > 30 and re.search(r'[,]',word)) or count_words > 47:

                line = f"{start_time:.2f} # {word_info['end']:.2f} # {segment_samples}\n"
                write_subtitle_to_file(line,file_name)
                segment_samples =""
                count_words = 0
                start_time = None
                    
                # if count_words > 30:
                #     if count_words > 47:

                #         line1, line2 , count = sub_word_to_file(segment_samples)
                #         word_new = last_word_backup[count]
                #         print(f"count_words: {count_words}")

                #         line = f"{start_time:.2f} # {word_new['end']:.2f} # {line1}\n"
                #         write_subtitle_to_file(line,file_name)

                #         segment_samples = line2
                #         count_words = 0
                #         start_time  = word_new['end']
                
                #     line = f"{start_time:.2f} # {word_info['end']:.2f} # {segment_samples}\n"
                #     write_subtitle_to_file(line,file_name)
                #     segment_samples =""
                #     count_words = 0
                #     start_time = None
                #     last_word_backup = []
                

    if segment_samples.strip():
        end_time = result['segments'][-1]['words'][-1]['end']
        line = f"{start_time:.2f} # {end_time:.2f} #  {segment_samples}\n"
        write_subtitle_to_file(line,file_name)

    return None, None


def main():
    folder_path = r"assets\audio\test\\" 
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' does not exist.")
        return
    
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith(".mp3"):
            audio_path = os.path.join(folder_path, file_name)
            file_name_without_extension = os.path.splitext(file_name)[0]
            subtitels_all(audio_path, file_name_without_extension) 

            print(f"Subtitle for {file_name} has been created.")


if __name__ == "__main__":
    main()    
    # text = "Parts were of nickel, parts of ivory, parts had certainly been filed or sawed out of rock crystal. The thing was generally complete, but the twisted crystalline bars lay unfinished upon the bench beside some sheets of drawings, and I took one up for a better look at it."
    # sub_word_to_file(text)