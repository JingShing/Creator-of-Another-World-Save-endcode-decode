import base64
import json
import gzip

def decode_base64_gzip_json(file_path):
    try:
        with open(file_path, 'rb') as file:
            content = file.read()
        
        header_str = b"#=>main<=#"
        index = content.find(header_str)
        
        if index == -1:
            raise ValueError("Header '#=>main<=#' not found in the file.")
        
        base64_data = content[index + len(header_str):]
        
        gzip_data = base64.b64decode(base64_data)
        json_data = gzip.decompress(gzip_data)
        
        decoded_data = json.loads(json_data)
        return decoded_data
    
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred while processing the file {file_path}: {e}")

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

if __name__ == "__main__":
    file_name = "target/tbrg_save_0.tbrgsv"
    decoded_data = decode_base64_gzip_json(file_name)
    
    if decoded_data:
        output_json_file = "decoded_data.json"
        save_json_to_file(decoded_data, output_json_file)
