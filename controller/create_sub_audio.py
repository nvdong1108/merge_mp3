
import datetime
import time
import os
import re
import uuid
import whisper
from googletrans import Translator
from pyannote.audio import Pipeline

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"


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


def subtitels_all(audio_path , file_name):

    model = whisper.load_model("base")


    # try:
    #     pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization", use_auth_token="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")
    #     diarization = pipeline(audio_path)
    # except Exception as e:
    #     print(f"Error when open audio file : {e}")    
    # print(f"\n#################\n\n")
    # speaker_segments = []
    # for turn, _, speaker in diarization.itertracks(yield_label=True):
    #     speaker_segments.append({
    #         "start": turn.start,
    #         "end": turn.end,
    #         "speaker": speaker
    #     })

    result = model.transcribe(audio_path, word_timestamps=True)
    start_time = None
    segment_samples = ""

    for  i,  segment in  enumerate(result['segments']):

        for word_info in segment['words']:   
            word = word_info['word']
            segment_samples += word+ ""

            if start_time is None:
                start_time = word_info['start']

            if re.search(r'[.!?]',word):

                if i == 0:
                    speaker = "title"
                elif re.search(r'[?]',word):
                    speaker = "Q"    
                else:
                    speaker = "A"
                    
                end_time = word_info['end']
                line = f"{speaker} # {start_time:.2f} # {end_time:.2f} # {segment_samples}\n"
                write_subtitle_to_file(line,file_name)
                segment_samples =""
                start_time = None


    if segment_samples.strip():
        end_time = result['segments'][-1]['words'][-1]['end']
        line = f"{start_time:.2f} # {end_time:.2f} #  {segment_samples} # {translate_text(segment_samples)}\n"
        write_subtitle_to_file(line,file_name)

    return None, None

def main():
    folder_path = r"assets\test\\" 
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