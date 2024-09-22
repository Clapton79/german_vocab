from vocabularizer import *
from functions import *


def save_result(test, points, rounds):
    """
    Saves the result of a test in the results file.
    """
    if config_loaded and len(get_config('results_file'))>0:
        row = ','.join([datetime.today().strftime('%Y-%m-%d-%H:%M:%S'), get_config('profile'),test,str(points),str(rounds)])
        row = ''.join([row, '\n'])
        with open (get_config('results_file'), 'a') as f:
            f.write(row)
    print("Results saved.")


def word_memorizer(count_of_words:int, sleep_time_seconds:int=4, random_or_last:str='rnd'):
    """
    Shows some words for few seconds for you to memorize.
    """
    global df
    global loaded_files
    # raise error if no vocabulary is loaded 
    if loaded_files==[]:
        raise ValueError("No vocabulary has been loaded.")

    output_decorator("Word memorizer", 4)

    if count_of_words<1:
        return

    if len(df) < count_of_words:
        count_of_words = len(df) 

    rnd = []
    # set up test words
    if random_or_last=='rnd':
        rnd = random.choices(population = df.index,weights = df._weight, k = count_of_words)
    elif random_or_last=='last':
        rnd = list(df[-1*count_of_words:].index)
    elif random_or_last=='first':
        rnd = list(df[:count_of_words].index)

    # build dictionary
    mem = dict({})
    for i in rnd:
        mem[i] = {}
        mem[i]['Translation'] = df.translation[i]
        mem[i]['Word'] = f"{bcolor_da(df.da[i])}{df._expression[i]}{bcolors.ENDC}"
        mem[i]['Mode'] = decode_mode(df['mode'][i])

    # show the words
    for i, v in mem.items():
        row = "{0} {1} {2}".format(mem[i]['Mode'].ljust(30), mem[i]['Translation'].ljust(30), mem[i]['Word'].ljust(30))
        print("")
        print(row)
        time.sleep(sleep_time_seconds)

    print("Word memorizer completed.")
        

def test_1(word_mode:str = '',count_of_words:int=10):
    """
    Test 1 tests your writing skills and knowledge
    """
    global df
    
    output_decorator("Test 1", 4)

    if count_of_words<1:
        return

    if len(df) < count_of_words:
        count_of_words = len(df) 

    # set up test words
    #rnd = random.choices(population = df.index,weights = df._weight, k = count_of_words)
    rnd = random_choice(word_mode,count_of_words)
    translations = [df['translation'][i] for i in rnd]
    words = [df['word'][i] for i in rnd]
    solutions = [df['_expression'][i] for i in rnd]
    counts = [len(df[df['translation']==i]) for i in translations]

    responses= []
    for k in range(0,len(translations)):
        word = translations[k]
        c = len(df[df['translation']==word])
        match len(df[df['translation']==word]):
            case 0:
                hint = ""
            case 1:
                hint = ""
            case _:
                hint = "(hint: {0})".format(words[k][0])
        response = input("What is {0} in {1}{2}? ".format(word, language,hint)) or ""
        responses.append(str(response))

    evaluations = [solutions[i].strip() == responses[i].strip() for i in range(0, len(translations))]
    res = round(sum([int(i) for i in evaluations])/len(translations)*100, 1)
    dres = pd.DataFrame(data=zip(translations, solutions, responses, [int(i) for i in evaluations]),
                        columns = ['Word', 'Solution', 'Response', 'Point'])
    output_decorator('Results', 6)

    print ("Your result is {0}%, {1} out of {2}".format(res, sum(dres.Point),len(dres))) 
    save_result('Test 1', res, len(translations))

    # update weights
    update_weights(dres)

    if dres.Point.sum() != len(dres):
        output_decorator("Errors",6)
        print(dres[dres['Point']==0].filter(items=['Word','Response', 'Solution']))

    output_decorator("",0, 'end') 

