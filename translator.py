from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from selenium import webdriver

'''
from bs4 import BeautifulSoup
from selenium import webdriver

url = "http://legendas.tv/busca/walking%20dead%20s03e02"
browser = webdriver.PhantomJS()
browser.get(url)
html = browser.page_source
soup = BeautifulSoup(html, 'lxml')
a = soup.find('section', 'wrapper')
'''

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
    
    browser = webdriver.PhantomJS()
    browser.get(url)
    html = browser.page_source
    
    
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    web_byte = urlopen(req).read()
    webpage = web_byte.decode('utf-8')
    
    soup = BeautifulSoup(html, "html.parser")
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
