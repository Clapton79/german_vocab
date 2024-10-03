
import requests
from bs4 import BeautifulSoup

url =  "https://conjugator.reverso.net/conjugation-german-verb-schaffen.html"
sess = requests.session()
sess.headers.update({'User-Agent': 'EventParser PowerShell/7.3.4'})
page = sess.get(url)
#print(page.content)
soup = BeautifulSoup(page.content,"html.parser")
#elements = soup.find(id="ch_divSimple")
#get all headers of verb tense
elements=soup.find_all('h4')
verbs = soup.find_all('i', class_='verbtxt')

for verb in verbs:
    print(verb.text)