def test_2(word_mode:str = '',count_of_words:int = 20):
    """Multiple choice test for translating"""
    global df
    
    output_decorator("Test 2 - Multiple choice", 4)

    if count_of_words<1:
        return
    
    if len(df) < count_of_words:
        count_of_words = len(df) 
        
    letters = ['a','b','c','d']

    rnd = random_choice(word_mode,count_of_words)
    translations = [df['translation'][i] for i in rnd]
    solutions = [df['_expression'][i] for i in rnd]
    
    if len(rnd)==0:
        raise ValueError(f"{bcolors.FAIL}No words found({decode_mode(word_mode)}).{bcolors.ENDC}")

    # build the dict:

    questions_dict = {}
    for idx,val in enumerate(rnd):
        
        #shuffle the letters
        random.shuffle(letters)

        # select 3 words that are not the asked word
        rnd_alt = random.choices(population =df.index[df.index!=idx], k = 3)
        rnd_alt_solutions = [df['_expression'][i] for i in rnd_alt]
        question_dict = {}
        question_dict[letters[0]]= solutions[idx]
        
        for f in range(0, 3):
            question_dict[letters[f+1]] = rnd_alt_solutions[f]

        questions_dict[idx+1]={}
        questions_dict[idx+1]['options'] = question_dict
        questions_dict[idx+1]['question'] = translations[idx]
        questions_dict[idx+1]['solution'] = solutions[idx]
        questions_dict[idx+1]['solution_choice'] = letters[0]
        questions_dict[idx+1]['response'] = ''

        
    # collect the answers by looping through the dict
    for key, dictvalue in questions_dict.items():
        # build padded row of choices
        row = '     '.join(["{0}) {1}".format(x[0], x[1].ljust(20)) for x in list(sorted(dictvalue['options'].items()))])
        print('')
        print(f"{bcolors.OKBLUE}{dictvalue['question']}{bcolors.ENDC}:")
        print(row)
        response = input (f"{bcolors.OKGREEN}Select option: {bcolors.ENDC}")
        questions_dict[key]['response'] = response

    # show results
    results = pd.DataFrame([(questions_dict[x]['question'], 
                             questions_dict[x]['solution'],
                             questions_dict[x]['solution_choice'], 
                             questions_dict[x]['response'], 
                             int(questions_dict[x]['solution_choice']==questions_dict[x]['response'])) for x in questions_dict.keys()],
                             columns = ['Word', 'Solution','Solution Choice', 'Response', 'Point'])
    
    if sum(results.Point) != len(results):
        output_decorator('Errors',6)
        print(results[results.Point!=1])

    res = round(sum(results.Point)/len(results)*100,1)

    match res < 85:
        case True:
            this_color = bcolors.FAIL
        case _:
            this_color = bcolors.ENDC

    print (f"{this_color}Your result is {res}%, {sum(results.Point)} out of {len(results)}{bcolors.ENDC}") 
    update_weights(results)
    save_result('Test 2', res, len(results))

def test_3(count_of_words:int = 10):
    """Multiple choice test for definitive articles."""
    global df
    
    output_decorator("Test 3 - Definitive article test", 4)

    if count_of_words<1:
        return
    
    if len(df) < count_of_words:
        count_of_words = len(df) 
        
    letters = ['a','b','c']
    definitive_article_choice = ['r','e','s']

    rnd = random_choice('n',count_of_words)
    words = [df['word'][i] for i in rnd]
    solutions = [df['da'][i] for i in rnd]

    if len(rnd)==0:
        raise ValueError(f"{bcolors.FAIL}No words found({decode_mode('n')}).{bcolors.ENDC}")

    # build the dict:

    questions_dict = {}
    for idx,val in enumerate(rnd):
        
        #shuffle the letters
        random.shuffle(letters)

        definitive_articles_alt = [decode_da(x) for x in definitive_article_choice if x!= solutions[idx]]
        random.shuffle(definitive_articles_alt)

        question_dict = {}
        question_dict[letters[0]]= decode_da(solutions[idx])
        
        for f in range(0, 2):
            question_dict[letters[f+1]] = definitive_articles_alt[f]

        questions_dict[idx+1]={}
        questions_dict[idx+1]['options'] = question_dict
        questions_dict[idx+1]['question'] = words[idx]
        questions_dict[idx+1]['solution'] = decode_da(solutions[idx])
        questions_dict[idx+1]['solution_choice'] = letters[0]
        questions_dict[idx+1]['response'] = ''

        
    # collect the answers by looping through the dict
    for key, dictvalue in questions_dict.items():
        # build padded row of choices
        row = '     '.join(["{0}) {1}".format(x[0], x[1].ljust(20)) for x in list(sorted(dictvalue['options'].items()))])
        print('')
        print(f"{bcolors.OKBLUE}{dictvalue['question']}{bcolors.ENDC}:")
        print(row)
        response = input (f"{bcolors.OKGREEN}Select option: {bcolors.ENDC}")
        questions_dict[key]['response'] = response

    # show results
    results = pd.DataFrame([(questions_dict[x]['question'], 
                             questions_dict[x]['solution'],
                             questions_dict[x]['solution_choice'], 
                             questions_dict[x]['response'], 
                             int(questions_dict[x]['solution_choice']==questions_dict[x]['response'])) for x in questions_dict.keys()],
                             columns = ['Word', 'Solution','Solution Choice', 'Response', 'Point'])
    
    if sum(results.Point) != len(results):
        output_decorator('Errors',6)
        print(results[results.Point!=1])

    res = round(sum(results.Point)/len(results)*100,1)

    match res < 85:
        case True:
            this_color = bcolors.FAIL
        case _:
            this_color = bcolors.ENDC

    print (f"{this_color}Your result is {res}%, {sum(results.Point)} out of {len(results)}{bcolors.ENDC}") 
    #update_weights(results)
    save_result('Test 3', res, len(results))

def test_selector():
    response = input("""Press the letter of the test to start it:
    a - Test 1 (type words) 
    b - Test 2 (multiple choice)
    """) or 'skip'
    match response: 
        case "a":
            test_1()
        case "b": 
            raise NotImplementedError
        case _:
            print("Nothing selected.")


if config_loaded and get_config("autostart_test_selector")=="true":
    test_selector()
    