import urllib.parse
import json
from pathlib import Path

header_dir = r'D:\Developed\Automation\GalleryDownloader\headerfiles'

def parse_firefox_header(header_str):
    header_lines = header_str.strip().split('\n')[1:]
    header_dict = {}
    for line in header_lines:
        if 'Accept-Encoding' in line:
            continue
        key, value = line.split(':', 1)
        header_dict[key.strip()] = value.strip()
    return header_dict

def read_header_file(file_name):
    Path(header_dir).mkdir(parents=True, exist_ok=True)
    file_path = Path(header_dir) / file_name
    try:
        with open(file_path, 'r') as file:
            header_str = file.read()
            return parse_firefox_header(header_str)
    except FileNotFoundError:
        file_path.touch()
        print(f"File not found: {file_path} but created now")
        breakpoint()
        return {}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

if __name__ == "__main__":
    # file_path = "request_header.txt"  # Replace with the path to your header file
    header_dict = read_header_file(file_path)

    if header_dict:
        header_json = json.dumps(header_dict, indent=4)
        print(header_json)
