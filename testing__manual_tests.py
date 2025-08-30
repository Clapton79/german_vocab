from vocab import *
import os
from vocab_utilities import *
import sys


os.environ['VOCAB_LOG_LEVEL'] = "DEBUG"
os.environ['VOCAB_LOG_TO_SCREEN'] = "True"
vv = Vocabulary('dict.yaml')
# get verbs
# word='abgebaut'
# print(get_first_vowel(word))
# word='gegeben'
# print(get_first_vowel(word))
def feature_vowel_extraction_verbs():
    verbs = vv.filter(word_class='verb')
    counter = 0
    vowel_journeys_1=[]
    vowel_journeys_2=[]
    for verb in verbs:
        conjugations_prae = vv.vocab[verb].get('conjugations', {}).get('Präsens', [])
        conjugations_praet = vv.vocab[verb].get('conjugations', {}).get('Präteritum', [])
        conjugations_perf = vv.vocab[verb].get('conjugations', {}).get('Perfekt', [])
        
        if len (conjugations_prae)<3 or len(conjugations_praet)<3 or len(conjugations_perf)<3:
            continue

        vj_1 = get_first_vowel(conjugations_prae[0])
        vj_2 = get_first_vowel(conjugations_praet[0])
        vj_3 = get_first_vowel(conjugations_perf[0].split(" ")[-1])

        #if vj_1!=vj_2!=vj_3:
        vowel_journey_1 = f'{"vowel_journey_ppp_"}{vj_1}->{vj_2}->{vj_3}'
        vowel_journeys_1.append(vowel_journey_1)

        vj2_1 = get_first_vowel(conjugations_prae[0])
        vj2_2 = get_first_vowel(conjugations_prae[1])
        vj2_3 = get_first_vowel(conjugations_prae[2])
        vowel_journey_2 = f'{"vowel_journey_S123_"}{vj2_1}->{vj2_2}->{vj2_3}'
        #if vj2_1!=vj2_2!=vj2_3:
        vowel_journey_2 = f'{"vowel_journey_S123_"}{vj2_1}->{vj2_2}->{vj2_3}'
        vowel_journeys_2.append(vowel_journey_2)
        
        counter+=1
        # if counter >= 30:
        #     break
    print(list(set(vowel_journeys_1)))
    print(len(list(set(vowel_journeys_1))))
    print(list(set(vowel_journeys_2)))
    print(len(list(set(vowel_journeys_2))))
    print(counter)

def test_data_extractors():
    

    result = False
    questions = []
    solutions = []
    fail_msg = "Test failed"

    current_module = sys.modules['vocab']
    all_attributes = dir(current_module)
    callable_methods = [attr for attr in all_attributes if callable(getattr(current_module, attr)) and attr.startswith('data_selector')]
    
    for method_name in callable_methods:
        method = getattr(current_module, method_name)
        result,questions,solutions = method(10,vv)
        if result:
            print(f'Result: {bcolors.OKGREEN}{method_name} {result}{bcolors.ENDC}')
        else:
            print(f'Result: {bcolors.FAIL}{method_name} {result}{bcolors.ENDC}')


#test_data_extractors()

# a,b,c=data_selector_translation(5,vv)
# print (a,b,c)
num_questions=5
questions = [(x, random.choice(list(vv.vocab[x]['conjugations']))) for x in random.sample(list(vv.filter(word_class='verb')),k=num_questions)]
solutions = [vv.vocab[x[0]].get('conjugations').get(x[1]) for x in questions]
question_formatted = [f"{x[0]} in {x[1]}" for x in questions]


print(question_formatted)
print(solutions)
        