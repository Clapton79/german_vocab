import vocab as v

w = v.Word('noun')
word_data = {'Ergebnis': {'class': 'noun', 'date_added': '2024-11-17',
                          'plural': 'Ergebnisse', 
                           'tags': ['vocabulary_Pg_01', 'exam', 'project'], 'translations': {'hungarian': ['eredmény']}}}
                          
w.update_from_dict(word_data)
w.get_definite_article()
print(w.convert_to_dict())
w.check_structure()
print(w.dq, w.dq_list)