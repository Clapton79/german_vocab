import itertools
from datetime import datetime

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
        weights = {}
        for word,test in itertools.product(words,tests):
            if word not in weights.keys():
                weights[word] = {}
                
            weights[word][test]={'last_seen': format(datetime.now(),'%Y-%m-%d'),'weight': 100}
        
        self_weights = self.weights.copy()
        weights.update(self_weights)           
        self.weights.update(weights)
     
    def save(self,filename:str=""):
        if filename == "":
            filename = self.filename
            
        save_to_file(filename, self.weights, 'ruamel')
        
     