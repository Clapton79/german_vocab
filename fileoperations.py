import yaml
import os
import zipfile36 as zipfile
import shutil
from datetime import datetime

# file operations
def load_file (filename):
    vocab = {}
    
    # read the file
    with open (filename, 'r') as f:
        vocab = yaml.safe_load(f)
    
    return vocab

def save_to_file(filename, contents:dict):
    with open(filename, 'w', encoding='utf-8') as f:
        yaml.dump(contents, f, default_flow_style=False,allow_unicode=True)
        
def backup_file(filename):
    fileserial =datetime.now()
    fileserial = fileserial.strftime("%Y%m%d%H%M%S") 
    backup_filename =f"{''.join(filename.split('.')[0:-1])}{fileserial}.bak"
    try:
        shutil.copy(filename, backup_filename)
        print(f"Backup created: {backup_filename}")
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
    except PermissionError:
        print(f"Error: Permission denied to create backup of {filename}.")
    except Exception as e:
        print(f"Error backing up file {filename}: {str(e)}")
    
def zip_files(file_paths, zip_name):
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for file in file_paths:
            zipf.write(file, os.path.basename(file))
    print(f"Files zipped into {zip_name}")
    
def unzip_file(zip_name, extract_to):
    with zipfile.ZipFile(zip_name, 'r') as zipf:
        zipf.extractall(extract_to)
    print(f"Files extracted to {extract_to}")