from vocab import *
import os
from vocab_utilities import *

os.environ['VOCAB_LOG_LEVEL'] = "DEBUG"
os.environ['VOCAB_LOG_TO_SCREEN'] = "True"
vv = Vocabulary('dict.yaml')
# get verbs
# word='abgebaut'
# print(get_first_vowel(word))
# word='gegeben'
# print(get_first_vowel(word))
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