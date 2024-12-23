# Create a Python project to merge MP3 files. #
1. install lib 
2. dowload ImageMagick download page 

# Step 1: Create a Python virtual environment (venv), and activate the venv.
# python -m venv venv
# venv\Scripts\activate


# Step 2: Install the necessary libraries and file
# fix bug : pip install audioop-lts
1. create file  main.py 
2. create folder  
3. copy the files you want to merge into the folder. 


# Step 3: create funcion read all MP3 files in  folder

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

# Step 4: process merge all MP3 files and export file

def merge_mp3_files(mp3_files):

    combined = AudioSegment.from_mp3(mp3_files[0])


    for mp3_file in mp3_files[1:]:
        audio = AudioSegment.from_mp3(mp3_file)
        combined += audio
    

    output_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'merged_output.mp3')
    combined.export(output_file, format="mp3")
    print(f"File has been merged and saved at: {output_file}")

# Step 5: create function main
    if __name__ == "__main__":
        mp3_files = read_mp3_files()
        if mp3_files:
            merge_mp3_files(mp3_files)
        else:
            print("No MP3 files found in the audio directory.")


# font  
fort ['Arial', 'Arial-Black', 'Arial-Bold', 'Arial-Bold-Italic', 'Arial-Italic', 'Bahnschrift', 'Calibri', 'Calibri-Bold', 'Calibri-Bold-Italic', 'Calibri-Italic', 'Calibri-Light', 'Calibri-Light-Italic', 'Cambria-&-Cambria-Math', 'Cambria-Bold', 'Cambria-Bold-Italic', 'Cambria-Italic', 'Candara', 'Candara-Bold', 'Candara-Bold-Italic', 'Candara-Italic', 
'Candara-Light', 'Candara-Light-Italic', 'Comic-Sans-MS', 'Comic-Sans-MS-Bold', 'Comic-Sans-MS-Bold-Italic', 'Comic-Sans-MS-Italic', 'Consolas', 'Consolas-Bold', 'Consolas-Bold-Italic', 'Consolas-Italic', 'Constantia', 'Constantia-Bold', 'Constantia-Bold-Italic', 'Constantia-Italic', 'Corbel', 'Corbel-Bold', 'Corbel-Bold-Italic', 'Corbel-Italic', 'Corbel-Light', 'Corbel-Light-Italic', 'Courier-New', 'Courier-New-Bold', 'Courier-New-Bold-Italic', 'Courier-New-Italic', 'Ebrima', 'Ebrima-Bold', 'Franklin-Gothic-Medium', 'Franklin-Gothic-Medium-Italic', 'Gabriola', 'Gadugi', 'Gadugi-Bold', 'Georgia', 'Georgia-Bold', 'Georgia-Bold-Italic', 'Georgia-Italic', 'Holo-MDL2-Assets', 'Impact', 'Ink-Free', 'Javanese-Text', 'Leelawadee-UI', 'Leelawadee-UI-Bold', 'Leelawadee-UI-Semilight', 'Lucida-Console', 'Lucida-Sans-Unicode', 'Malgun-Gothic', 'Malgun-Gothic-Bold', 'Malgun-Gothic-SemiLight', 'Microsoft-Himalaya', 'Microsoft-JhengHei-&-Microsoft-JhengHei-UI', 'Microsoft-JhengHei-Bold-&-Microsoft-JhengHei-UI-Bold', 'Microsoft-JhengHei-Light-&-Microsoft-JhengHei-UI-Light', 'Microsoft-New-Tai-Lue', 'Microsoft-New-Tai-Lue-Bold', 'Microsoft-PhagsPa', 'Microsoft-PhagsPa-Bold', 'Microsoft-Sans-Serif', 'Microsoft-Tai-Le', 'Microsoft-Tai-Le-Bold', 
'Microsoft-YaHei-&-Microsoft-YaHei-UI', 'Microsoft-YaHei-Bold-&-Microsoft-YaHei-UI-Bold', 'Microsoft-YaHei-Light-&-Microsoft-YaHei-UI-Light', 'Microsoft-Yi-Baiti', 'MingLiU-ExtB-&-PMingLiU-ExtB-&-MingLiU_HKSCS-ExtB', 'Mongolian-Baiti', 'MS-Gothic-&-MS-UI-Gothic-&-MS-PGothic', 'MV-Boli', 'Myanmar-Text', 'Myanmar-Text-Bold', 'Nirmala-UI', 'Nirmala-UI-Bold', 'Nirmala-UI-Semilight', 'Palatino-Linotype', 'Palatino-Linotype-Bold', 'Palatino-Linotype-Bold-Italic', 'Palatino-Linotype-Italic', 'Segoe-MDL2-Assets', 'Segoe-Print', 'Segoe-Print-Bold', 'Segoe-Script', 'Segoe-Script-Bold', 'Segoe-UI', 'Segoe-UI-Black', 'Segoe-UI-Black-Italic', 'Segoe-UI-Bold', 'Segoe-UI-Bold-Italic', 'Segoe-UI-Emoji', 'Segoe-UI-Historic', 'Segoe-UI-Italic', 'Segoe-UI-Light', 'Segoe-UI-Light-Italic', 'Segoe-UI-Semibold', 'Segoe-UI-Semibold-Italic', 'Segoe-UI-Semilight', 'Segoe-UI-Semilight-Italic', 'Segoe-UI-Symbol', 'SimSun-&-NSimSun', 'SimSun-ExtB', 'Sitka-Small-&-Sitka-Text-&-Sitka-Subheading-&-Sitka-Heading-&-Sitka-Display-&-Sitka-Banner', 'Sitka-Small-Bold-&-Sitka-Text-Bold-&-Sitka-Subheading-Bold-&-Sitka-Heading-Bold-&-Sitka-Display-Bold-&-Sitka-Banner-Bold', 'Sitka-Small-Bold-Italic-&-Sitka-Text-Bold-Italic-&-Sitka-Subheading-Bold-Italic-&-Sitka-Heading-Bold-Italic-&-Sitka-Display-Bold-Italic-&-Sitka-Banner-Bold-Italic', 'Sitka-Small-Italic-&-Sitka-Text-Italic-&-Sitka-Subheading-Italic-&-Sitka-Heading-Italic-&-Sitka-Display-Italic-&-Sitka-Banner-Italic', 'Sylfaen', 'Symbol', 'Tahoma', 'Tahoma-Bold', 'Times-New-Roman', 'Times-New-Roman-Bold', 'Times-New-Roman-Bold-Italic', 'Times-New-Roman-Italic', 'Trebuchet-MS', 'Trebuchet-MS-Bold', 'Trebuchet-MS-Bold-Italic', 'Trebuchet-MS-Italic', 'Verdana', 'Verdana-Bold', 'Verdana-Bold-Italic', 'Verdana-Italic', 'Webdings', 'Wingdings', 'Yu-Gothic-Bold-&-Yu-Gothic-UI-Semibold-&-Yu-Gothic-UI-Bold', 'Yu-Gothic-Light-&-Yu-Gothic-UI-Light', 'Yu-Gothic-Medium-&-Yu-Gothic-UI-Regular', 'Yu-Gothic-Regular-&-Yu-Gothic-UI-Semilight']