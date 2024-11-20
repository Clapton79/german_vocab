import yaml
from os import path
import zipfile36 as zipfile
import shutil
from datetime import datetime
from applogger import logger

def load_file (filename):
    try:
        vocab = {}
        
        # read the file
        with open (filename, 'r') as f:
            vocab = yaml.safe_load(f)
        
        return vocab
    except Exception as e:
        logger.error(f"Error loading file {filename}: {str(e)}")
        return None

def save_to_file(filename, contents:dict):
    # try:
    with open(filename, 'w', encoding='utf-8') as f:
        yaml.dump(contents, f, default_flow_style=False,allow_unicode=True)
    
    # except Exception as e:
    #         #logger.error(f"Error writing to file {filename}: {str(e)}")
    #         print(str(e))
        
def backup_file(filename):
    try:
        fileserial =datetime.now()
        fileserial = fileserial.strftime("%Y%m%d%H%M%S") 
        backup_filename =f"{''.join(filename.split('.')[0:-1])}{fileserial}.bak"
    
        shutil.copy(filename, backup_filename)
        logger.info(f"Backup created: {backup_filename}")
        return backup_filename
    except Exception as e:
        logger.error(f"Error backing up file {filename}: {str(e)}")
        return None
    
def zip_files(file_paths, zip_name):
    try:
        with zipfile.ZipFile(zip_name, 'w') as zipf:
            for file in file_paths:
                zipf.write(file, path.basename(file))
        logger.info(f"Files zipped into {zip_name}")
    except Exception as e:
        logger.error(f"Error zipping files: {str(e)}")
    
def unzip_file(zip_name, extract_to):
    try:
        with zipfile.ZipFile(zip_name, 'r') as zipf:
            zipf.extractall(extract_to)
        logger.info(f"Files extracted to {extract_to}")
    except Exception as e:
            logger.error(f"Error extracting files from {zip_name}: {str(e)}")