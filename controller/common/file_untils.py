import os

def write_to_file(file_path, content,overwrite=True):
    """
    Ghi nội dung mới vào tệp, xóa nội dung cũ trước khi ghi.
    
    Args:
        file_path (str): Đường dẫn đến tệp cần ghi.
        content (str): Nội dung cần ghi vào tệp.
    """
    try:
        if overwrite:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
        else:
            with open(file_path, 'a', encoding='utf-8') as file:
                file.write(content)        
                
    except Exception as e:
        print(f"Lỗi khi ghi tệp: {e}")

if __name__ == "__main__":
    pass