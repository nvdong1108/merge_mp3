import os
import glob
from pydub import AudioSegment 
def read_mp3_files():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    
    audio_dir = os.path.join(script_dir, 'audio')
    
    mp3_files = glob.glob(os.path.join(audio_dir, '*.mp3'))
    
    for file in mp3_files:
        print(f"Processing file:: {os.path.basename(file)}")

    return mp3_files


def merge_mp3_files(mp3_files):

    combined = AudioSegment.from_mp3(mp3_files[0])


    for mp3_file in mp3_files[1:]:
        audio = AudioSegment.from_mp3(mp3_file)
        combined += audio
    

    output_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'merged_output.mp3')
    combined.export(output_file, format="mp3")
    print(f"File has been merged and saved at: {output_file}")



if __name__ == "__main__":
    mp3_files = read_mp3_files()
    if mp3_files:
        merge_mp3_files(mp3_files)
    else:
        print("No MP3 files found in the audio directory.")







