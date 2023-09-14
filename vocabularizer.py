"""
This simple app helps speed testing and building vocabulary in a foreign language. 
"""
    


import pandas as pd
import logging 
import numpy as np
import random 
from json import loads
from os import path
from datetime import datetime
import time
import matplotlib.pyplot as plt
from pprint import pprint

config = {}
config_loaded = False

library_version = "1.1.4"

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
df.style.set_properties(**{'text-align': 'left'})
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

    #try:
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
    da['_expression']=da['_expression'].apply(lambda x: x.strip())
    da['_weight']=1
    # append loaded vocabulary to the in-memory vocabulary
    df=df._append(da)

    # load weights if weight file can be found
    if config_loaded and path.exists(get_config('weights_file')) and not weights_updated_not_saved:
       load_weights(get_config('weights_file'))
     
    #df.drop_duplicates(inplace=True)
    loaded_files.append(file)
    print('Loaded {3} words from {0} vocabulary ({1} - {2})'.format(_vocabulary_type,language,secondary_language, len(da)))



def load_weights(file):
    global weights_loaded
    global df
    dw = pd.read_csv(file)

    if '_weight' in df.columns:
        df.rename({"_weight":"_weight_df"}, axis=1,inplace=True)

    df = df.merge(dw,how='left', left_on=['translation', '_expression'], right_on=['translation', '_expression'])

    if '_weight_df' in df.columns:
        df['_weight']= df['_weight'].fillna(df['_weight_df']).fillna(1)
        df.drop(['_weight_df'],axis=1, inplace=True)
    
    weights_loaded=True
    print("Loaded {0} weights".format(len(dw)))

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

def show_loaded_files():
    if len(loaded_files)==0:
        print('No files loaded.')
    else:
        output_decorator("Loaded files", 8)
        for i in loaded_files:
            print(i)
        output_decorator("",0,'end')

def show_vocabulary(offset_rows:int,fetch_rows:int):

    global loaded_files
    global df

    if len(loaded_files)==0:
        raise ValueError('No vocabulary to show.')
            
    max_len = len(df)
    
    if offset_rows>max_len:
        raise ValueError("There are less rows than the offset value")
    
    range_end = offset_rows+fetch_rows+1
    if range_end>max_len:
        range_end = max_len

    # display(df.style.set_properties(**{'text-align': 'left'}))
    print(df.loc[offset_rows:range_end][['translation', '_expression']])

def show_vocabulary_pg(pagesize:int):
    global df
    if pagesize>len(df):
        show_vocabulary(0,len(df))
    else:
        offset=0
        
        while True:
            range_end = offset+pagesize
            if range_end>len(df):
                range_end = len(df)

            print(df.loc[offset:range_end][['translation', '_expression']])
            offset=offset+pagesize
            response = input("Continue?(y)") or 'y'

            if offset>len(df) or response !='y':
                break

def save_vocabulary_to_file(file=""):
    """
    Exports a vocabulary file.
    """
    if len(loaded_files) ==0:
        raise ValueError("There is no file loaded.")
    elif len(loaded_files) == 1: 
        clean_and_save_vocabulary(file)
    else:
        response = input("There are multiple files loaded. You can save all the data into a single file. Do you wish to proceed? (y)") or 'y'
        if response == 'y':
            default = ".".join(["_".join ([language,secondary_language,"new"]), 'csv'])
            response = input("Filename ({0}):".format(default)) or default
            clean_and_save_vocabulary(response)
                
def clean_and_save_vocabulary(file=""):
    """used internally only: drops _ columns and exports dataframe."""
    if file =="":
        raise ValueError("Specify a filename.")

    global df
    da = df.filter(regex=r'^(?!_)')
    try:
        da.to_csv(file, index = False) #this method puts a linebreak at the end
        print("Saving to {0} complete({1} words).".format(file, len(da)))
    except Exception as ex:
        print(str(ex))

def new_weight(row):
    if row['_PointUpdate'] == 0:
        returnvalue = row['_weight'] + 0.2
    elif pd.isna(row['_PointUpdate']):
        returnvalue = row['_weight']
    else:
        if row['_weight'] > 0.2:
            returnvalue = row['_weight'] - 0.2
        else:
            returnvalue = 0.2
    returnvalue = round(returnvalue, 2)
    return returnvalue

