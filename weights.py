from ruamel.yaml import YAML as yaml2
from vocab_utilities import *
from vocab import *
import itertools
from pprint import pprint


filename = 'weights.yaml'

class Weight():
    def __init__(self, filename:str=None):
        self.filename = filename
        self.weights = dict({})
        
        if filename is not None:
            self.weights = load_file(filename, 'yaml')
            
    def create_schema_for_words(self, words:list=[]):
        """
        Creates a weights schema for the given words.
        """
        tests = [t for t, f in test_functions.items() if f !=""]
        #print(tests)
        weights = {}
        #print(list(itertools.product(words, tests)))
        for word,test in itertools.product(words,tests):
            if word not in weights.keys():
                weights[word] = {}
                
            weights[word][test]={'last_seen': '2024-12-24','weight': 100}
        pprint(weights)               
        self.weights.update(weights)
                
v = Vocabulary('dict.yaml')
    
wt = Weight()
wt.create_schema_for_words(v.words())
#pprint(wt.weights)