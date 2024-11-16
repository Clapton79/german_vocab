import fileoperations as fo
import random 
from os import getenv, path
from applogger import logger
from vfunctions import *
from datetime import datetime
import scraper

class Word():
    __slots__ = ['word_class','word_data','word_text','date_added','definite_article']
    def __init__(self, word_class):
        self.word_class = word_class
        self.word_data = {}
        self.word_text = None
        self.date_added = format(datetime.now(), "%Y-%m-%d")
        logger.debug(f"Initialized WordClass {self.word_class}")
    
    def __str__(self):
        return self.word_text
        
    def items(self):
        return self.word_data
    
    def get_definite_article(self):
        if self.word_class != 'noun':
            return None
        else:
            return scraper.get_definite_article(self.word_text)
            
    def update_from_dict(self, data_dict:dict): 
        self.word_class = data_dict['word_class']   
        self.word_text = data_dict['word_text']
        self.word_data = data_dict['word_data']
        self.date_added = format(datetime.now(), "%Y-%m-%d")    
    
    def convert_to_dict(self):
        word_dict = {self.word_text: {'class': self.word_class}}
        for key, value in self.word_data.items():
            word_dict[self.word_data][key] = value
        return word_dict
        
    def check_structure(self):
        dict_to_check = self.convert_to_dict()
        dict_model = get_vocabulary_model()
        
        return check_dict_structure(dict_to_check, dict_model,self.word_text)
        
    def update(self):
        defaults = {'translation_language': 'hungarian'}
        
        questions = {
            'noun':{
                'translations': {
                    'question': "What are the translations you'd like to add in the selected language? (specify in list format) ",
                    'type':  dict
                },
                'tags':{
                    'question': "Specify a list of tags you'd like to add: (topic, specialty)",
                    'type': list
                    },
                'plural': {
                    'question': "What is the plural of this noun? ",
                    'type': str
                }
            },
            'verb': {
                'translations': {
                    'question': "What are the translations you'd like to add? (specify in dict format: [list of translations]) ",
                    'type':  dict
                },
                'tags':{
                    'question': "Specify a list of tags you'd like to add: (haben|sein, sich, ) ",
                    'type': list
                    },
                'prepositions':{
                    'question': "Specify a list of examples with prepositions:",
                    'type': list
                    }
                },
            'adjective': {
                'tags':{
                    'question': "Specify a list of tags you'd like to add: (topics) ",
                    'type': list
                    },
                'translations': {
                    'question': "What are the translations you'd like to add? (specify in list format: [list of translations]) ",
                    'type':  dict
                }
            },
            'conjunction': {
                'tags':{
                    'question': "Specify a list of tags you'd like to add: (topics) ",
                    'type': list
                    },
                'translations': {
                    'question': "What are the translations you'd like to add? (specify in list format: [list of translations]) ",
                    'type':  dict
                }
            },
            'adverb': {
                'tags':{
                    'question': "Specify a list of tags you'd like to add: (topics) ",
                    'type': list
                    },
                'translations': {
                    'question': "What are the translations you'd like to add? (specify in list format: [list of translations]) ",
                    'type':  dict
                }
            },
            'phrase': {
                'tags':{
                    'question': "Specify a list of tags you'd like to add: (topics) ",
                    'type': list
                    },
                'translations': {
                    'question': "What are the translations you'd like to add? (specify in list format: [list of translations]) ",
                    'type':  dict
                }
            }
        }    
        
        if self.word_class not in questions.keys():
            logger.error(f"Unspecified word class for recording data: {self.word_class}")
            return
        
        self.word_text = input(f"What is the {self.word_class} you want to add?: ")
        
        for question, details in questions[self.word_class].items():
            response = input(details['question'])
            
            if question =='translations':
                response = dict({defaults['translation_language']: response.split(',')})
            
            if details['type'] == list:
                response = response.split(',')
                
            data_obj = details['type'](response)
            if not isinstance(data_obj, details['type']):
                logger.error(f"Invalid response for {details['question']}. Expected {details['type'].__name__}")
                return
            
            self.word_data[question]=data_obj
            
            if self.word_class == 'noun':
                self.definite_article=self.get_definite_article()
            
        self.word_data['date_added']=self.date_added
        
    
