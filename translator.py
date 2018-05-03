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

    fp = urllib.request.urlopen(url)
    mybytes = fp.read()
    content = mybytes.decode("utf8")
    fp.close()

    soup = BeautifulSoup(content, "html.parser")
    soup = soup.find("span",{"id": "result_box"})
    soup = soup.find("span")
    text = soup.get_text()
    
    if text:
        print('From: '+text)
        print('To: ' '.join(args[i:]))
        return text
    return "I Could not find anything from {0:s}".format(url)
