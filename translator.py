from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import unicodedata

from wikiCall import getAbbreviation

abbrev = getAbbreviation()

def translate(args):
    
    if args:
        args = args.split(' ')
    else:
        return 'All languages: ' + ', '.join(abbrev)
    
    i = 0
    
    if args[i] in abbrev:
        from_language = args[i]
        i += 1
    else:
        from_language = "auto"
    
    if args[i] in abbrev:
        to_language = args[i]
        i += 1
    else:
        to_language = "en"
        
    if i == 1:
        to_language = from_language
        from_language = "auto"
        
        
    sentences = '+'.join(args[i:]).split('\n')
    textList = []
    for sentence in sentences:
        sentence = unicodedata.normalize('NFKD', sentence).encode('ascii','ignore').decode('utf8')
    
        url = 'http://translate.google.com/m?hl={0:s}&sl={1:s}&q={2:s}'
        link = url.format(to_language, from_language, sentence)
        request = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
        web_byte = urlopen(request).read()
        webpage = web_byte.decode('utf-8')
        soup = BeautifulSoup(webpage, "html.parser")
        soup = soup.find("div", {'class': 't0'})
        textList.append(soup.get_text())
    
    text = '\n'.join(textList)
    if text:
        print('From: ' + ' '.join(args[i:]))
        print('To: ' + text)
        return text
    return "I Could not find anything from {0:s}".format(url)
