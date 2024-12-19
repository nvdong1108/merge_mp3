import time
import os
import re
import moviepy.editor as mp
from googletrans import Translator
from moviepy.config import change_settings
from moviepy.editor import ImageClip, AudioFileClip, TextClip, CompositeVideoClip # type: ignore
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
                start_time = float(parts[0])
                end_time = float(parts[1])
                text = parts[2]
                text_2 = parts[3]
                subtitles.append({"start": start_time
                                  , "end": end_time
                                  , "text_en":text
                                  , "text_vn": text_2})
    return subtitles


# if not os.path.exists(image_path):
#     raise FileNotFoundError(f"File picture not found: {image_path}")

# if not os.path.exists(audio_path):
#     raise FileNotFoundError(f"File audio not found: {audio_path}")



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

        end_time = subtitles[-1]['end'] 
        
        rows = 0.05
        for subtitle in subtitles:
            

            text_en = subtitle['text_en']
            text_vn = subtitle['text_vn']

            text_en_lines = text_en.splitlines()
            text_vn_lines = text_vn.splitlines()

            for text_line in text_en_lines:
                text_clip_en = TextClip(text_line, fontsize=40, color='white', font='Arial', method='caption', size=(screen_width * 0.5, None))
                text_clip_en = text_clip_en.set_position(('left', rows), relative=True).set_start(subtitle['start']).set_end(end_time)
                text_clips.append(text_clip_en)
                
                rows = rows + 0.05


            for text_line in text_vn_lines:
                text_clip_vn = TextClip(text_line, fontsize=40, color='yellow', font='Arial', method='caption', size=(screen_width * 0.5, None))
                text_clip_vn = text_clip_vn.set_position(('right', rows), relative=True).set_start(subtitle['start']).set_end(end_time)
                text_clips.append(text_clip_vn)


            if len(text_en) > 50 or len(text_vn) > 50:
                rows = rows + 0.05
            
            if re.search(r'[\n]',text_en) or re.search(r'[\n]',text_vn):
                rows = rows + 0.05                

        video = CompositeVideoClip([image_clip] + text_clips)
        video.write_videofile(output_path, fps=24, threads=4)

    finally:
        audio_clip.close()


def main():
    audio_folder = r"assets\test"
    image_path = r"assets\image\image_background.jpg"
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



# output_path = fr"assets\video_export\{unique_id}.mp4"  

# try:
#     audio_clip = AudioFileClip(audio_path)
#     duration = audio_clip.duration

#     image_clip = ImageClip(image_path).set_duration(duration)

#     screen_width = image_clip.size[0]
#     screen_height = image_clip.size[1]

#     image_clip = image_clip.set_audio(audio_clip)

#     text_clips = []
#     subtitles = load_subtitles()
    
    
#     for subtitle in subtitles:
#         text_clip_ja = TextClip(subtitle['text_en'], fontsize=50, color='white',font='Arial', method='caption',size=(screen_width * 0.5, None))
#         text_clip_ja = text_clip_ja.set_position(('left',0.1), relative=True).set_start(subtitle['start']).set_end(subtitle['end'])
#         text_clips.append(text_clip_ja)


#         text_clip_vn = TextClip(subtitle['text_vn'], fontsize=50, color='yellow', font='Arial', method='caption',size=(screen_width * 0.5, None))
#         text_clip_vn = text_clip_vn.set_position(('right',0.1), relative=True).set_start(subtitle['start']).set_end(subtitle['end'])
#         text_clips.append(text_clip_vn)

    
#     video = CompositeVideoClip([image_clip]+ text_clips)
#     video.write_videofile(output_path, fps=24, threads=4)

# finally:
#     audio_clip.close()

