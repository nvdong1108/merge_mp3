from pydub import AudioSegment
import librosa
import soundfile as sf
import os


def change_speed_keep_pitch(input_path, output_path, speed=1.0):
    """
    Thay đổi tốc độ phát lại mà không thay đổi cao độ bằng librosa.

    Args:
        input_path (str): Đường dẫn đến tệp âm thanh đầu vào (MP3).
        output_path (str): Đường dẫn lưu tệp âm thanh đầu ra (WAV).
        speed (float): Tốc độ phát mới (ví dụ: 0.9 để chậm hơn, 1.1 để nhanh hơn).

    Returns:
        None
    """
    try:
        # Đọc tệp âm thanh
        y, sr = librosa.load(input_path, sr=None)
        
        # Thay đổi tốc độ mà không đổi cao độ
        y_stretched = librosa.effects.time_stretch(y, rate=speed)
        
        # Ghi tệp WAV đã xử lý
        sf.write(output_path, y_stretched, sr)
        print(f"Đã xử lý: {input_path} -> {output_path} với tốc độ {speed}x")
    
    except Exception as e:
        print(f"Lỗi khi xử lý {input_path}: {e}")





def change_audio_speed(audio, speed=1.0):
    """
    Thay đổi tốc độ phát của âm thanh.

    Args:
        audio (AudioSegment): Đối tượng âm thanh từ pydub.
        speed (float): Tốc độ phát mới (ví dụ: 0.9 để chậm hơn, 1.1 để nhanh hơn).

    Returns:
        AudioSegment: Đối tượng âm thanh đã thay đổi tốc độ.
    """
    # Tính toán frame_rate mới
    new_frame_rate = int(audio.frame_rate * speed)
    return audio._spawn(audio.raw_data, overrides={"frame_rate": new_frame_rate}).set_frame_rate(audio.frame_rate)



def convert_all_mp3_to_wav(input_dir, output_dir,  speed=0.8):
    """
    Chuyển đổi tất cả các tệp MP3 trong thư mục sang định dạng WAV.

    Args:
        input_dir (str): Đường dẫn đến thư mục chứa tệp MP3.
        output_dir (str): Đường dẫn đến thư mục lưu tệp WAV đầu ra.

    Returns:
        None
    """
    try:
        # Tạo thư mục đầu ra nếu chưa tồn tại
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Duyệt qua tất cả các tệp trong thư mục đầu vào
        for file_name in os.listdir(input_dir):
            # Kiểm tra xem tệp có phải là MP3 không
            if file_name.lower().endswith(".mp3"):
                input_mp3_path = os.path.join(input_dir, file_name)

                output_wav_path = os.path.join(output_dir, os.path.splitext(file_name)[0] + ".wav")
                

                # change_speed_keep_pitch(input_mp3_path, output_wav_path, speed)    

                # Chuyển đổi MP3 sang WAV
                slowed_audio = AudioSegment.from_mp3(input_mp3_path)
                # slowed_audio = change_audio_speed(audio, speed)
                slowed_audio.export(output_wav_path, format="wav")
                print(f"Đã chuyển đổi: {file_name} -> {output_wav_path}")
                
       
    
    except Exception as e:
        print(f"Lỗi khi chuyển đổi: {e}")


def cut_mp3(input_file, output_file, start_time, end_time):
    """
    Cắt file MP3 từ thời gian bắt đầu đến kết thúc.
    
    Args:
        input_file (str): Đường dẫn đến file MP3 đầu vào.
        output_file (str): Đường dẫn lưu file MP3 đầu ra.
        start_time (int): Thời gian bắt đầu (tính bằng mili-giây).
        end_time (int): Thời gian kết thúc (tính bằng mili-giây).
    
    Returns:
        None
    """
    try:
        # Đọc file MP3
        audio = AudioSegment.from_file(input_file, format="mp3")
        
        # Cắt file theo thời gian
        cut_audio = audio[start_time:end_time]
        
        # Lưu file MP3 đã cắt
        cut_audio.export(output_file, format="mp3")
        print(f"File MP3 đã được cắt và lưu tại: {output_file}")
    except Exception as e:
        print(f"Lỗi: {e}")

# Đường dẫn thư mục
# folder_path = r"assets\test\\" 
# input_directory = r"assets\audio\input_mp3\\" 
# output_directory = r"assets\audio\input_wav\\" 
# convert_all_mp3_to_wav(input_directory, output_directory)

input_file = r"assets\audio\book\timemachinewells_01_ae_64kb.mp3"  # Thư mục chứa các tệp MP3
output_file = r"assets\audio\input_mp3\2p_timemachinewells_01_ae_64kb.mp3" 
cut_mp3(input_file, output_file, 0, 120 * 1000)
