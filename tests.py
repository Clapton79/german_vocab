
from vocab import *
from pprint import pprint
from datetime import datetime

#print(get_available_tests())

v = Vocabulary('new_dict.yaml')

# w = Word('noun')
# w.update()
# pprint(w.items())
# v.add(w)

# v.save()
# v.backup()
#print(list(v.filter_by_class('noun')))
w = v.filter_by_class_and_tag('noun')
v.append_tags_to_words(list(w),['core'])
print(list(v.filter_by_class_and_tag('noun','core')))
print(list(v.filter_by_class_and_tag('noun')))
#print(list(v.filter_by_topic_and_class('noun','building')))

#pprint([(x,dtl['date_added']) for x, dtl in v.vocab.items()])
# #@@@@@@@@@@@ Test tester
# t = LanguageTest(2,"verb conjugation",v)
# t.run()
# t.show_results()
#'verb conjugation', 'imperative verb form', 'noun translation', 'noun plural form', 'definite article', 'translation'
#v.vocab['sodass']['date_added']=format(datetime.now(),"%Y-%m-%d")
#pprint([(x,dtl['date_added']) for x, dtl in v.vocab.items()])
#v.save_as()
