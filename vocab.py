import random 
from os import path
from applogger import logger
from vocab_utilities import *
from datetime import datetime
from pprint import pprint

class Word():
    __slots__ = ['word_class','word_data','word_text','date_added','definite_article','dq','dq_list']
    def __init__(self, word_class):
        self.word_class = word_class
        self.definite_article = ""
        self.word_data = {}
        self.word_text = None
        self.date_added = format(datetime.now(), "%Y-%m-%d")
        self.dq = ""
        self.dq_list = []
        logger.debug(f"Initialized WordClass {self.word_class}")
    
    def __str__(self):
        return str(self.word_text)
        
    def items(self):
        if self.word_class == "noun":
            return {self.word_text: {'class': self.word_class,'definite_article':self.definite_article ,**self.word_data}}
        else:
            return {self.word_text: {'class': self.word_class, **self.word_data}}
    
    def get_definite_article(self):
        if self.word_class =='noun':
            self.definite_article = get_definite_article(self.word_text)
    
    def get_conjugations(self):
        logger.debug(f"Getting conjugations for {self.word_text}")
        if self.word_class!= 'verb':
            return None
        else:
            webdata = get_conjugation(self.word_text)
            logger.debug(webdata)
            self.word_data['conjugations'] = webdata['conjugations']    
            self.word_data['imperative'] = webdata['imperative']
              
    def update_from_dict(self, data_dict:dict): 
        try:
            k = list(data_dict.keys())
            self.word_class = data_dict[k[0]]['class']
            self.word_text = k[0]
            self.word_data = data_dict[k[0]]
            self.date_added = format(datetime.now(), "%Y-%m-%d")    
        except Exception as e:
            print(str(e))
            logger.error(f"Error updating Word data: {str(e)}")
            return False
    
    def convert_to_dict(self,no_key:bool=False):
        try:
            if self.word_class == 'noun' and not no_key:
                word_dict = {self.word_text: {'class': self.word_class, 'definite_article':self.definite_article,**self.word_data}}
            elif self.word_class == 'noun' and no_key:
                word_dict = {'class': self.word_class, 'definite_article':self.definite_article,**self.word_data}
            elif not no_key:
                word_dict = {self.word_text: {'class': self.word_class,
                                              **self.word_data}}
            else:
                word_dict = {'class': self.word_class,**self.word_data}
            return word_dict
            
        except Exception as e:
            logger.error(f"Error converting {self.word_text} to dict: {str(e)}")
            return None
        
    def check_structure(self):
        dict_to_check = self.convert_to_dict(no_key=True)
        dict_model = get_vocabulary_model(self.word_class)
        
        self.dq, self.dq_list =  check_dict_structure(dict_to_check, dict_model,self.word_text,verbose=True)
        
    def update(self):
        defaults = {'translation_language': 'hungarian'}
        
        questions = {
            'noun':{
                'translations': {
                    'question': "What are the translations you'd like to add in the selected language? (specify in list format)",
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
                    'question': "What are the translations you'd like to add? (specify in dict format: [list of translations])",
                    'type':  dict
                },
                'tags':{
                    'question': "Specify a list of tags you'd like to add: (haben|sein, sich, )",
                    'type': list
                    },
                'prepositions':{
                    'question': "Specify a list of examples with prepositions:",
                    'type': list
                    }
                },
            'adjective': {
                'tags':{
                    'question': "Specify a list of tags you'd like to add: (topics)",
                    'type': list
                    },
                'translations': {
                    'question': "What are the translations you'd like to add? (specify in list format: [list of translations])",
                    'type':  dict
                }
            },
            'conjunction': {
                'tags':{
                    'question': "Specify a list of tags you'd like to add: (topics)",
                    'type': list
                    },
                'translations': {
                    'question': "What are the translations you'd like to add? (specify in list format: [list of translations])",
                    'type':  dict
                }
            },
            'adverb': {
                'tags':{
                    'question': "Specify a list of tags you'd like to add: (topics)",
                    'type': list
                    },
                'translations': {
                    'question': "What are the translations you'd like to add? (specify in list format: [list of translations])",
                    'type':  dict
                }
            },
            'phrase': {
                'tags':{
                    'question': "Specify a list of tags you'd like to add: (topics)",
                    'type': list
                    },
                'translations': {
                    'question': "What are the translations you'd like to add? (specify in list format: [list of translations])",
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
        try:
            self.filename = filename
            self.load_success = None
            self.last_backupfile = None
            self.vocab = {}
            self.custom_data = {}
            
            if filename is not None and path.isfile(filename):
                vocab = load_file(filename)
                if vocab is None or len(vocab) == 0:
                    logger.error("No vocabulary data found in file.")
                    self.load_success = False
                    self.filename = None
                    
                else:
                    self.vocab, self.custom_data = vocab.get('words'),vocab.get('tags')
                    self.load_success = True
        
        except Exception as e:
            logger.error(f"Error initializing vocabulary: {str(e)}")

    # file operations
    def save(self, filename:str = None,fileformat:str = None,overwrite:bool=False):
        if filename is None:
            filename = self.filename
        try:
            safe = False
            if fileformat is None:
                fileformat = 'json' if filename.endswith('.json') else 'ruamel'

            
            data = {"tags": self.custom_data, "words": self.vocab}
            save_to_file(filename, data, fileformat,safe=safe,overwrite=overwrite)
            
        except Exception as e:
            logger.error(f"Could not save vocabulary to file: {str(e)}")
        
    def backup(self):
        self.last_backupfile = backup_file(self.filename)
        
    # item operations
    def __getitem__(self, key):
        return self.vocab.get(key)
        
    def items(self):
        return self.vocab
    
    def words(self):
        return list(self.vocab.keys())
        
    def count(self):
        return len(self.vocab)
        
    def __str__ (self):
        return (str(self.vocab))

    def show_verbs(tag: str = None, word: str = None):
        """Displays words in the vocabulary, optionally filtered by class and tag."""
        try:
            words = self.filter(word_class='verb', tag=tag,word=word)
            if len(words)==0:
                print('No words selected')
            else:
                for w in words:
                    print(f'{w.ljust(10, " ")}{self.vocab[w]["translations"]["hungarian"][0]}')
        except Exception as e:
            logger.error(f"Error showing words: {str(e)}")

    # def filter_by_class_and_tag(self, word_class:str, tag:str=None):
    #     """Deprecated! Returns a list of words that have the specified class and tag."""
    #     try:
    #         result=[]
    #         for item, detail in self.vocab.items():
    #             if detail.get('class') == word_class:
    #                 if tag is None or tag in detail.get('tags', []):
    #                     result.append(item)
    #     except Exception as e:
    #         logger.error(f"Error filtering by class and tag: {str(e)}")
    #         return []
    #     return sorted(result)
    
    # def filter_by_class(self, word_class: str):
    #     """Deprecated! Returns a list of words that have the specified word class."""
    #     try: 
    #         if not word_class:
    #             return []
            
    #         result = [word for word, detail in self.vocab.items() 
    #                 if detail.get('class') == word_class]
    #         return sorted(result)
    #     except Exception as e:
    #         logger.error(f"Error filtering by class '{word_class}': {str(e)}")
    #         return []

    # def filter_by_tag(self, tag: str) -> list:
    #     """Deprecated! Returns a list of words that have the specified tag."""
    #     try:
    #         if not tag:
    #             return []
    #         result = []
    #         result = [word for word, detail in self.vocab.items() 
    #                 if tag in detail.get('tags', [])]
    #         # for word, detail in self.vocab.items():
    #         #     if tag in detail.get('tags', []):
    #         #         result.append(word)
    #         return sorted(result)
    #     except Exception as e:
    #         logger.error(f"Error filtering by tag '{tag}': {str(e)} iteration: {word}")
    #         return []

    # def filter_by_class_and_tag(self, word_class: str, tag: str) -> list:
    #     """Deprecated! Returns a list of words that have the specified class and tag."""
    #     try:
    #         if not word_class:
    #             return []
            
    #         result = []
    #         result = [word for word, detail in self.vocab.items() if detail.get('class') == word_class and tag in detail.get('tags',[])]
            
    #         return sorted(result)
    #     except Exception as e:
    #         logger.error(f"Error filtering by class '{word_class}' and tag '{tag}': {str(e)}")
    #         return []

    def filter(self, word_class: str = None, tag: str = None, word: str = None) -> list:
        """
        Returns a list of words matching the specified criteria.
        
        Args:
            word_class: Filter by word class (optional)
            tags: List of tags to filter by (optional)
            word: Filters for a specific word (optional)
        """
        try:
            result = []
            
            if word_class is not None and tag is not None and word is None:  # 110
                result = [w for w in self.vocab if self.vocab[w].get('class') == word_class and tag in self.vocab[w].get('tags', [])]
            elif word_class is None and tag is not None and word is None:  # 010
                result = [w for w in self.vocab if tag in self.vocab[w].get('tags', [])]
            elif word_class is None and tag is None and word is not None:  # 001
                result = [w for w in self.vocab if w == word]
            elif word_class is not None and tag is None and word is None:  # 100
                result = [w for w in self.vocab if self.vocab[w].get('class') == word_class]
            elif word_class is None and tag is None and word is None:  # 000
                result = [w for w in self.vocab]
            elif word_class is not None and tag is None and word is not None:  # 101
                result = [w for w in self.vocab if self.vocab[w].get('class') == word_class and w == word]
            elif word_class is None and tag is not None and word is not None:  # 011
                result = [w for w in self.vocab if tag in self.vocab[w].get('tags', []) and w == word]
            elif word_class is not None and tag is not None and word is not None:  # 111
                result = [w for w in self.vocab if self.vocab[w].get('class') == word_class and tag in self.vocab[w].get('tags', []) and w == word]
            return sorted(result)
        except Exception as e:
            logger.error(f"Error filtering by multiple criteria: {str(e)}")
            return []

    def clone(self, word_class_filter: str = None, tag_filter: str = None, words_filter: list = None):
        """Creates a new instance of the vocabulary based on the given filters"""
        try:
            
            #filtered_words = self.filter(word_class=word_class_filter, tags=tag_filter)

            # Start with all words
            filtered_words = set(self.vocab.keys())
            
            # Apply word class filter
            if word_class_filter is not None:
                class_filtered = set(self.filter(word_class=word_class_filter))
                filtered_words = filtered_words.intersection(class_filtered)
            
            # Apply tag filter
            if tag_filter is not None:
                tag_filtered = set(self.filter(tag=tag_filter))
                filtered_words = filtered_words.intersection(tag_filtered)
            
            # Apply words filter (only keep words that are in the specified list)
            if words_filter is not None:
                words_filtered = set(words_filter)
                filtered_words = filtered_words.intersection(words_filtered)
            
            # Check if we have any words after filtering
            if len(filtered_words) == 0:
                raise ValueError("No words found matching the specified filters.")
            
            # Create the filtered vocabulary
            new_vocab = Vocabulary()
            new_vocab.vocab = {k: v for k, v in self.vocab.items() if k in filtered_words}
            new_vocab.custom_data = self.custom_data.copy()  
            
            # Create descriptive filename
            filter_parts = []
            if word_class_filter is not None:
                filter_parts.append(f"class:{word_class_filter}")
            if tag_filter is not None:
                filter_parts.append(f"tag:{tag_filter}")
            if words_filter is not None:
                filter_parts.append(f"words:{len(words_filter)}")
            
            filter_desc = ", ".join(filter_parts) if filter_parts else "no filters"
            new_vocab.filename = f'Cloned from {self.filename} ({filter_desc})'
            
            return new_vocab
            
        except Exception as e:
            logger.error(f"Error cloning vocabulary: {str(e)}")
            print(f"Error cloning vocabulary: {str(e)}")
            return None

    def add(self,word:Word,overwrite:bool=False):
        if word in self.vocab.keys() and overwrite == False:
            logger.error(f"The word {word.word_text} is already in this vocabulary. Remove it first and try again.")
            return
        
        self.vocab[word.word_text] = word.convert_to_dict(no_key=True)
    def remove(self,word:Word):
        if word in self.vocab.keys():
            del self.vocab[word.word_text]
    #collection operations
    def append_tag_to_words(self,tag:str,words:list=[]):
        
        if len(words) == 0:
            words = self.vocab.keys()
        else:
            words = [word for word in self.vocab.keys() if word in words]
            
        for word in words:
            self.vocab[word]['tags'] = list(set(self.vocab[word]['tags']+[tag]))
   
    def remove_tags_from_words(self, tag: str,words: list = []):
        """Removes a parameter tag from a list of words or all of the words in the vocabulary."""
        if len(words) == 0:
            words = self.vocab.keys()
        else:
            words = [word for word in self.vocab.keys() if word in words]
        
        for word in words:
            self.vocab[word]['tags'] = [t for t in self.vocab[word]['tags'] if t!= tag]
        
    def data_quality_errors(self) -> dict:
        try:
            model = get_vocabulary_model()
            results = {}
            for word in self.vocab.keys():
                logger.debug(f"Checking {word} data quality.")
                
                dict_to_check = dict(self.vocab[word])
                dict_model = dict(model[self.vocab[word].get('class')])
                if len(dict_model.keys()) == 0:
                    result,problems = False,['class']
                else:
                    result,problems = check_dict_structure(dict_to_check, dict_model,word,verbose=True, recursive=False)
                
                if len(problems) > 0: 
                    results[word]=problems
                    
            return results
                
        except Exception as e:
            print(f"Error in checking vocabulary structure of {word}: {str(e)}")
            return results
    def tags(self):
        tags = []
        for word,detail in self.vocab.items():
            word_tags = detail.get('tags')
            if word_tags is not None:
                tags+=word_tags

        return sorted(set(tags))
                     
def merge_vocabulary(source_vocabulary:Vocabulary, target_vocabulary:Vocabulary,overwrite:bool=False) -> None:
    try:
        for word, detail in source_vocabulary.vocab.items():
            if word not in target_vocabulary.vocab.keys() or overwrite:
                target_vocabulary.vocab[word] = detail 
         
    except Exception as e:
            logger.error(f"Error merging vocabularies: {str(e)}")
##################################################################
#  Data selector functions
##################################################################
def data_selector_verb_conjugation(num_questions:int,vocabulary:Vocabulary):
    try:
        questions = [(x, random.choice(list(vocabulary.vocab[x]['conjugations']))) for x in random.sample(list(vocabulary.filter(word_class='verb')),k=num_questions)]
        solutions = [vocabulary.vocab[x[0]].get('conjugations').get(x[1]) for x in questions]
        question_formatted = [f"{x[0]} in {x[1]}" for x in questions]
    except Exception as e: 
        logger.error(str(e))
        return [False,[],[]]
    return [True, question_formatted, solutions]


def data_selector_translation(num_questions:int, vocabulary:Vocabulary):
    try:
        base = random.sample(list(vocabulary.vocab.keys()), k=num_questions)
        questions = [vocabulary[x].get('translations').get('hungarian') for x in base]
        questions = [random.choice(z) if type(z) is list else z for z in questions]
        solutions = [(" ".join([(vocabulary[x].get('definite_article') or ""),x])).lstrip().rstrip() for x in base]
        
    except Exception as e: 
        logger.error(str(e))
        return [False,[],[]]
    return [True, questions, solutions]

def data_selector_inverse_translation(num_questions: int,vocabulary:Vocabulary):
    try:
        base = random.sample(list(vocabulary.vocab.keys()), k=num_questions)
        solutions = [vocabulary[x].get('translations').get('hungarian') for x in base]
        solutions = [random.choice(z) if type(z) is list else z for z in solutions]
        questions = [(" ".join([(vocabulary[x].get('definite_article') or ""),x])).lstrip().rstrip() for x in base]

    except Exception as e:
        logger.error(str(e))
        return [False,[],[]]
    return [True, questions, solutions]

def data_selector_definite_article(num_questions:int, vocabulary:Vocabulary):
    try:
        questions = random.sample(list(vocabulary.filter(word_class='noun')), k=num_questions)
        solutions = [vocabulary.vocab[x].get("definite_article") for x in questions]
    except Exception as e:  
        logger.error(str(e))
        return [False,[],[]]
    return [True, questions, solutions]

def data_selector_noun_plural(num_questions:int, vocabulary:Vocabulary):
    try:
        questions = [" ".join([(vocabulary[x].get('definite_article',"")),x]) for x in random.sample(list(vocabulary.filter(word_class='noun')), k=num_questions)]
        solutions = [" ".join(["die",vocabulary[x].get("plural")]) for x in questions]
    except Exception as e:  
        logger.error(str(e))
        return [False,[],[]]
    return [True, questions, solutions]
    
# def data_selector_noun_translation(num_questions:int, vocabulary:Vocabulary):
#     try:
#         base = random.sample(list(vocabulary.filter(word_class='noun')), k=num_questions)
#         questions = [vocabulary[x].get('translations').get('hungarian')[0] for x in base]
#         solutions = [" ".join([(vocabulary[x].get('definite_article') or ""),x]) for x in base]  
#     except Exception as e:  
#         logger.error(str(e))
#         return [False,[],[]]
#     return [True, questions, solutions]
        
def data_selector_imperative_verb_form(num_questions:int, vocabulary:Vocabulary):
    try:
        questions = random.sample(list(vocabulary.filter(word_class='verb')), k=num_questions)
        solutions = [f"{vocabulary.vocab[x].get('imperative','').capitalize()}!" for x in questions]
    except Exception as e:  
        logger.error(str(e))
        return [False,[],[]]
    return [True, questions, solutions]

# def data_selector_verb_translation(num_questions:int, vocabulary:Vocabulary):
#     try:
#         questions = random.choices(list(vocabulary.filter(word_class='verb')), k=num_questions)
#         solutions = [y[0] for y in vocabulary.vocab[x].get('translations').get('hungarian')]
#     except Exception as e:  
#         logger.error(str(e))
#         return [False,[],[]]
#     return [True, questions, solutions]

# def data_selector_adjective_translation(num_questions:int, vocabulary:Vocabulary):
#     try:
#         questions = random.choices(list(vocabulary.filter(word_class='adjective')), k=num_questions)
#         solutions = [vocabulary.vocab[x].get('translations').get('hungarian') for x in questions]
#         solutions = [z[0] if type(z) is list else z for z in solutions]
#     except Exception as e:  
#         logger.error(str(e))
#         return [False,[],[]]
#     return [True, questions, solutions]

def data_selector_verb_conjugation_praet(num_questions:int, vocabulary:Vocabulary):
    try:
        questions = [x for x in random.choices(list(vocabulary.filter(word_class='verb')),k=num_questions)]
        solutions = [vocabulary[x].get('conjugations').get('Präteritum')[:6] for x in questions]
    except Exception as e:
        print(str(e))
        logger.error(str(e))
        return [False,[],[]]
    return [True, questions, solutions]

def data_selector_verb_conjugation_perf(num_questions:int, vocabulary:Vocabulary):
    try:
        questions = random.sample(list(vocabulary.filter(word_class='verb')), k=num_questions)
        solutions = [vocabulary.vocab[y].get('conjugations').get('Perfekt') for y in questions]
    except Exception as e:
        logger.error(str(e))
        return [False,[],[]]
    return [True, questions, solutions]

def data_selector_verb_conjugation_praes(num_questions:int, vocabulary:Vocabulary):
    try:
        questions = random.choices(list(vocabulary.filter(word_class='verb')), k=num_questions)
        solutions = [[f"{y.capitalize()}!" for y in vocabulary.vocab[x].get('conjugation').get('Präsens') or []] for x in questions]
    except Exception as e:
        logger.error(str(e))
        return [False,[],[]]
    return [True, questions, solutions]

test_functions = {
    "verb conjugation Präteritum": data_selector_verb_conjugation_praet,
    "verb conjugation Perfekt": data_selector_verb_conjugation_perf,
    "verb conjugation Präsens": data_selector_verb_conjugation_praes,
    "imperative verb form": data_selector_imperative_verb_form,
    "noun plural form":data_selector_noun_plural,
    "definite article":data_selector_definite_article,
    "translation": data_selector_translation,
    "inverse translation":data_selector_inverse_translation
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
            print(f"Unknown language test type: {test_type}")

        self.test_load_success, self.questions, self.solutions = self.function(num_questions, vocabulary)
        logger.debug(f"Language test {self.test_type} initialized. ({len(self.questions)} words)")
        if not self.test_load_success:
            logger.error(f"Failed to load test {self.test_type} data due to an internal error.")
    
    def __is_ready_to_run(self):
        return self.function is not None and self.function != "" and self.test_load_success

    def __get_answer(self, index, question):
        answer = input(f"{index + 1}. {question}: ").rstrip().lstrip()
        return answer.split(',') if len(answer.split(',')) > 1 else answer or ""

    def __check_immediate_correction(self, index, answer):
        if self.immediate_correction and answer != self.solutions[index]:
            self.__display_correct_answer(index)

    def __display_correct_answer(self, index):
        correct_answer = self.solutions[index]
        if isinstance(correct_answer, str):
            print(f"{' '.ljust(5, ' ')}{bcolors.FAIL}Correct answer: {bcolors.OKGREEN}{correct_answer}{bcolors.ENDC}")
        elif isinstance(correct_answer, list):
            print(f"{' '.ljust(5, ' ')}{bcolors.FAIL}Correct answer:")
            compare_two_lists(correct_answer,self.answers[index])

    def __calculate_results(self):
        try:
            self.results = [self.solutions[i] == self.answers[i] for i in range(len(self.questions))]
            self.accuracy = round(sum(self.results) / len(self.results) * 100, 2)   
        except Exception as e:
            logger.error(f"Failed to calculate results due to an internal error: {str(e)}")
    
    def save_results(self, filename):
        try:
            # if filename does not exist, create and write header
            if not path.isfile(filename):
                with open (filename, 'w') as f:
                    f.write("Date,Test type,Number of questions,Accuracy\n")
            with open (filename, 'a') as f:
                f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')},{self.test_type.title()},{self.num_questions},{self.accuracy}\n")
        except IOError as e:
            logger.error(f"Error saving results to file: {filename} ({str(e)})")
     
    def show_results(self):
        try:
            questions_display = [f"{i+1}. {x}" for i,x in enumerate(self.questions)]
            max_length_q = max([len(x) for x in questions_display])+1
            max_length_a = max([len(x) for x in self.answers])+1
            max_length_s = max([len(x) for x in self.solutions])+1
            print("====================================================================================")
            print(f"{'Test type: '.ljust(15,' ')}{self.test_type.title()}")
            print(f"{'Questions: '.ljust(15,' ')}{self.num_questions}")
            print(f"{'Accuracy: '.ljust(15,' ')}{self.accuracy}%")
            print("====================================================================================")
            print(f"{'Question'.ljust(max_length_q,' ')}{'Solution'.ljust(max_length_s,' ')}{'Answer'.ljust(max_length_a,' ')}")
            print("====================================================================================")
            
            formats = [bcolors.OKGREEN if x else bcolors.FAIL for x in self.results]
            
            for i, question in enumerate(questions_display):

                solution_type = type(self.solutions[i])
                answer_type = type(self.answers[i])
                
                # default case: str 
                if solution_type == str and solution_type == answer_type:
                    print(f"{question.ljust(max_length_q,' ')}{bcolors.OKGREEN}{self.solutions[i].ljust(max_length_s,' ')}{bcolors.ENDC}{formats[i]}{self.answers[i]}{bcolors.ENDC}")
                
                # extra case: matching lists
                elif solution_type == list and solution_type == answer_type:
                    print(f"{i+1}. {question.ljust(max_length_q,' ')}")
                    compare_two_lists(self.solutions[i], self.answers[i], no_header=True, padding_default=16)
                    
                else:
                    print(f"{i+1}. {question.ljust(10,' ')}")
                    for solution in self.solutions[i]:
                        print (f"{''.ljust(max_length_s, ' ')}{bcolors.FAIL}{solution}{bcolors.ENDC}")
        except Exception as e:
            logger.error(f"Failed to show results due to an internal error: {str(e)}, {e.__traceback__}")
            print(str(e))
                      
    def run(self):
        logger.debug(f"Running test {self.test_type} with {self.num_questions} questions.")
        
        try:
            if not self.__is_ready_to_run():
                raise RuntimeError(f"Unable to execute non-existent, not implemented or erroneous test ({self.test_type})")
            divider_length = 40
            print("=" * divider_length)
            print(f"  * Test: {self.test_type.title()}")
            print("=" * divider_length)
            for i, question in enumerate(self.questions):
                answer = self.__get_answer(i, question)
                answer = answer if len(answer) > 0 else "-"
                self.answers.append(answer)
                self.__check_immediate_correction(i, answer)

            self.__calculate_results()
            self.save_results('test_results.csv')
            self.show_results()
        except Exception as e:
            print(str(e))
            logger.error(f"Failed to run test due to an internal error: {str(e)}")
    
    
            
    