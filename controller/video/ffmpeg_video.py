import ffmpeg
import os


def load_subtitles(file_name):
    file_path = fr"assets\subtitle\{file_name}.txt"
    subtitles = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(" # ")
            if len(parts) > 0:
                # speaker = parts[0]
                start_time = float(parts[0])
                end_time = float(parts[1])
                text = parts[2]
                subtitles.append({"start": start_time
                                  , "end": end_time
                                  , "text_en":text})
    return subtitles




def create_video_from_image(audio_path, image_path, output_folder, file_name):
    output_path = os.path.join(output_folder, f"{file_name}.mp4")

    # Lấy độ dài của audio
    audio_info = ffmpeg.probe(audio_path, v='error', select_streams='a:0', show_entries='stream=duration')
    duration = float(audio_info['streams'][0]['duration'])

    # audio_info = ffmpeg.probe(audio_path, v='error', select_streams='a:0', show_entries='stream=duration')
    # duration = float(audio_info['streams'][0]['duration'])

    # Tạo video từ ảnh với độ dài của âm thanh
    # ffmpeg.input(image_path, loop=1, t=duration).output(output_path, vcodec='libx264', acodec='aac', audio=audio_path, pix_fmt='yuv420p').run()
    ffmpeg.input(image_path, loop=1, t=duration).input(audio_path).output(output_path, vcodec='libx264', acodec='aac', pix_fmt='yuv420p').run()
    print(f"handle audio and image done")
    # Thêm văn bản (subtitles)
    subtitles = load_subtitles(file_name)
    for subtitle in subtitles:
        start_time = subtitle['start']
        end_time = subtitle['end']
        text = subtitle['text_en']
        
        ffmpeg.input(output_path).output(output_path, vf=f"drawtext=text='{text}':fontfile=/path/to/Comic-Sans-MS-Bold.ttf:fontsize=70:fontcolor=yellow:x=(w-text_w)/2:y=(h-text_h)/10:enable='between(t,{start_time},{end_time})'").run()
        ffmpeg.input(output_path).output(output_path, vf=f"drawtext=text='{text}':fontfile=/path/to/Comic-Sans-MS-Bold.ttf:fontsize=70:fontcolor=yellow:x=(w-text_w)/2:y=(h-text_h)/10:enable='between(t,{start_time},{end_time})'").run()

    print(f"Video đã được tạo tại: {output_path}")


def main():
    audio_folder = r"assets\audio\test\\"
    image_path = r"assets\image\img_padcast.jpg"
    output_folder = r"assets\video\output_ffmpeg\\" 

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for audio_file in os.listdir(audio_folder):
        if audio_file.lower().endswith(".mp3"):
            audio_path = os.path.join(audio_folder, audio_file)
            file_name = os.path.splitext(audio_file)[0] 
            print(f"process audio file: {file_name}" )
            create_video_from_image(audio_path, image_path, output_folder, file_name)

if __name__ == "__main__":
    main()