class Vocabulary():
    __slots__ = ['filename','load_success','last_backupfile','vocab','custom_data']
    def __init__(self, filename:str=None):
        self.filename = filename
        self.load_success = None
        self.last_backupfile = None
        if filename is not None and path.isfile(filename):
            vocab = fo.load_file(filename)
            self.vocab, self.custom_data = vocab['words'],vocab['tags']
        else:
            self.vocab = {}
            self.custom_data = {}
            
        if len(self.vocab.keys()) > 0 or filename is None:
            self.load_success = True

    # file operations
    def save(self, filename:str = None):
        if filename is None:
            filename = self.filename
        
            
        data = {"tags": self.custom_data, "words": self.vocab}
        fo.save_to_file(filename, data)
        
    def backup(self):
        self.last_backupfile = fo.backup_file(self.filename)
        
    # item operations
    def __getitem__(self, key):
        if key in self.vocab:
            return self.vocab[key]
        else:
            return None
    def items(self):
        return self.vocab
    
    def __str__ (self):
        return (str(self.vocab))
        
    def filter_by_class_and_tag(self, word_class:str, tag:str=None):
        for item, detail in self.vocab.items():
            if detail['class'] == word_class:
                if tag is None or tag in detail['tags']:
                    yield item
                
    def add(self,word:Word):
        if word in self.vocab.keys():
            logger.error(f"The word {word.word_text} is already in this vocabulary. Remove it first and try again.")
            return
        
        self.vocab[word.word_text] = word.word_data
        
    def remove(self,word:Word):
        if word in self.vocab.keys():
            del self.vocab[word.word_text]
        else:
            logger.error(f"The word {word.word_text} is not in this vocabulary.")
    
    #collection operations
    def append_tags_to_words(self,words:list,tags:list):
        for word in words:
            if word in self.vocab.keys():
                for tag in tags:
                    if tag not in self.vocab[word]['tags']:
                        self.vocab[word]['tags'].append(tag)
            else:
                logger.error(f"The word {word} is not in this vocabulary.")
    
    def check_structure(self):
        try:
            model = get_vocabulary_model()
            results = []
            for word in self.vocab.keys():
                logger.debug(f"Checking {word} data quality.")
                dict_to_check = dict(self.vocab[word])
                dict_model = dict(model[self.vocab[word].get('class')])
                result = check_dict_structure(dict_to_check, dict_model,word)
                results.append(result)
            
            if len(results) == 0:
                logger.warning("Not able to test data quality.")  
                return False  
            elif len(results) != sum(results):
                logger.warning("Data quality issues found in vocabulary.")
                return False
            else:
                logger.info(f"No data quality issues found in vocabulary ({len(results)} words)")
                return True
                
        except Exception as e:
            logger.error(f"Error in checking vocabulary structure: {str(e)}")
            return False
     
    def topics(self):
        topics = []
        for word, value in self.vocab.items():
            topics += value.tags
                
        return list(set(topics))
                     
def merge(source_vocabulary:Vocabulary, target_vocabulary:Vocabulary):
    for word, detail in source_vocabulary.vocab.items():
        if word not in target_vocabulary.vocab.keys():
            target_vocabulary.vocab[word] = detail    
            
    target_vocabulary.custom_data.append(source_vocabulary.custom_data)
##################################################################
#  Data selector functions
##################################################################
def data_selector_verb_conjugation(num_questions:int,vocabulary:Vocabulary):
    try:
        questions = [(x, random.choice(list(vocabulary[x]['conjugations']))) for x in random.choices(list(vocabulary.filter_by_class_and_tag('verb')),k=num_questions)]
        solutions = [vocabulary[x[0]].get('conjugations').get(x[1]) for x in questions]
        question_formatted = [f"{x[0]} in {x[1]}" for x in questions]
    except Exception as e: 
        logger.error(str(e))
        return [False,[],[]]
    return [True, question_formatted, solutions]
    
def data_selector_translation(num_questions:int, vocabulary:Vocabulary):
    try:
        base = random.choices(list(vocabulary.vocab.keys()), k=num_questions)
        questions = [vocabulary[x].get('translations').get('hungarian')[0] for x in base]
        solutions = [" ".join([(vocabulary[x].get('definite_article') or ""),x]) for x in base]
    except Exception as e: 
        logger.error(str(e))
        return [False,[],[]]
    return [True, questions, solutions]

def data_selector_definite_article(num_questions:int, vocabulary:Vocabulary):
    try:
        questions = random.choices(list(vocabulary.filter_by_class_and_tag('noun')), k=num_questions)
        solutions = [vocabulary.vocab[x].get("definite_article") for x in questions]
    except Exception as e:  
        logger.error(str(e))
        return [False,[],[]]
    return [True, questions, solutions]

