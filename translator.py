from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

def translate(args):
    if args:
        args = args.split()
    else:
        return "Use /translate .( en, fi, ru etc. ) sentence\ne.g. /translate .ru how are you"
    
    i = 0
    
    if args[i][0]=='.':
        language = args[i][1:]
        i += 1
    else:
        language = "en"
    
    search = '%20'.join(args[i:])
    url = 'https://translate.google.fi/?hl=fi#fi/{0:s}/{1:s}'.format(language, search)
    print(url)
    
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    web_byte = urlopen(req).read()
    webpage = web_byte.decode('utf-8')
    
    soup = BeautifulSoup(webpage, "html.parser")
    text = soup.get_text()
    return 'text'
    
    soup = soup.find("span", {'id': 'result_box'})
    print(soup)
    children = soup.findChildren()
    print(children)
    return 'test'
    soup = soup.find("span")
    print(soup)
    text = soup.get_text()
    
    if text:
        print('From: ' + text)
        print('To: ' + ' '.join(args[i:]))
        return text
    return "I Could not find anything from {0:s}".format(url)