def update_weights(dw:pd.DataFrame):
    """
    Updates the weights based on the latest test result
    """
    global df
    global weights_updated_not_saved
    # aggregate dw by Solution, Word take Points Avg
    dw_agg=dw.groupby(['Solution','Word']).agg(_PointUpdate=('Point','mean'))
    df = df.merge(dw_agg, left_on = ['_expression', 'translation'], right_on = ['Solution', 'Word'], how='left')
    #df.apply(lambda x: f(x.col_1, x.col_2), axis=1)
    df['_weight']=df.apply(new_weight,axis=1)
    df.drop('_PointUpdate', axis = 1, inplace = True)
    weights_updated_not_saved=True
    print("{0} weight(s) updated.".format(len(dw_agg)))
    if get_config("autosave_weights")=="true":
        save_weights(get_config("weights_file"))
    
def output_decorator(text, level, motiv='start'):
    if motiv=='start':
        print(72*"#")
        print("#", level * " ", text)
        print(72*"=")
    elif motiv =='end':
        print(72*"-")

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
            return 'Nominativ-Substantiv'
        case 'd':
            return 'Dativ-Substantiv'
        case 'a':
            return 'Akkusativ Substantiv'
        case 'g':
            return 'Genitiv-Substantiv'
        case 'v':
            return 'Verb'
        case 'a':
            return 'Adjektiv'
        case 's':
            return 'other'
        case _: 
            return ''

def decode_da(da:str) -> str:
    """
    Converts definitive article code into a definitive article
    """
    match da:
        case 's':
            return 'das'
        case 'r': 
            return 'der'
        case 'e':
            return 'die'
        case 'm':
            return 'dem'
        case 'n':
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
    df = df._append(pd.Series({"translation": translation, "mode": mode,"da":da,"word":word}), ignore_index=True)

def save_result(test, points, rounds):
    """
    Saves the result of a test in the results file.
    """
    if config_loaded and len(get_config('results_file'))>0:
        row = ','.join([datetime.today().strftime('%Y-%m-%d-%H:%M:%S'), get_config('profile'),test,str(points),str(rounds)])
        row = ''.join([row, '\n'])
        with open (get_config('results_file'), 'a') as f:
            f.write(row)
    print("Results saved.")

def save_weights(file):
    global df
    global weights_updated_not_saved
   
    da = pd.DataFrame(df.filter(items=['translation','_expression','_weight']))

    # if data exists, load and update it first. If it doesn't, just make the current selection the contents to write.
    if path.exists(file):
        de = pd.read_csv(file)

        if '_weight' in de.columns:
            de.rename({'_weight':'_weight_ex'}, axis=1,inplace=True)

        de = de.merge(da, how='outer', left_on=['translation','_expression'], right_on =['translation','_expression'])
        
        if '_weight' in de.columns:
            de['_weight'] = de['_weight'].fillna(de['_weight_ex'])

        if '_weight_ex' in de.columns:
            de.drop('_weight_ex', axis=1, inplace=True)
    else:
        de = da

    de.to_csv(file, index=False)
    weights_updated_not_saved=False
    print('Weights saved. ({0} words)'.format(len(de)))

def word_memorizer(count_of_words:int):
    """
    Shows some words
    """
    global df
    global loaded_files
    # raise error if no vocabulary is loaded 
    if loaded_files==[]:
        raise ValueError("No vocabulary has been loaded.")

    output_decorator("Word memorizer", 4)

    sleep_time_seconds = 4

    if count_of_words<1:
        return

    if len(df) < count_of_words:
        count_of_words = len(df) 

    # set up test words
    rnd = random.choices(population = df.index,weights = df._weight, k = count_of_words)

    # build dictionary
    mem = dict({})
    for i in rnd:
        mem[i] = {}
        mem[i]['Translation'] = df.translation[i]
        mem[i]['Word'] = df._expression[i]
        mem[i]['Mode'] = decode_mode(df['mode'][i])

    # show the words
    for i, v in mem.items():
        row = "{0} {1} {2}".format(mem[i]['Mode'].ljust(30), mem[i]['Translation'].ljust(30), mem[i]['Word'].ljust(30))
        print("")
        print(row)
        time.sleep(sleep_time_seconds)

    print("Word memorizer completed.")
        

