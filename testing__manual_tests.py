import vocab as v
import os

os.environ['VOCAB_LOG_LEVEL'] = "DEBUG"
os.environ['VOCAB_LOG_TO_SCREEN'] = "True"
voc = v.Vocabulary('dict.yaml')

word_data = {'Ergebnis': {'class': 'noun', 'date_added': '2024-11-17',
                          'plural': 'Ergebnisse', 
                           'tags': ['vocabulary_Pg_01', 'exam', 'project'], 'translations': {'hungarian': ['eredmény']}},
            'lesen' : {'class': 'verb', 'date_added': '2024-12-01',
                        'tags': ['vocabulary_Pg_01', 'core', 'life'],
                        'translations': {'hungarian': ['olvas']},
                        'imperative': ['lies','lesen','liest','lesen'],
                        'prepositions': [],
                        }
            }
# word_data = {'lesen': {'class': 'verb', 'date_added': '2024-12-01',
#                                                'tags': ['vocabulary_Pg_01', 'core', 'life'],
#                                                'translations': {'hungarian': ['olvas']},
#                                                'imperative': ['lies','lesen','liest','lesen'],
#                                                'prepositions': [],
#                                                }}
                                            
for item in word_data.keys():
    w = v.Word(word_data[item]['class'])
    w.update_from_dict({item:word_data[item]})
    if w.word_class=='noun':
        w.get_word_definite_article()
    elif w.word_class=='verb':
        w.get_conjugations()
    
    #w.check_structure()
    voc.add(w, overwrite=False)
    #print("vocabulary check result: ", voc.check_structure())
print(f"load success {voc.load_success}")
voc.save('new_dict.yaml',fileformat='ruamel')


 