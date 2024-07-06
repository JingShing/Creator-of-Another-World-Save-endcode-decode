import base64
import json
import gzip
import tkinter as tk
from tkinter import filedialog, messagebox


def read_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"file {file_path} not found")
    except json.JSONDecodeError:
        print(f"file {file_path} is not a valid json file")
    except Exception as e:
        print(f"error while loading {file_path} with: {e}")


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


def select_json_file():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        json_file_path_var.set(file_path)


def select_save_file():
    file_path = filedialog.askopenfilename(filetypes=[("Save files", "*.tbrgsv")])
    if file_path:
        save_file_path_var.set(file_path)


def decode_save_file():
    save_file_path = save_file_path_var.get()
    json_file_path = json_file_path_var.get()
    
    if not save_file_path:
        messagebox.showerror("Error", "Please select a save file.")
        return
    
    decoded_data = decode_base64_gzip_json(save_file_path)
    if decoded_data:
        if json_file_path:
            save_json_to_file(decoded_data, json_file_path)
            messagebox.showinfo("Success", f"Data successfully decoded to {json_file_path}")
        else:
            json_file_path = save_file_path + "_decoded.json"
            save_json_to_file(decoded_data, json_file_path)
            messagebox.showinfo("Success", f"Data successfully decoded to {json_file_path}")


def encode_json_file():
    json_file_path = json_file_path_var.get()
    save_file_path = save_file_path_var.get()
    if not json_file_path:
        messagebox.showerror("Error", "Please select a JSON file.")
        return
    if not save_file_path:
        messagebox.showerror("Error", "Please select a save file.")
        return
    
    json_content = read_json(json_file_path)
    save_file_contents = read_text_file(save_file_path)
    encoded_data = encode_json_to_base64_gzip(json_content)
    encoded_data = encoded_data.decode('utf-8')
    
    header_str = "#=>main<=#"
    save_file_contents = save_file_contents.split(header_str)[0] + header_str
    output_save_file_path = save_file_path + "_encoded.tbrgsv"
    
    if encoded_data:
        write_text_file(output_save_file_path, save_file_contents + encoded_data)
        messagebox.showinfo("Success", f"Data successfully encoded to {output_save_file_path}")


# GUI setup
root = tk.Tk()
root.title("Save File Encoder/Decoder")

json_file_path_var = tk.StringVar()
save_file_path_var = tk.StringVar()

tk.Label(root, text="JSON File:").grid(row=0, column=0, padx=10, pady=5)
tk.Entry(root, textvariable=json_file_path_var, width=50).grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=select_json_file).grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Save File:").grid(row=1, column=0, padx=10, pady=5)
tk.Entry(root, textvariable=save_file_path_var, width=50).grid(row=1, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=select_save_file).grid(row=1, column=2, padx=10, pady=5)

tk.Button(root, text="Decode", command=decode_save_file).grid(row=2, column=0, columnspan=3, pady=10)
tk.Button(root, text="Encode", command=encode_json_file).grid(row=3, column=0, columnspan=3, pady=10)

root.mainloop()
