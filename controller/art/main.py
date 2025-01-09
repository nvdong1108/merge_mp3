import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from moviepy.config import change_settings
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import *
from gtts import gTTS
import os


change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})


def create_video_with_typing_effect(image_path, text, output_path, duration_per_char=0.2):
    # Load hình nền
    background = ImageClip(image_path, duration=len(text) * duration_per_char)
    screen_width = background.size[0]
    screen_hight = background.size[1]
    # Hàm hiển thị từng chữ
    def make_text_clip(char_index):
        current_text = text[:char_index + 1]  # Lấy text từ đầu đến char_index
        text_clip = TextClip(current_text, fontsize=80, color="white", font="Arial", align="North", method="caption",size=(screen_width, screen_hight*0.5))
        text_clip = text_clip.set_position(("center",0.3), relative=True).set_duration(duration_per_char)
        return text_clip

    # Tạo danh sách các đoạn clip cho từng chữ
    text_clips = [make_text_clip(i) for i in range(len(text))]

    # Nối các clip text lại thành một clip
    typing_effect = concatenate_videoclips(text_clips)

    # Chèn typing_effect vào nền
    final_video = CompositeVideoClip([background, typing_effect])

    # Xuất video
    final_video.write_videofile(output_path, fps=24)


def generate_audio(text, output_path):
    tts = gTTS(text)
    tts.save(output_path)

def run():

    image_path = "assets/image/typing.png"  # Tấm hình màn hình điện thoại
    output_video = "assets/typing_effect.mp4"  # Tên video đầu ra
    output_audio = "assets/audio.mp3"  # Tên file âm thanh
    text_to_type = "Where are you from?"  # Câu tiếng Anh
    font_path = "arial.ttf"  # Đường dẫn đến font chữ
    font_size = 90  # Kích thước chữ
    tts = gTTS(text_to_type, lang="en")
    tts.save(output_audio)


    frames = []
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, font_size)


    x, y = 100, 300  # Vị trí bắt đầu in chữ
    current_text = ""
    frame_duration = 0.2  # Thời gian mỗi khung (giây)

    for char in text_to_type:
        current_text += char
        img_copy = image.copy()
        draw = ImageDraw.Draw(img_copy)
        draw.text((x, y), current_text, font=font, fill="black")  # Vẽ từng ký tự
        frames.append(img_copy)

    frame_files = []
    for i, frame in enumerate(frames):
        frame_file = f"frame_{i}.png"
        frame.save(frame_file)
        frame_files.append(frame_file)

    clips = [ImageClip(f).set_duration(frame_duration) for f in frame_files]
    video = concatenate_videoclips(clips, method="compose")


    audio = AudioFileClip(output_audio)
    final_video = video.set_audio(audio)
    final_video.write_videofile(output_video, fps=24)
        

if __name__ == "__main__":

    image_path = "assets/image/typing.png"  
    text = "Where are you from?"          
    video_output = "assets/output_video.mp4"
    audio_output = "assets/output_audio.mp3"

    generate_audio(text, audio_output)

    create_video_with_typing_effect(image_path, text, video_output)

    final_clip = VideoFileClip(video_output).set_audio(AudioFileClip(audio_output))
    final_clip.write_videofile("final_output.mp4", fps=24)