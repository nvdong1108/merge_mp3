import time
import os
import re
import moviepy.editor as mp
from googletrans import Translator
from moviepy.config import change_settings
from moviepy.editor import ImageClip, AudioFileClip, TextClip, CompositeVideoClip # type: ignore
from moviepy.video.fx import fadein, fadeout

change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})

# timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
# unique_id = uuid.uuid4()


# image_path = r"assets\image.jpg"
# audio_path = r"assets\01-at-home.mp3"

def load_subtitles(file_name):
    file_path = fr"assets\subtitle\{file_name}.txt"
    subtitles = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(" # ")
            if len(parts) == 4:
                speaker = parts[0]
                start_time = float(parts[1])
                end_time = float(parts[2])
                text = parts[3]
                subtitles.append({
                                  "speaker": speaker
                                  ,"start": start_time
                                  , "end": end_time
                                  , "text_en":text})
    return subtitles


def process():
     for i, subtitle in enumerate( subtitles):

            text_en = subtitle['text_en']
            # print(f"start_time: {subtitle['start']} end time: {end_all_video_time}") 
            if i == 0:
                # title 
                text_clip_en = TextClip(text_en, fontsize=90, color='#d1d155',font='Comic-Sans-MS-Bold', method='caption',size=(screen_width, None))
                text_clip_en = text_clip_en.set_position(('center',rows),relative=True).set_start(0).set_end(end_all_video_time)

            else:

                if subtitle['speaker'] == "Q":
                    # rows = rows + space_line
                    text_clip_en = TextClip(text_en, fontsize=55, color='white',font='Comic-Sans-MS', method='caption', align='West',size=(screen_width*0.99, None))
                    text_clip_en = text_clip_en.set_position(('left',rows),relative=True).set_start(subtitle['start']).set_end(subtitle['end'])
                else:
                    text_clip_en = TextClip(text_en, fontsize=55, color='#d2aedb',font='Comic-Sans-MS-Italic', method='caption', align='East',size=(screen_width*0.99 , None))
                    text_clip_en = text_clip_en.set_position(('right',rows),relative=True).set_start(subtitle['start']).set_end(subtitle['end'])
                # answer
                

            rows = round((rows + (text_clip_en.h / screen_height) ) ,2)
            print(f"rows = {rows} {text_en}")
            text_clips.append(text_clip_en)
            if rows > 0.88:
                rows = 0.1

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
        name_speaker = None

        
        rows = 0.02
        end_time_title = subtitles[-1]['end']   
        end_time_screen = subtitles[-1]['end'] 

        text_en = ""
        #  run draft
        for i, subtitle in enumerate( subtitles):
            if i == 0:
                text_clip_en = TextClip(subtitle['text_en'], fontsize=90, color='#d1d155',font='Comic-Sans-MS-Bold', method='caption',size=(screen_width, None))
                text_clip_en = text_clip_en.set_position(('center',rows),relative=True).set_start(0).set_end(end_time_title)
            else:
                if name_speaker is None:
                    name_speaker = subtitle['speaker']

                if subtitle['speaker'] == name_speaker:
                    text_clip_en = TextClip(subtitle['text_en'], fontsize=55, color='white',font='Comic-Sans-MS', method='caption', align='West',size=(screen_width*0.99, None))
                    text_clip_en = text_clip_en.set_position(('left',rows),relative=True).set_start(subtitle['start']).set_end(subtitle['end'])
                else:
                    text_clip_en = TextClip(subtitle['text_en'], fontsize=55, color='#d2aedb',font='Comic-Sans-MS-Italic', method='caption', align='East',size=(screen_width*0.99 , None))
                    text_clip_en = text_clip_en.set_position(('right',rows),relative=True).set_start(subtitle['start']).set_end(subtitle['end'])

            rows = round((rows + (text_clip_en.h / screen_height) ) ,2)
            # text_clips.append(text_clip_en)
            if rows >= 0.89:
                rows = 0.09
                end_time_screen = subtitle['end']
        
        #  run final
        text_clips = []
        
        rows = 0.02
        for i, subtitle in enumerate( subtitles):
            if i == 0:
                text_clip_en = TextClip(subtitle['text_en'], fontsize=90, color='#d1d155',font='Comic-Sans-MS-Bold', method='caption',size=(screen_width, None))
                text_clip_en = text_clip_en.set_position(('center',rows),relative=True).set_start(0).set_end(end_time_title)
            else:
                end_time = subtitle['end']
                # print(f"end_time_screen {end_time_screen} and end_time {end_time}")
                if end_time <= end_time_screen:
                     end_time = end_time_screen
                else:
                    end_time = end_time_title
                # print(f"\n --------->>>>> end_time_screen {end_time_screen} and end_time {end_time}\n")

                if subtitle['speaker'] == name_speaker:
                    text_clip_en = TextClip(subtitle['text_en'], fontsize=55, color='white',font='Comic-Sans-MS', method='caption', align='West',size=(screen_width*0.99, None))
                    text_clip_en = text_clip_en.set_position(('left',rows),relative=True).set_start(subtitle['start']).set_end(end_time)
                else:
                    text_clip_en = TextClip(subtitle['text_en'], fontsize=55, color='#fcc1de',font='Comic-Sans-MS-Italic', method='caption', align='East',size=(screen_width*0.99 , None))
                    text_clip_en = text_clip_en.set_position(('right',rows),relative=True).set_start(subtitle['start']).set_end(end_time)

            rows = round((rows + (text_clip_en.h / screen_height) ) ,2)
            # print(f"rows = {rows} {subtitle['text_en']}")
            text_clips.append(text_clip_en)
            if rows >= 0.89:
                rows = 0.09        


        video = CompositeVideoClip([image_clip] + text_clips)
        video.write_videofile(output_path, fps=24, threads=4)

    finally:
        audio_clip.close()


def main():
    audio_folder = r"assets\audio\test\\"
    image_path = r"assets\image\short_youtube.jpg"
    output_folder = r"assets\video\output\\" 

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for audio_file in os.listdir(audio_folder):
        if audio_file.lower().endswith(".wav"):
            audio_path = os.path.join(audio_folder, audio_file)
            file_name = os.path.splitext(audio_file)[0] 
            process_video(audio_path, image_path, output_folder, file_name)

if __name__ == "__main__":
    main()