def data_selector_noun_plural(num_questions:int, vocabulary:Vocabulary):
    try:
        questions = [" ".join([(vocabulary[x].get('definite_article') or ""),x]) for x in random.choices(list(vocabulary.filter_by_class_and_tag('noun')), k=num_questions)]
        solutions = [" ".join(["die",vocabulary[x].get("plural")]) for x in questions]
    except Exception as e:  
        logger.error(str(e))
        return [False,[],[]]
    return [True, questions, solutions]
    
def data_selector_noun_translation(num_questions:int, vocabulary:Vocabulary):
    try:
        base = random.choices(list(vocabulary.filter_by_class_and_tag('noun')), k=num_questions)
        questions = [vocabulary[x].get('translations').get('hungarian')[0] for x in base]
        solutions = [" ".join([(vocabulary[x].get('definite_article') or ""),x]) for x in base]  
    except Exception as e:  
        logger.error(str(e))
        return [False,[],[]]
    return [True, questions, solutions]
        
def data_selector_imperative_verb_form(num_questions:int, vocabulary:Vocabulary):
    try:
        questions = random.choices(list(vocabulary.filter_by_class_and_tag('verb')), k=num_questions)
        solutions = [[f"{y.capitalize()}!" for y in vocabulary.vocab[x].get('imperative')] for x in questions]
    except Exception as e:  
        logger.error(str(e))
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
    __slots__ = ['test_type','num_questions','answers','results','accuracy','vocabulary','immediate_correction','function','test_load_success','questions','solutions']
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
            logger.error(f"Unknown language test type: {test_type}")
            
        self.test_load_success, self.questions, self.solutions = self.function(self.num_questions, self.vocabulary)
        logger.debug(f"Language test {self.test_type} initialized.")
        
        if not self.test_load_success:
            logger.error(f"Failed to load test {self.test_type} data due to an internal error.")
    
    def __is_ready_to_run(self):
        return self.function is not None and self.function != "" and self.test_load_success

    def __get_answer(self, index, question):
        answer = input(f"{index + 1}. {question}: ")
        return answer.split(';') if len(answer.split(';')) > 1 else answer or ""

    def __check_immediate_correction(self, index, answer):
        if self.immediate_correction and answer != self.solutions[index]:
            self.__display_correct_answer(index)

    def __display_correct_answer(self, index):
        correct_answer = self.solutions[index]
        if isinstance(correct_answer, str):
            print(f"{' '.ljust(5, ' ')}{bcolors.FAIL}Correct answer: {bcolors.OKGREEN}{correct_answer}{bcolors.ENDC}")
        elif isinstance(correct_answer, list):
            print(f"{' '.ljust(5, ' ')}{bcolors.FAIL}Correct answer:")
            for sol in correct_answer:
                print(f"{''.ljust(10, ' ')}{bcolors.OKGREEN}{sol}{bcolors.ENDC}")

    def __calculate_results(self):
        try:
            self.results = [self.solutions[i] == self.answers[i] for i in range(len(self.questions))]
            self.accuracy = round(sum(self.results) / len(self.results) * 100, 2)   
        except Exception as e:
            logger.error(f"Failed to calculate results due to an internal error: {str(e)}")
    
    def save_results(self, filename):
        try:
            with open (filename, 'a') as f:
                f.write(f"{datetime.datetime.now().strftime},{self.test_type.title()},{self.num_questions},{self.accuracy}")
        except IOError as e:
            logger.error(f"Error saving results to file: {filename} ({str(e)})")
     
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
                
            else:
                print(f"{i+1}. {question.ljust(10,' ')}")
                for solution in self.solutions[i]:
                    print (f"{''.ljust(16, ' ')}{bcolors.FAIL}{solution}{bcolors.ENDC}")
                
    def run(self):
        logger.debug("Running test")
        try:
            if not self.__is_ready_to_run():
                raise RuntimeError("Unable to execute non-existent, not implemented or erroneous test")

            for i, question in enumerate(self.questions):
                answer = self.__get_answer(i, question)
                self.answers.append(answer)
                self.__check_immediate_correction(i, answer)

            self.__calculate_results()
            self.show_results()
        except Exception as e:
            logger.error(f"Failed to run test due to an internal error: {str(e)}")
    
    
            
    