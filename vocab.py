import fileoperations as fo
import random 
from vfunctions import *
from datetime import datetime
from pprint import pprint


class Word():
    def __init__(self, word_class):
        self.word_class = word_class
        self.word_data = {}
        self.word_to_add = None
        self.date_added = format(datetime.now(), "%Y-%m-%d")
    
    def __str__(self):
        return self.word_to_add
        
    def items(self):
        return self.word_data
        
    def update(self):
        defaults = {'translation_language': 'hungarian'}
        
        questions = {
            'noun':{
                'translations': {
                    'question': "What are the possible translations noun you'd like to add? (specify in list format: [list of translations]) ",
                    'type':  dict
                    
                },
                'tags':{
                    'question': "Specify a list of tags you'd like to add: ",
                    'type': list
                    },
                'plural': {
                    'question': "What is the plural of this noun? ",
                    'type': str
                },
                'definite_article':
                {
                    'question': "What is the definite article of this noun? ",
                    'type': str
                }
            }
        }    
        
        if self.word_class not in questions.keys():
            print(f"Unspecified word class: {self.word_class}")
            return
        
        self.word_to_add = input(f"What is the {self.word_class} you want to add?: ")
        
        for question, details in questions[self.word_class].items():
            response = input(details['question'])
            
            if question =='translations':
                response = dict({defaults['translation_language']: response.split(',')})
            
            if details['type'] == list:
                response = response.split(',')
                
            data_obj = details['type'](response)
            if not isinstance(data_obj, details['type']):
                print(f"Invalid response for {details['question']}. Expected {details['type'].__name__}")
                return
        
            self.word_data[question]=data_obj
            
        self.word_data['date_added']=self.date_added
    
    
class Vocabulary():
    def __init__(self, filename):
        self.filename = filename
        self.load_success = None
        vocab = fo.load_file(filename)
        self.vocab = vocab['words']
        self.custom_data = vocab['tags']
        self.nouns = [x for x, d in self.vocab.items() if d['class']=='noun']
        self.adjectives = [x for x, d in self.vocab.items() if d['class']=='adjective']

    # file operations
    def save(self, filename:str = None):
        if filename is None:
            filename = self.filename
            
        data = {"tags": self.custom_data, "words": self.vocab}
        fo.save_to_file(filename, data)
        
    def backup(self):
        fo.backup_file(self.filename)
        
    # item operations
    def __getitem__(self, key):
        if key in self.vocab:
            return self.vocab[key]
        else:
            return None
    def items(self):
        return self.vocab
    
    def verbs(self):
        return [x for x, d in self.items() if d['class']=='verb']
               
    def __str__ (self):
        return (str(self.vocab))
        
    def filter_by_class(self, word_class):
        for item, detail in self.vocab.items():
            if detail['class']== word_class:
                yield item
                
    def add(self,word:Word):
        if word in self.vocab.keys():
            print(f"This word is already in this vocabulary. Remove it first and try again.")
            return
        
        self.vocab[word.word_to_add] = word.word_data
        
       
##################################################################
#  Data selector functions
##################################################################
def data_selector_verb_conjugation(num_questions:int,vocabulary:Vocabulary):
    try:
        questions = [(x, random.choice(list(vocabulary[x]['conjugations']))) for x in random.choices(vocabulary.verbs,k=num_questions)]
        solutions = [vocabulary[x[0]].get('conjugations').get(x[1]) for x in questions]
        question_formatted = [f"{x[0]} in {x[1]}" for x in questions]
    except Exception as e: 
        print(str(e))
        return [False,[],[]]
    return [True, question_formatted, solutions]
    
def data_selector_translation(num_questions:int, vocabulary:Vocabulary):
    try:
        base = random.choices(list(vocabulary.vocab.keys()), k=num_questions)
        questions = [vocabulary[x].get('translations').get('hungarian')[0] for x in base]
        solutions = [" ".join([(vocabulary[x].get('definite_article') or ""),x]) for x in base]
    except Exception as e: 
        print(str(e))
        return [False,[],[]]
    return [True, questions, solutions]

def data_selector_definite_article(num_questions:int, vocabulary:Vocabulary):
    try:
        questions = random.choices(vocabulary.nouns, k=num_questions)
        solutions = [vocabulary.vocab[x].get("definite_article") for x in questions]
    except: 
        return [False,[],[]]
    return [True, questions, solutions]

