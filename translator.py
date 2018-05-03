from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

def translate(args):
    if args:
        args = args.split()
    else:
        return "Use /translate ( en, fi, ru etc. )>( en, fi, ru etc. ) sentence\ne.g. /translate >ru how are you"
    
    i = 0
    
    if args[i][0]=='.':
        from_language = args[i][1:]
        i += 1
    else:
        from_language = "auto"
    
    if args[i][0]=='>':
        to_language = args[i][1:]
        i += 1
    else:
        to_language = "auto"
        
    sentence = '+'.join(args[i:])
    url = 'http://translate.google.com/m?hl={0:s}&sl={1:s}&q={2:s}'
    link = url.format(to_language, from_language, sentence)
    request = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    web_byte = urlopen(request).read()
    webpage = web_byte.decode('utf-8')
    soup = BeautifulSoup(webpage, "html.parser")
    soup = soup.find("div", {'class': 't0'})
    print(soup)
    text = soup.get_text()
    
    if text:
        print('From: ' + text)
        print('To: ' + ' '.join(args[i:]))
        return text
    return "I Could not find anything from {0:s}".format(url)
