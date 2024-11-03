import fileoperations as fo
import random 
from vfunctions import *


class Vocabulary():
    def __init__(self, filename):
        self.filename = filename
        self.load_success = None
        vocab = fo.load_file(filename)
        self.vocab = vocab['words']
        self.custom_data = vocab['tags']
        self.verbs = [x for x, d in self.vocab.items() if d['class']=='verb']
        self.nouns = [x for x, d in self.vocab.items() if d['class']=='noun']
        self.adjectives = [x for x, d in self.vocab.items() if d['class']=='adjective']

##################################################################
#  Data selector functions
##################################################################
def data_selector_verb_conjugation(num_questions:int,vocabulary:Vocabulary):
    #try:
    questions = [(x,random.choice(vocabulary.get(x).get('conjugation').keys())) for x in random.choices(vocabulary.verbs,k=num_questions)]
    solutions = [vocabulary.vocab[x[0]].get('conjugation').get(x[1]) for x in questions]
    #except Exception as e: 
        # print(str(e))
        # return [False,[],[]]
    return [True, questions, solutions]
    
def data_selector_translation(num_questions:int, vocabulary:Vocabulary):
    try:
        questions = random.choices(list(vocabulary.vocab.keys()), k=num_questions)
        solutions = [vocabulary.vocab[x].get('translations').get('hungarian')[0] for x in questions]
    except: 
        return [False,[],[]]
    return [True, questions, solutions]

def data_selector_definite_article(num_questions:int, vocabulary:Vocabulary):
    try:
        questions = random.choices(vocabulary.nouns, k=num_questions)
        solutions = [vocabulary.vocab[x].get("definite_article") for x in questions]
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
    "verb conjugation": "",
    "verb translation": "",
    "imperative verb form": data_selector_imperative_verb_form,
    "noun translation":"",
    "noun plural form":"",
    "definite article":data_selector_definite_article,
    "adjectives":"",
    "translation": data_selector_translation
}

def get_available_tests():
    return [key.capitalize() for key, item in test_functions.items() if item is not None and item != ""]
        
class Test():
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