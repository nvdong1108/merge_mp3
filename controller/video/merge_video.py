import os
from moviepy.editor import VideoFileClip, concatenate_videoclips

# Đường dẫn đến thư mục chứa các video
video_folder = r'assets\video\merged\\'

# Lấy danh sách tất cả các file trong thư mục
video_files = [f for f in os.listdir(video_folder) if f.endswith('.mp4')]

# Tạo danh sách các clip video
video_clips = []

# Lặp qua tất cả các file video và thêm vào danh sách video_clips
for video_file in video_files:
    video_path = os.path.join(video_folder, video_file)
    video_clip = VideoFileClip(video_path)
    if video_clip.audio:
        video_clips.append(video_clip)
    else:
        # Nếu video không có âm thanh, thêm âm thanh từ video đầu tiên hoặc video trước đó
        video_clips.append(video_clip.set_audio(video_clip.audio))
    # video_clips.append(video_clip)

# Ghép tất cả video lại
final_video = concatenate_videoclips(video_clips)

# Xuất video đã ghép
final_video.write_videofile(os.path.join(video_folder, "merged_output.mp4"), codec="libx264", audio_codec="aac")
