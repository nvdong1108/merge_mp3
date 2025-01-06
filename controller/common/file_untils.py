import os
import uuid as uuids
import json
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

def convert_text_to_json(text):
    file_tmp = rf"static\tmp\{uuids.uuid4()}.txt" 
    write_to_file(file_tmp,text)

    json_result = []
    with open(file_tmp, 'r', encoding='utf-8') as file:
        # lines = file.readlines()
        lines = [line.strip() for line in file if line.strip()]
        
    for i in range(0,len(lines),2):
        en_text = lines[i].strip()    
        en_text = lines[i+1].strip()
        json_result.append({"en":en_text,
                            "es":en_text})    
        
    os.remove(file_tmp)
    return json_result

def create_folder_new_project():
    sequence =  0 
    with open('static/data.json', 'r+') as f:
        data = json.load(f)
        data['sequence'] += 1
        sequence = data['sequence']
        f.seek(0)
        json.dump(data, f)
        f.truncate()


    project_name = f"myproject{sequence}"
    output_folder = rf"static\project_videos\{project_name}\\" 
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    return output_folder


if __name__ == "__main__":
    pass