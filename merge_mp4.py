import os
from moviepy.editor import VideoFileClip, concatenate_videoclips

def combine_videos(input_folder, output_file):
    """
    Combine all MP4 files in the input folder into a single video file.

    :param input_folder: Path to the folder containing MP4 files.
    :param output_file: Path to the output combined video file.
    """
    # Lấy danh sách tất cả các tệp MP4 trong thư mục
    video_files = [
        os.path.join(input_folder, f)
        for f in os.listdir(input_folder)
        if f.lower().endswith('.mp4')
    ]

    if not video_files:
        print("No MP4 files found in the folder.")
        return

    # Đọc từng video và thêm vào danh sách
    video_clips = []
    for video_file in sorted(video_files):  # Sắp xếp theo tên file
        print(f"Processing: {video_file}")
        clip = VideoFileClip(video_file)
        video_clips.append(clip)

    # Kiểm tra xem có audio trong các video không
    if not all(clip.audio for clip in video_clips):
        print("Warning: Some videos do not have audio tracks.")

    # Kết hợp tất cả các clip, đảm bảo xử lý audio chính xác
    combined_clip = concatenate_videoclips(video_clips, method="compose")

    # Xuất video kết hợp
    combined_clip.write_videofile(
        output_file,
        codec="libx264",
        audio_codec="aac",  # Codec âm thanh
        temp_audiofile="temp-audio.m4a",  # Tệp âm thanh tạm thời
        remove_temp=True,  # Xóa tệp tạm sau khi hoàn tất
    )

    # Đóng tất cả các clip để giải phóng bộ nhớ
    for clip in video_clips:
        clip.close()

    print(f"Combined video saved to {output_file}")

def main():
    input_folder = r"assets\save backup"
    output_folder = r"assets\video_export" 

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_file = os.path.join(output_folder, "combined_video.mp4")
    combine_videos(input_folder, output_file)

if __name__ == "__main__":
    main()
