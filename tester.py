import vocab as v

#vv = v.Vocabulary('dict.yaml')
#print(len(vv.items()))
w = v.Word('noun')
w.update_from_dict({'Ergebnis': {'date_added': '2024-11-17', 'plural': 'Ergebnisse', 'tags': ['vocabulary_Pg_01', 'exam', 'project'], 'translations': {'hungarian': ['eredmény']}}})
print(w.items())
#vv.save()
