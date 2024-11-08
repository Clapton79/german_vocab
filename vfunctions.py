from applogger import logger
from fileoperations import load_file

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
        
def compare_two_lists(a:list, b:list,header1:str="Header1",header2:str="Header2",no_header:bool=False,padding_default:int=0) -> list:
    try:
        padding = padding_default if padding_default != 0 else len(max([str(x) for x in a+[header1,header2]],key=len))
        
        if not no_header:
            print(f"{bcolors.HEADER}{str(header1).ljust(padding,' ')} - {str(header2).ljust(padding,' ')}{bcolors.ENDC}")
            
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
        return model_dict['words'][vocabulary_object_class]
      
def check_dict_structure(param_dict, model_dict,word):
    """
    Check if param_dict has the same keys as model_dict, including nested dictionaries.
    
    :param param_dict: The dictionary to check.
    :param model_dict: The model dictionary to compare against.
    :return: True if the structure matches, False otherwise.
    """
    try:
        if not isinstance(param_dict, dict) :
            logger.info("Not a dictionary.")
            return False

        for key in model_dict.keys():
            if key not in param_dict.keys():
                logger.warning(f"Dictionary model check (word: {word}): missing key: {key}")
                return False
            
            # If the value is a dictionary, check its structure recursively
            if isinstance(model_dict[key], dict):
                if not isinstance(param_dict[key], dict):
                    logger.warning(f"Dictionary model check: expected dictionary for key: {key}")
                    return False
                if not check_dict_structure(param_dict[key], model_dict[key],word):
                    logger.info(f"Dictionary model check: structure mismatch for key: {key}")
                    return False
        return True
    except Exception as e:
            logger.error(f"Error in check_dict_structure: {str(e)}")
            return False
                
    