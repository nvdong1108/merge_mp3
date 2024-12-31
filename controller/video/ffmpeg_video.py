import subprocess
import os
import matplotlib.font_manager as fm



def wrap_text(text, max_chars_per_line):
    """
    Chia text thành các dòng dựa trên số lượng ký tự tối đa trên mỗi dòng.
    
    Args:
        text (str): Chuỗi văn bản cần chia.
        max_chars_per_line (int): Số lượng ký tự tối đa mỗi dòng.

    Returns:
        str: Text đã được chia thành nhiều dòng.
    """
    words = text.split()  # Tách text thành danh sách từ
    lines = []
    current_line = []

    for word in words:
        # Nếu thêm từ vào dòng hiện tại vượt quá giới hạn, xuống dòng mới
        if sum(len(w) for w in current_line) + len(word) + len(current_line) > max_chars_per_line:
            lines.append(" ".join(current_line))
            current_line = [word]
        else:
            current_line.append(word)

    # Thêm dòng cuối cùng
    if current_line:
        lines.append(" ".join(current_line))

    # Kết hợp các dòng lại với ký tự xuống dòng
    return "\n".join(lines)



def write_to_file(file_path, content):
    """
    Ghi nội dung mới vào tệp, xóa nội dung cũ trước khi ghi.
    
    Args:
        file_path (str): Đường dẫn đến tệp cần ghi.
        content (str): Nội dung cần ghi vào tệp.
    """
    try:
        # Mở tệp ở chế độ ghi (write mode), xóa nội dung cũ
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Đã ghi nội dung mới vào tệp: {file_path}")
    except Exception as e:
        print(f"Lỗi khi ghi tệp: {e}")



def load_subtitles(file_name):
    file_path = fr"assets\subtitle\{file_name}.txt"
    # print(f"================= >>>>>>  load_subtitles file_path: {file_path}")
    subtitles = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(" # ")
            if len(parts) > 2:
                # speaker = parts[0]
                start_time = float(parts[0].strip())
                end_time = float(parts[1].strip())
                text = parts[2].strip()
                subtitles.append({"start": start_time
                                  , "end": end_time
                                  , "text_en":text})
    return subtitles


def create_video_with_audio(image_path, audio_path, output_video_path, file_name,  fps=30, duration=5):

    """
    Tạo video từ các file ảnh trong thư mục.
    
    :param image_folder: Thư mục chứa các file ảnh
    :param output_video_path: Đường dẫn video đầu ra (ví dụ: 'output.mp4')
    :param fps: Số khung hình mỗi giây của video (mặc định là 30)
    """
    drawtext_filters = []
    subtitles = load_subtitles(file_name)

    # for i, subtitle in enumerate( subtitles):
    #     text = subtitle['text_en']
    #     wrapped_text = wrap_text(text, max_chars_per_line=50)
    #     temp_file = f"{file_name}_{i}.txt"
    #     write_to_file(temp_file, wrapped_text)

    output_folder = rf"assets\subtitle\book\{file_name}"

    if not os.path.exists(output_folder):
        print(f"ERROR ------------ Creating folder: {output_folder}")
    
    for i, subtitle in enumerate( subtitles):
        temp_file =  f"assets/subtitle/book/{file_name}/{file_name}_{i}.txt" 
        # os.path.join(output_folder, f"{file_name}_{i}.txt")

        # temp_file = f"{file_name}_{i}.txt"
        if i == 0:
            drawtext_filter = f"drawtext=textfile={temp_file}:x=(w-text_w)/2:y=(h*0.04):fontcolor=#FFFF33:fontfile='C\:\\Windows\\Fonts\\comicbd.ttf':fontsize=70:enable='between(t,{subtitle['start']},{subtitle['end']})'"
        else:
            drawtext_filter = f"drawtext=textfile={temp_file}:x=(w-text_w)/2:y=(h-text_h)/2:fontcolor=#FFFFFF:fontfile='C\:\\Windows\\Fonts\\ariblk.ttf':fontsize=60:line_spacing=-10:enable='between(t,{subtitle['start']},{subtitle['end']})'"
        drawtext_filters.append(drawtext_filter)

    # Ghép các filter drawtext lại với nhau
    drawtext_filter_string = ','.join(drawtext_filters)
    

    # Lệnh ffmpeg để tạo video từ ảnh
    command = [
        'ffmpeg',
         '-y', 
        '-loop', '1',                # Lặp lại ảnh để tạo video
        '-framerate', str(fps),      # Số khung hình mỗi giây
        '-i', image_path,            # Đầu vào là file ảnh
        '-i', audio_path,            # Đầu vào là file âm thanh MP3
        '-c:v', 'libx264',           # Codec video (H.264)
        '-r', str(fps),              # Khung hình mỗi giây cho video đầu ra
        '-pix_fmt', 'yuv420p',       # Định dạng pixel
        '-c:a', 'copy',               # Codec âm thanh (AAC)
        '-strict', 'experimental',   # Đảm bảo sử dụng codec AAC
        '-map', '0:v:0',             # Chỉ định đầu vào video từ file ảnh
        '-map', '1:a:0',             # Chỉ định đầu vào âm thanh từ file MP3
        '-shortest',                 # Đảm bảo video sẽ dài bằng độ dài của âm thanh
        '-vf', drawtext_filter_string,
        output_video_path           # Đường dẫn video đầu ra
    ]

    # Chạy lệnh ffmpeg
    subprocess.run(command)

def main():
    # Thư mục chứa các file ảnh
    # image_folder = 'images'  # Đảm bảo rằng bạn có thư mục 'images' với các file ảnh
    image_path = r"assets/image/img_padcast.jpg"
    audio_folder = r"assets\audio\test\\"
    output_folder = r"assets\video\output\book\\" 
    # output_video_path = r"assets/video/output/timemachinewells_01_ae_64kb.mp4"

    for audio_file in os.listdir(audio_folder):
        if audio_file.lower().endswith(".mp3"):
            file_name = os.path.splitext(audio_file)[0] 
            audio_path = os.path.join(audio_folder, audio_file)
            file_output = os.path.join(output_folder, file_name)
            create_video_with_audio(image_path, audio_path, f"{file_output}.mp4",file_name) 
            print(f"Video đã được tạo tại: {file_name}")


if __name__ == "__main__":
    # main2()
    main()

