import base64
import json
import gzip

def read_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到。")
    except json.JSONDecodeError:
        print(f"文件 {file_path} 不是有效的 JSON 文件。")
    except Exception as e:
        print(f"读取文件 {file_path} 时发生错误：{e}")


def save_json_to_file(data, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Data successfully saved to {file_path}")
    except Exception as e:
        print(f"An error occurred while writing to the file {file_path}: {e}")

def encode_json_to_base64_gzip(data):
    try:
        json_str = json.dumps(data, ensure_ascii=False).encode('utf-8')
        gzip_data = gzip.compress(json_str)
        base64_data = base64.b64encode(gzip_data)
        return base64_data
    except Exception as e:
        print(f"An error occurred while encoding to base64 gzip: {e}")

def read_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred while reading the file {file_path}: {e}")

def write_text_file(file_path, content):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Data successfully saved to {file_path}")
    except Exception as e:
        print(f"An error occurred while writing to the file {file_path}: {e}")

header_str = "#=>main<=#"
if __name__ == "__main__":
    file_name = "target/tbrg_save_0.tbrgsv"
    output_file_name = "save_file.tbrgsv"
    output_json_file = "decoded_data.json"
    json_content = read_json(output_json_file)
    save_file_contents = read_text_file(file_name)
    encoded_data = encode_json_to_base64_gzip(json_content)
    encoded_data = str(encoded_data)
    save_file_contents = save_file_contents.split(header_str)[0]+header_str

    if encoded_data:
        write_text_file(output_file_name, save_file_contents+encoded_data)
