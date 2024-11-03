import random 
from json import loads
from os import path
import pprint

def load_config(file):
    global config
    global config_loaded

    if not path.exists(file):
        raise ValueError(f"Configuration file {file} does not exist.")

    with open(file, 'r') as f:
        config = loads(f.read())

    config_loaded = True

def get_config(config_item):
    if config_loaded:
        try:
            return config[config_item]
        except KeyError:
            return ''
    else:
        return ''


def load_file (file):
    vocab = {}
    if file == "":
        raise ValueError("Filename cannot be empty.")
    
    print(f"Loading {file}")
    

    if not path.exists(file):
        raise ValueError(f"File {file} does not exist.")
        
    # read the file
    line_id = 0
    key_index = 0
    with open(file,'r') as f:
        for line in f:
            cols = line.strip().split(',')
            if line_id == 0:
                header = cols
                if 'word' in header:
                    key_index = header.index('word')
                elif 'verb' in header:
                     key_index = header.index('verb')
                    
            else:
                vocab[cols[key_index]]={} # this is the word
                for i in range(len(header)):
                    if i != key_index:
                        if ';' in cols[i]:
                            vocab[cols[key_index]][header[i]] = cols[i].split(';')
                        else:
                            vocab[cols[key_index]][header[i]] = cols[i]
                
            line_id += 1
            
    return vocab
    
def pprint_vocab(file):
    my_vocab = load_file(file)
    pprint.pprint(my_vocab)
        
        
        
    