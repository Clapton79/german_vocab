import requests 
#import beautifulsoup4 as BeautifulSoup 

def get_definite_article(noun:str=None):
    if noun is None:
        raise ValueError("Noun is required")
        
    articles = ['der','die','das']
    for article in articles:
        response = requests.get(f"https://der-artikel.de/{article}/{noun}.html")
        if response.status_code == 200:
            return article

    return None
    
def webquery_conjugation(verb):
    url = f"https://conjugator.reverso.net/conjugation-german-verb-{verb}.html"
    sess = requests.session()
    sess.headers.update({'User-Agent': 'EventParser PowerShell/7.3.4'})
    page = sess.get(url, verify=False)
    soup = beautifulsoup(page.content, "html.parser")
    output = {'conjugations':'', 'imperative':''}
    # imperative 
    imperative = soup.find_all('div', class_='blue-box-wrap alt-tense')
    for c in imperative:
        title = c['mobile-title']
        if title == 'Imperativ Präsens':
            verb_imperative = c.find('i', class_='verbtxt')
            output['imperative'] = verb_imperative.text

    # conjugation
    conjugation = soup.find_all('div', class_='blue-box-wrap')
    
    for c in conjugation:
        title = c['mobile-title']
        if title[0:9] == 'Indikativ' and title.split(' ')[1] in ['Präsens', 'Präteritum', 'Perfekt']:
            res_tense = c.p.string
           
            for conjugation_block in c.find_all('ul', class_='wrap-verbs-listing'):
                conj_data = []
                for row in conjugation_block.children:
                    conj_data.append(' '.join(row.text.split(' ')[1:])) # remove the personal pronoun
                
                #output.append(','.join([verb,res_tense,res_tags,';'.join(conj_data)]))    
                output[res_tense] = conj_data
    return output
   
    