# library configuration 
library_version = "1.0.1"

print ("Deutsch lernen {0}".format(library_version))
auto_load_default_vocabulary=True
default_vocabulary = 'vocab.csv'

import pandas as pd
import random 

df = pd.DataFrame()
res = pd.DataFrame()

# Vocabulary file handling
def load_file(file):
    """
    loads a vocabulary file
    """
    global df
    try:
        df = pd.read_csv(file)
        # transformations:
        # computed column: Full word
        df['expression']=df['da'].apply(decode_da)+ ' ' + df['word']
        
        print('Loaded file {0}'.format(file))
    except Exception as ex:
        print(str(ex))


def save_file(file):
    """
    exports a vocabulary file
    """
    df.to_csv(file, index=False)
# Vocabulary lookup commands
def decode_da(da:str):
    """
    converts definitive article id into definitive article
    """
    
    try:
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
    
    except IndexError:
        return ""

def set_convert(s:set):
    """
    concatenates set elements
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

    finally:
        return result

def translate_list(words:list, rev:str='str',da:str='da') -> list:
    """
    finds the first translation of all the input words
    """
    if rev not in ['rev','str']:
        raise ValueError('Argument "rev" invalid (can be rev or str)')
    if da not in ['da', 'n']:
        raise ValueError('Argument DA invalid (can be da or n)')
    # organise retrieved lists into one single list    
    return sum([translate(x, 'first',rev,da) for x in words],[])

# Vocabulary content commands
def add_word(word, da, translation, weight):
    """
    adds a word to the loaded dictionary
    """
    global df
    df = df._append(pd.Series({"Word":word,"DA":da, "Translation": translation, "Weight":weight}), ignore_index=True)

# Vocabulary test excercises
# Excercise 1 - simple word query
def test_1():
    count_of_words=3
    words = []
    solutions = []
    responses = []
    evaluation =[]

    global df
    try:
        if len(df) < count_of_words:
            count_of_words = len(df) 
        # set up test words
        
        rnd = [random.choice(range(0, count_of_words-1)) for i in range(1,count_of_words)]
        print(rnd)
       # words_raw = [df[i].word for i in range(0,len(rnd)-1)]
       # words = [' '.join ([df[i].da, df[i].word]) for i in range(0,len(rnd)-1)]
       # print (words)
        # set up their solutions 
        #solutions = [translate(word,'first', 'str','da') for word in words_raw]
        #solutions = sum(solutions, [])
        # input user solutions
        # for word in words:
        #     response = input('Translate {0}: '.format(word))
        #     responses.append(response)
        # evaluate
        # evaluation= [1 if responses[i]==solutions[i] else 0 for i in range(1,len(words))]
        # print(words)
        # print(responses)
        # print(solutions)
        # print(evaluation)
    finally:
        pass
    # except Exception as ex:
    #     print ("Failure.")
    #     print(str(ex))
        
# library load events
if auto_load_default_vocabulary:
     load_file(default_vocabulary)
