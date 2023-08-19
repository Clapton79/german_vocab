"""
This simple app helps speed testing and building vocabulary in a foreign language. 
"""
library_version = "1.1.1"

print ("Vocabularizer {0}".format(library_version))

import pandas as pd
import numpy as np
import random 
from json import loads
from os import path
from datetime import datetime
config = {}
config_loaded = False


language = ""
secondary_language = ""
vocabulary_type = ""
loaded_files = []
weights_loaded = False
weights_updated_not_saved = False

if path.exists('config.json'):
    with open ('config.json', 'r') as f:
        config = loads(f.read())
        config_loaded=True

def get_config(config_item):
    """
    If configuration has been loaded, this function will retrieve the value of the config_item.
    """
    if config_loaded:
        try:
            return config[config_item]
        except:
            return ''
    else:
        return ''

df = pd.DataFrame()
res = pd.DataFrame()

# Vocabulary file handling
def load_file(file):
    """
    Loads a vocabulary file and extracts file information from a conventional filename
    """
    global df
    global language
    global secondary_language
    global vocabulary_type
    global loaded_files

    try:
        if file == "":
            raise ValueError("Filename cannot be empty.")
        print("Loading {0}".format(file))
        if file in loaded_files:
            raise ValueError("File {0} has already been loaded.".format(file))
        
        *info, ext = file.split('/')[-1].split('.')
        _language, _secondary_language, _vocabulary_type, *others = info[0].split('_')
        if (language != "" and language != _language) or (secondary_language != _secondary_language and secondary_language!="") :
            raise ValueError("Cannot load {0}-{1} into loaded {2}-{3} vocabulary.".format(_language,_secondary_language,language,secondary_language))
        
        language=_language
        secondary_language=_secondary_language

        if vocabulary_type != "" :
            vocabulary_type= [vocabulary_type,_vocabulary_type]
        else:
            vocabulary_type=_vocabulary_type

        da = pd.read_csv(file)
        # transformations:
        # computed column: Full word: look up the definite article and add it to the word
        da['_expression']=da['da'].apply(decode_da)+ ' ' + da['word']
       
        # load weights if weight file can be found
        if config_loaded and path.exists(get_config('weights_file')) and not weights_updated_not_saved:
            dw = pd.read_csv(get_config('weights_file'))
            da.drop('_weight',inplace=True)
            da=da.merge(dw, on=['translation', 'translation'],how='left')
            
            weights_loaded=True
        else:
            da['_weight']=1

        df=df._append(da)
        loaded_files.append(file)
        print(df)
        print('Loaded {3} words from {0} vocabulary ({1} - {2})'.format(_vocabulary_type,language,secondary_language, len(da)))
    except Exception as ex:
        print(str(ex))

def unload_vocabulary():
    """
    Clears the memory from all loaded vocabularies.
    """
    global df
    global language
    global secondary_language
    global vocabulary_type
    global loaded_files
    
    print("Unloading vocabulary ({0} file(s))".format(len(loaded_files)))
    df = pd.DataFrame()
    language = ""
    secondary_language= ""
    vocabulary_type=""
    loaded_files=[]

def save_vocabulary_to_file(file=""):
    """
    Exports a vocabulary file.
    """
    if len(loaded_files) ==0:
        raise ValueError("There is no file loaded.")
    elif len(loaded_files) == 1: 
        _clean_and_save(file)
    else:
        response = input("There are multiple files loaded. You can save all the data into a single file. Do you wish to proceed? (y)") or 'y'
        if response == 'y':
            default = ".".join(["_".join ([language,secondary_language,"new"]), 'csv'])
            response = input("Filename ({0}):".format(default)) or default
            _clean_and_save(response)
                
def _clean_and_save(file=""):
    """used internally only: drops _ columns and exports dataframe."""
    if file =="":
        raise ValueError("Specify a filename.")

    global df
    da = df.filter(regex=r'^(?!_)')
    try:
        da.to_csv(file, index = False)
        print("Saving to {0} complete.".format(file))
    except Exception as ex:
        print(str(ex))

def update_weights(dw:pd.DataFrame):
    """
    Updates the weights based on the latest test result
    """
    global df
    global weights_updated_not_saved
    # aggregate dw by Solution, Word take Points Avg
    dw_agg=dw.groupby(['Solution','Word']).agg(_PointUpdate=('Point','mean'))
    df = df.merge(dw_agg, left_on = ['_expression', 'translation'], right_on = ['Solution', 'Word'], how='left')
    values = {"_PointUpdate":1}
    df.fillna(value=values, inplace=True)
    df['_weight']=1/((df['_weight']+df['_PointUpdate'])/2)
    df.drop('_PointUpdate',axis=1, inplace=True)
    weights_updated_not_saved=True
    print("{0} weight(s) updated.".format(len(dw_agg)))
    

def output_decorator(text, level):
    print(72*"#")
    print("#", level * " ", text)
    print(72*"#")

def left_1 (s:str):
    """
    Returns the first character of a string. 
    Used in dataframe value references"""
    return s[0]

def decode_mode(mode:str):
    """
    converts a mode code into the mode description
    """
    match mode:
        case 'n':
            return 'nominative'
        case 'd':
            return 'dativ'
        case 'a':
            return 'akkusativ'
        case 'g':
            return 'genitiv'
        case _: 
            return ''

