
import os
import uuid
from datetime import datetime
import moviepy.editor as mp
from moviepy.config import change_settings

from moviepy.editor import ImageClip, AudioFileClip, TextClip, CompositeVideoClip

change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
unique_id = uuid.uuid4()


image_path = r"assets\image.jpg"
# audio_path = r"assets\audio.mp3"
audio_path = r"assets\01-at-home.mp3"
# script_path = "script.txt"
output_video = "podcast_video.mp4"

# with open(script_path, "r", encoding="utf-8") as f:
#     script = f.read()


def load_subtitles():
    file_path = r"assets\subtitles_.txt"
    subtitles = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(" # ")
            if len(parts) == 3:
                start_time = float(parts[0])
                end_time = float(parts[1])
                text = parts[2]
                subtitles.append({"start": start_time, "end": end_time, "text": text})
    return subtitles


if not os.path.exists(image_path):
    raise FileNotFoundError(f"File ảnh không tồn tại: {image_path}")

if not os.path.exists(audio_path):
    raise FileNotFoundError(f"File audio không tồn tại: {audio_path}")


output_path =  f"output_{unique_id}.mp4"

try:
    audio_clip = AudioFileClip(audio_path)
    duration = audio_clip.duration

    image_clip = ImageClip(image_path).set_duration(duration)
    image_clip = image_clip.set_audio(audio_clip)

    text_clips = []
    subtitles = load_subtitles()
    
    
    for subtitle in subtitles:
        text_clip = TextClip(subtitle['text'], fontsize=13, color='white',method='label')
        width, height = text_clip.size
        # text_clip = text_clip.resize(width=width * 0.6)

        text_clip = text_clip.set_position((0.05,0.2), relative=True).set_start(subtitle['start']).set_end(subtitle['end'])
        text_clips.append(text_clip)
    print("============== > go")
    video = CompositeVideoClip([image_clip]+ text_clips)
    video.write_videofile(output_path, fps=24, threads=4)

finally:
    audio_clip.close()

