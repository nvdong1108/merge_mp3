
import datetime
import os


def subtitels_all(audio_path):
    model = whisper.load_model("base")
    load_audio_file(audio_path)

    result = model.transcribe(audio_path, word_timestamps=True)
    buffer = ""
    start_time = None

    for segment in result['segments']:
        text = segment['text']
        end_time = segment['end']

        # Thêm văn bản vào buffer
        if start_time is None:
            start_time = segment['start']
        buffer += text + " "

        # Tìm các câu kết thúc bằng dấu câu
        sentences = re.split(r'([.?!])', buffer)
        for i in range(0, len(sentences) - 1, 2):  # Lấy các cặp câu và dấu câu
            full_sentence = sentences[i].strip() + sentences[i + 1]
            subtitle = f"{start_time:.2f} -> {end_time:.2f}: {full_sentence}\n"
            write_subtitle_to_file(subtitle)
            start_time = None  # Reset thời gian bắt đầu
        buffer = sentences[-1].strip()  # Câu chưa kết thúc (nếu có)

    # Ghi câu còn lại trong buffer (nếu kết thúc đoạn)
    if buffer:
        subtitle = f"{start_time:.2f} -> {end_time:.2f}: {buffer}\n"
        write_subtitle_to_file(subtitle)

    print("Hoàn tất ghi phụ đề.")
    return None, None


def write_subtitle_to_file(subtitles):
    # Tạo tên file dựa trên thời gian hiện tại
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    output_file = f"assets/subtitle_{timestamp}.txt"

    # Tạo thư mục nếu chưa tồn tại
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    try:
        with open(output_file, 'a', encoding='utf-8') as file:
            file.write(subtitles)  # Ghi nội dung vào file
        print(f"Subtitles written to: {output_file}")
    except Exception as e:
        print(f"An error occurred while writing subtitles: {e}")