def decode_da(da:str):
    """
    Converts definitive article code into a definitive article
    """
    match da:
        case 'n':
            return 'das'
        case 'm': 
            return 'der'
        case 'f':
            return 'die'
        case 'm':
            return 'dem'
        case 'd':
            return 'den'
        case _:
            return ''

def set_convert(s:set):
    """
    Concatenates set elements
    """
    return ' '.join (s)

def translate(word:str, all:str='first', rev:str='str', da:str='da') -> list:
    """
    Translates a word, outputs a list
    options:
    - get all translations (all:True) or the first (all:first)
    - reverse translate (ie to first language) (rev: rev) or straight (rev: str)
    - retrieve definitive article (da: da) or not (da: n)
    """
    global df

    try: 
        result = ['']

        if all not in ['first', 'all']:
            raise ValueError('Argument "all" invalid (can be first or all)')
        if rev not in ['rev','str']:
            raise ValueError('Argument "rev" invalid (can be rev or str)')
        if da not in ['da', 'n']:
            raise ValueError('Argument DA invalid (can be da or n)')

        if rev=='rev':
            _filter = df.translation==word
            result = list(df[_filter].word)
            if da=='da':
                result_da = list(df[_filter].da)
                result_da = map(decode_da, result_da)
                merged = list(zip(result_da, result))
                result = list(map(set_convert, merged))           

        else:
            _filter = df.word==word
            result = list(df[_filter].translation)
        
        if len(result) == 0:
            result = ['#N/A']

        if all=='first':
            a = []
            a.append(result[0])
            result = a
    except ValueError as ex:
        print(str(ex))

    except Exception as ex:
        print(str(ex))
        result = ['#N/A']

    return result

def translate_list(words:list, rev:str='str',da:str='da') -> list:
    """
    Finds the first translation of all the input words
    """
    if rev not in ['rev','str']:
        raise ValueError('Argument "rev" invalid (can be rev or str)')
    if da not in ['da', 'n']:
        raise ValueError('Argument DA invalid (can be da or n)')
    # organise retrieved lists into one single list    
    return sum([translate(x, 'first',rev,da) for x in words],[])

# Vocabulary content commands
def add_word(word, da, translation, weight, mode):
    """
    Adds a word to the vocabulary in the memory
    """
    global df
    df = df._append(pd.Series({"mode": mode,"Word":word,"DA":da, "Translation": translation, "Weight":weight}), ignore_index=True)

def save_result(test, points, rounds):
    """
    Saves the result of a test in the results file.
    """
    if config_loaded and len(get_config('results_file'))>0:
        row = ','.join([datetime.today().strftime('%Y-%m-%d-%H:%M:%S'), get_config('profile'),test,str(points),str(rounds)])
        row = ''.join([row, '\n'])
        with open (get_config('results_file'), 'a') as f:
            f.write(row)

def save_weights():
    global df
    global weights_updated_not_saved
    file = get_config('weights_file')
    de = pd.DataFrame(df.filter(items=['translation','_expression','_weight']), columns = ['translation', '_expression','_weight'])
    de.to_csv(file, index=False)
    weights_updated_not_saved=True
    print('Weights saved.')

def test_1():
    """
    Test 1 tests your writing skills and knowledge
    """
    count_of_words= int(input("How many words shall I ask from you in this test?(10)") or "10")
    
    output_decorator("Test 1", 4)

    global df

    if len(df) < count_of_words:
        count_of_words = len(df) 
    # set up test words
    
    rnd = [random.choice(range(0, len(df)-1)) for i in range(0,count_of_words)]
    translations = [df['translation'][i] for i in rnd]
    words = [df['word'][i] for i in rnd]
    solutions = [df['_expression'][i] for i in rnd]
    counts = [len(df[df['translation']==i]) for i in translations]

    responses= []
    for k in range(0,len(translations)):
        word = translations[k]
        c = len(df[df['translation']==word])
        match len(df[df['translation']==word]):
            case 0:
                hint = ""
            case 1:
                hint = ""
            case _:
                hint = "(hint: {0})".format(words[k][0])
        response = input("What is {0} in {1}{2}? ".format(word, language,hint)) or ""
        responses.append(str(response))

    evaluations = [solutions[i] == responses[i] for i in range(0, len(translations))]
    res = round(sum([int(i) for i in evaluations])/len(translations)*100, 1)
    dres = pd.DataFrame(data=zip(translations, solutions, responses, [int(i) for i in evaluations]),
                        columns = ['Word', 'Solution', 'Response', 'Point'])
    output_decorator('Results', 6)

    print ("Your result is {0}%".format(res)) 
    
    save_result('Test 1', res, len(translations))

    # update weights
    update_weights(dres)

def test_selector():
    response = input("""Press the letter of the test to start it:
    a - Test 1 (type words) 
    b - Test 2 (multiple choice)
    """) or 'skip'
    match response: 
        case "a":
            test_1()
        case "b": 
            raise NotImplementedError
        case _:
            print("Nothing selected.")

if config_loaded and get_config("auto_load_default_vocabulary")=="true":
    load_file(get_config("default_vocabulary"))

load_file(get_config('default_vocabulary'))

if config_loaded and get_config("autostart_test_selector")=="true":
    test_selector()

test_1()
save_weights()
#print(df)