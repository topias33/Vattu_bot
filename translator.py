#from urllib.request import Request, urlopen
import urllib
from bs4 import BeautifulSoup
'''
def translate(to_translate, to_language="auto", from_language="auto"):
    base_link = "http://translate.google.com/m?hl=%s&sl=%s&q=%s"
    if (sys.version_info[0] < 3):
        to_translate = urllib.quote_plus(to_translate)
        link = base_link % (to_language, from_language, to_translate)
        request = urllib2.Request(link, headers=agent)
        raw_data = urllib2.urlopen(request).read()
    else:
        to_translate = urllib.parse.quote(to_translate)
        link = base_link % (to_language, from_language, to_translate)
        request = urllib.request.Request(link, headers=agent)
        raw_data = urllib.request.urlopen(request).read()
    data = raw_data.decode("utf-8")
    expr = r'class="t0">(.*?)<'
    re_result = re.findall(expr, data)
    if (len(re_result) == 0):
        result = ""
    else:
        result = unescape(re_result[0])
    return (result)
'''
def translate(args):
    if args:
        args = args.split()
    else:
        return "Use /translate .( en, fi, ru etc. ) >( en, fi, ru etc. ) sentence\ne.g. /translate >ru how are you"
    
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
        
    sentence = ' '.join(args[i:])
    
    url = 'http://translate.google.com/m?hl={0:s}&sl={1:s}&q={2:s}'
    
    sentence = quote_plus(sentence)
    link = url.format(to_language, from_language, sentence)
    request = Request(link, headers=agent)
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
    '''
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    web_byte = urlopen(req).read()
    webpage = web_byte.decode('utf-8')
    '''