def data_selector_noun_plural(num_questions:int, vocabulary:Vocabulary):
    try:
        questions = [" ".join([(vocabulary[x].get('definite_article') or ""),x]) for x in random.choices(vocabulary.nouns, k=num_questions)]
        solutions = [" ".join(["die",vocabulary[x].get("plural")]) for x in questions]
    except: 
        return [False,[],[]]
    return [True, questions, solutions]
    
def data_selector_noun_translation(num_questions:int, vocabulary:Vocabulary):
    try:
        base = random.choices(list(vocabulary.nouns), k=num_questions)
        questions = [vocabulary[x].get('translations').get('hungarian')[0] for x in base]
        solutions = [" ".join([(vocabulary[x].get('definite_article') or ""),x]) for x in base]
        
    except: 
        return [False,[],[]]
    return [True, questions, solutions]
        
def data_selector_imperative_verb_form(num_questions:int, vocabulary:Vocabulary):
    try:
        questions = random.choices(vocabulary.verbs, k=num_questions)
        solutions = [[f"{y.capitalize()}!" for y in vocabulary.vocab[x].get('imperative')] for x in questions]
    except: 
        return [False,[],[]]
    return [True, questions, solutions]
    
test_functions = {
    "verb conjugation": data_selector_verb_conjugation,
    "verb translation": "",
    "imperative verb form": data_selector_imperative_verb_form,
    "noun translation":data_selector_noun_translation,
    "noun plural form":data_selector_noun_plural,
    "definite article":data_selector_definite_article,
    "adjectives":"",
    "translation": data_selector_translation
}

def get_available_tests():
    return [key for key, item in test_functions.items() if item is not None and item != ""]
        
class LanguageTest():
    def __init__(self, num_questions: int, test_type:str, vocabulary:Vocabulary,immediate_correction:bool=False):
        self.test_type = test_type
        self.num_questions = num_questions
        self.answers = []
        self.results = []
        self.accuracy = None
        self.vocabulary = vocabulary
        self.immediate_correction = immediate_correction
        self.function = test_functions.get(test_type)
        
        if self.function is None:
            print(f"Unknown test type: {test_type}")
            
        self.test_load_success, self.questions, self.solutions = self.function(self.num_questions, self.vocabulary)
        
        if not self.test_load_success:
            print("Failed to load test data due to an internal error.")
            
    def run(self):
        if self.function is None or self.function == "" or not self.test_load_success:
            print("Unable to execute non-existent, not implemented or erroneous test")
            return
        for i, question in enumerate(self.questions):
            answer = input(f"{i+1}. {question}: ")
            answer = answer.split(';') if len(answer.split(';')) > 1 else answer
            answer = answer if answer else ""
            self.answers.append(answer)
            if self.immediate_correction and answer != self.solutions[i]:
                if isinstance(self.solutions[i],str):
                    print (f"{' '.ljust(5,' ')}{bcolors.FAIL}Correct answer: {bcolors.OKGREEN}{self.solutions[i]}{bcolors.ENDC}")
                    
                elif isinstance(self.solutions[i],list):
                    print (f"{' '.ljust(5,' ')}{bcolors.FAIL}Correct answer:")
                    for j, sol in enumerate(self.solutions[i]):
                        print(f"{''.ljust(10,' ')}{bcolors.OKGREEN}{sol}{bcolors.ENDC}")
            
        self.results = [self.solutions[i] == self.answers[i] for i in range(len(self.questions))]
        self.accuracy = round(sum(self.results) / len(self.results) * 100, 2)
        
    def show_results(self):
        print("==========================================")
        print(f"{'Test type: '.ljust(15,' ')}{self.test_type.title()}")
        print(f"{'Questions: '.ljust(15,' ')}{self.num_questions}")
        print(f"{'Accuracy: '.ljust(15,' ')}{self.accuracy}%")
        print("==========================================")
        print("Question\tSolution\tAnswer")
        print("==========================================")
        
        formats = [bcolors.OKGREEN if x else bcolors.FAIL for x in self.results]
        
        for i, question in enumerate(self.questions):
            
            solution_type = type(self.solutions[i])
            answer_type = type(self.answers[i])
            
            # default case: str 
            if solution_type == str and solution_type == answer_type:
                print(f"{i+1}. {question.ljust(10,' ')}\t{bcolors.OKGREEN}{self.solutions[i].ljust(10,' ')}{bcolors.ENDC}\t{formats[i]}{self.answers[i]}{bcolors.ENDC}")
            
            # extra case: matching lists
            elif solution_type == list and solution_type == answer_type:
                print(f"{i+1}. {question.ljust(10,' ')}")
                compare_two_lists(self.solutions[i], self.answers[i], no_header=True, padding_default=16)
                

    
    
            
    