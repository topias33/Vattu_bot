from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import unicodedata

def translate(args):
    if args:
        args = args.split()
    else:
        return "Use /translate .( en, fi, ru etc. ) >( en, fi, ru etc. ) sentence\ne.g. /translate >ru how are you"
    
    i = 0
    
    if len(args[i]) == 2:
        from_language = args[i]
        i += 1
    else:
        from_language = "auto"
    
    if len(args[i]) == 2:
        to_language = args[i]
        i += 1
    else:
        to_language = "en"
        
    sentence = '+'.join(args[i:])
    
    sentence = unicodedata.normalize('NFKD', sentence).encode('ascii','ignore').decode('utf8')
    
    url = 'http://translate.google.com/m?hl={0:s}&sl={1:s}&q={2:s}'
    link = url.format(to_language, from_language, sentence)
    request = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    web_byte = urlopen(request).read()
    webpage = web_byte.decode('utf-8')
    soup = BeautifulSoup(webpage, "html.parser")
    soup = soup.find("div", {'class': 't0'})
    text = soup.get_text()
    
    if text:
        print('From: ' + ' '.join(args[i:]))
        print('To: ' + text)
        return text
    return "I Could not find anything from {0:s}".format(url)