def test_1(count_of_words:int):
    """
    Test 1 tests your writing skills and knowledge
    """
    global df
    
    output_decorator("Test 1", 4)

    if count_of_words<1:
        return

    if len(df) < count_of_words:
        count_of_words = len(df) 

    # set up test words
    rnd = random.choices(population = df.index,weights = df._weight, k = count_of_words)
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

    evaluations = [solutions[i].strip() == responses[i].strip() for i in range(0, len(translations))]
    res = round(sum([int(i) for i in evaluations])/len(translations)*100, 1)
    dres = pd.DataFrame(data=zip(translations, solutions, responses, [int(i) for i in evaluations]),
                        columns = ['Word', 'Solution', 'Response', 'Point'])
    output_decorator('Results', 6)

    print ("Your result is {0}%, {1} out of {2}".format(res, sum(dres.Point),len(dres))) 
    save_result('Test 1', res, len(translations))

    # update weights
    update_weights(dres)

    if dres.Point.sum() != len(dres):
        output_decorator("Errors",6)
        print(dres[dres['Point']==0].filter(items=['Word','Response', 'Solution']))

    output_decorator("",0, 'end') 

def test_2(count_of_words:int):
    """multiple choice test"""
    global df
    
    output_decorator("Test 2 - Multiple choice", 4)

    if count_of_words<1:
        return
    
    if len(df) < count_of_words:
        count_of_words = len(df) 
        
    letters = ['a','b','c','d']

    rnd = random.choices(population = df.index,weights = df._weight, k = count_of_words)
    translations = [df['translation'][i] for i in rnd]
    solutions = [df['_expression'][i] for i in rnd]
    
    # build the dict:

    questions_dict = {}
    for idx,val in enumerate(rnd):
        
        #shuffle the letters
        random.shuffle(letters)

        # select 3 words that are not the asked word
        rnd_alt = random.choices(population =df.index, k = 3)
        rnd_alt_solutions = [df['_expression'][i] for i in rnd_alt]
        question_dict = {}
        question_dict[letters[0]]= solutions[idx]
        
        for f in range(0, 3):
            question_dict[letters[f+1]] = rnd_alt_solutions[f]

        questions_dict[idx+1]={}
        questions_dict[idx+1]['options'] = question_dict
        questions_dict[idx+1]['question'] = translations[idx]
        questions_dict[idx+1]['solution'] = solutions[idx]
        questions_dict[idx+1]['solution_choice'] = letters[0]
        questions_dict[idx+1]['response'] = ''

        

    # collect the answers by looping through the dict
    for key, dictvalue in questions_dict.items():
        # build padded row of choices
        row = '     '.join(["{0}) {1}".format(x[0], x[1].ljust(20)) for x in list(sorted(dictvalue['options'].items()))])
        print("{0}:".format(dictvalue['question']))
        print(row)
        response = input ("Select option: ")
        questions_dict[key]['response'] = response

    # show results
    results = pd.DataFrame([(questions_dict[x]['question'], 
                             questions_dict[x]['solution'],
                             questions_dict[x]['solution_choice'], 
                             questions_dict[x]['response'], 
                             int(questions_dict[x]['solution_choice']==questions_dict[x]['response'])) for x in questions_dict.keys()],
                             columns = ['Word', 'Solution','Solution Choice', 'Response', 'Point'])
    
    if sum(results.Point) != len(results):
        output_decorator('Errors',6)
        print(results[results.Point!=1])

    res = round(sum(results.Point)/len(results)*100,1)
    print ("Your result is {0}%, {1} out of {2}".format(res, sum(results.Point),len(results))) 
    update_weights(results)
    save_result('Test 2', res, len(results))

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

if config_loaded and get_config("autostart_test_selector")=="true":
    test_selector()