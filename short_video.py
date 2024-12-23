import time
import os
import re
import moviepy.editor as mp
from googletrans import Translator
from moviepy.config import change_settings
from moviepy.editor import ImageClip, AudioFileClip, TextClip, CompositeVideoClip # type: ignore
from moviepy.video.fx import fadein, fadeout

change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})

def load_subtitles(file_name):
    file_path = fr"assets\subtitle\{file_name}.txt"
    subtitles = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(" # ")
            if len(parts) == 4:
                start_time = float(parts[0])
                end_time = float(parts[1])
                text = parts[2]
                text_2 = parts[3]
                subtitles.append({"start": start_time
                                  , "end": end_time
                                  , "text_en":text
                                  , "text_vn": text_2})
    return subtitles


def process_video(audio_path, image_path, output_folder, file_name):
    output_path = fr"{output_folder}\{file_name}.mp4"

    try:
        audio_clip = AudioFileClip(audio_path)
        duration = audio_clip.duration

        image_clip = ImageClip(image_path).set_duration(duration)

        screen_width = image_clip.size[0]
        screen_height = image_clip.size[1]

        image_clip = image_clip.set_audio(audio_clip)

        text_clips = []
        subtitles = load_subtitles(file_name)

        end_all_video_time = subtitles[-1]['end'] 
        
        rows = 0
        rows_pixes = 0   
        width_pixes = 0 
        width_persent = 0   
        text_en = ""

        space_two_line = 0.02
        
        

        for i, subtitle in enumerate( subtitles):
            
            text_en = subtitle['text_en']
            text_vn = subtitle['text_en']

            start_time = subtitle['start']
            if i == 0:
                # title
                text_clip_en = TextClip(text_en, fontsize=90, color='#ade02f', font='Comic-Sans-MS-Bold', method='caption', align='North', size=((screen_width*0.6), None))
                text_clip_en = text_clip_en.set_position(('center',rows),relative=True).set_start(0).set_end(end_all_video_time)
                
                rows_pixes += text_clip_en.h
                rows = round(rows_pixes / screen_height, 3) + space_two_line

            elif i % 2 == 1:   
                # left 
                text_clip_en = TextClip(text_en, fontsize=60, color='#eedfd8', font='Comic-Sans-MS', align='west')
                text_clip_en = text_clip_en.set_position((0.02, rows), relative=True).set_start(start_time).set_end(end_all_video_time)
                
                width_persent  = round(text_clip_en.w / screen_width ,3)
                print(f" width = {width_persent}")
           
            else:    
                # right
                text_clip_en = TextClip(text_en, fontsize=50, color='#eb8ee4'
                                        , font='Comic-Sans-MS-Italic', align='West'
                                        , method='caption', size=(screen_width*0.96, None))

                width_persent = width_persent + 0.1
                text_clip_en = text_clip_en.set_position((width_persent, rows), relative=True).set_start(start_time).set_end(end_all_video_time)
                
                rows_pixes += text_clip_en.h
                rows = round(rows_pixes / screen_height, 3) + space_two_line
            
            
            text_clips.append(text_clip_en)

        video = CompositeVideoClip([image_clip] + text_clips)
        video.write_videofile(output_path, fps=24, threads=4)

    finally:
        audio_clip.close()


def main():
    audio_folder = r"assets\test"
    image_path = r"assets\image\background_4.jpg"
    output_folder = r"assets\video_export" 

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for audio_file in os.listdir(audio_folder):
        if audio_file.lower().endswith(".mp3"):
            audio_path = os.path.join(audio_folder, audio_file)
            file_name = os.path.splitext(audio_file)[0] 
            process_video(audio_path, image_path, output_folder, file_name)

if __name__ == "__main__":
    main()

