from ruamel.yaml import YAML as yaml2
import yaml
from os import path,remove
import zipfile36 as zipfile
import shutil
from datetime import datetime
from applogger import logger
import requests
import bs4
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
import json

disable_warnings(InsecureRequestWarning)


def get_definite_article(noun: str = None) -> str:
    logger.debug(f'get_definite_article for {noun}')
    try:
        if noun is None:
            raise ValueError("Noun is required")

        articles = ['der', 'die', 'das']
        for article in articles:
            response = requests.get(
                f"https://der-artikel.de/{article}/{noun}.html", verify=False)
            if response.status_code == 200:
                return article
    except Exception as e:
        logger.error(f'get_definite_article for {noun} failed with error: {str(e)}')
        return ''


def get_conjugation(verb):
    try:
        logger.debug(f'get_conjugation for {verb}')
        url = f"https://conjugator.reverso.net/conjugation-german-verb-{verb}.html"
        sess = requests.session()
        sess.headers.update({'User-Agent': 'EventParser PowerShell/7.3.4'})
        page = sess.get(url, verify=False)
        soup = bs4.BeautifulSoup(page.content, "html.parser")
        output = {'conjugations': {}, 'imperative': ''}
        # imperative
        imperative = soup.find_all('div', class_='blue-box-wrap alt-tense')
        for c in imperative:
            title = str(c['mobile-title'])
            if title == 'Imperativ Präsens':
                verb_imperative = c.find('i', class_='verbtxt')
                output['imperative'] = str(verb_imperative.text).rstrip()

        # conjugation
        conjugation = soup.find_all('div', class_='blue-box-wrap')

        for c in conjugation:
            title = c['mobile-title']
            if title[0:9] == 'Indikativ' and title.split(' ')[1] in ['Präsens', 'Präteritum', 'Perfekt']:
                res_tense = str(c.p.string)
                output['conjugations'][res_tense] = []
                for conjugation_block in c.find_all('ul', class_='wrap-verbs-listing'):
                    conj_data = []
                    for row in conjugation_block.children:
                        # remove the personal pronoun
                        conj_data.append(str(' '.join(row.text.split(' ')[1:])))

                    # output.append(','.join([verb,res_tense,res_tags,';'.join(conj_data)]))
                    output['conjugations'][res_tense] = conj_data
        return output
    except Exception as e:
        logger.error(f'Error processing conjugation webrequest for {verb}')
        return {}
def load_file(filename,file_type:str=None):
    try:
        vocab = {}

        # read the file
        with open(filename, 'r') as f:
            if filename.endswith('.yaml') or file_type=='yaml':
                vocab = yaml.safe_load(f)
            elif filename.endswith('.json') or file_type=='json':
                vocab = json.load(f)
            else:
                raise ValueError(f"Invalid arguments. {filename.split('.')[-1]}, {file_type}")

        return vocab
    except Exception as e:
        logger.error(f"Error loading file {filename}: {str(e)}")
        print(f"Error loading file {filename}: {str(e)}")
        return None

def save_to_file(filename, contents: dict, format:str='yaml',safe:bool=False,overwrite:bool=False):
    try:
        logger.info(f"Saving to file {filename}, format: {format}, safe: {safe}")
        if not overwrite and path.exists(filename):
            raise ValueError(f"File {filename} already exists. Use overwrite=True to overwrite.")
        with open(filename, 'w', encoding='utf-8') as f:
            if format == 'json':
                json.dump(contents, f, indent=4, ensure_ascii=False)
            elif format == 'yaml' and safe is False:
                yaml.dump(contents, f, default_flow_style=False, allow_unicode=True)
            elif format == 'yaml' and safe is True:
                yaml.safe_dump_all(contents, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
            elif format =='ruamel':
                yaml=yaml2()
                yaml.dump(contents,f)
            else:
                raise ValueError("Unsupported file format")

    except Exception as e:
            logger.error(f"Error writing to file {filename}: {str(e)}")
            print(str(e))


def backup_file(filename):
    try:
        fileserial = datetime.now()
        fileserial = fileserial.strftime("%Y%m%d%H%M%S")
        backup_filename = f"{''.join(filename.split('.')[0:-1])}{fileserial}.bak"

        shutil.copy(filename, backup_filename)
        logger.info(f"Backup created: {backup_filename}")
        return backup_filename
    except Exception as e:
        logger.error(f"Error backing up file {filename}: {str(e)}")
        return None

def zip_files(file_paths:list, zip_name:str):
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
        
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def list_find(my_list:list,element:int):
    try:
        return my_list[element]
    except:
        return None
        
def compare_two_lists(a:list, b:list,header1:str="Solution",header2:str="Entry",no_header:bool=False,padding_default:int=0) -> list:
    try:
        padding = padding_default if padding_default != 0 else len(max([str(x) for x in a+[header1,header2]],key=len))
        
        if not no_header:
            print(f"{''.ljust(padding, ' ')}{bcolors.HEADER}{str(header1).ljust(padding,' ')} - {str(header2).ljust(padding,' ')}{bcolors.ENDC}")
        for i in range(len(a)):
            if a[i]==list_find(b,i):
                print(f"{''.ljust(padding, ' ')}{bcolors.OKGREEN}{str(a[i]).ljust(padding,' ')} - {str(list_find(b,i)).ljust(padding,' ')}{bcolors.ENDC}")
            else:
                other_value = list_find(b,i)
                print(f"{''.ljust(padding,' ')}{bcolors.FAIL}{str(a[i]).ljust(padding,' ')} - {str(list_find(b,i)).ljust(padding,' ')}{bcolors.ENDC}")
    
    except Exception as e:
        logger.error(f"Error in compare_two_lists: {str(e)}")

def get_vocabulary_model(vocabulary_object_class: str=None):
    # Reads a yaml file and returns a dictionary
    model_dict = load_file('model.yaml')

    if vocabulary_object_class is None:
        return model_dict
    else:
        return model_dict[vocabulary_object_class]
      
def check_dict_structure(param_dict, model_dict,word,verbose:bool=False, recursive:bool=False):
    """
    Check if param_dict has the same keys as model_dict, including nested dictionaries.
    
    :param param_dict: The dictionary to check.
    :param model_dict: The model dictionary to compare against.
    :return: True if the structure matches, False otherwise.
    """
    try:
        if not isinstance(param_dict, dict) :
            logger.info("Not a dictionary.")
            if verbose :
                return False, ["Not a dictionary"]
            else:
                return False
        
        result = True
        result_verbose = []
        
        for key in model_dict.keys():
            if key not in param_dict.keys():
                logger.warning(f"Dictionary model check (word: {word}): missing key: {key}")
                result = False
                if verbose:
                    result_verbose.append(key)
            
            # If the value is a dictionary, check its structure recursively
            if recursive and isinstance(model_dict[key], dict):
                if not isinstance(param_dict[key], dict):
                    logger.warning(f"Dictionary model check: expected dictionary for key: {key}")
                    result = False
                    if verbose:
                        result_verbose.append(key)
                if not check_dict_structure(param_dict[key], model_dict[key],word):
                    logger.info(f"Dictionary model check: structure mismatch for key: {key}")
                    result = False
                    if verbose:
                        result_verbose.append(key)
                    
        if verbose:
            return result, result_verbose
        else:
            return result
        
    except Exception as e:
            logger.error(f"Error in check_dict_structure: {str(e)}")
            return False
                