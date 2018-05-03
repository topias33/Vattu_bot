def wiki(args):
    if args:
        args = args.split()
    else:
        return "Use /wiki .( en, fi, ru etc. ) +( paragraphs ) Your search\ne.g. /wiki .fi +2 one punch man"
    
    i = 0
    
    if args[i][0]=='.':
        language = args[i][1:]
        i += 1
    else:
        language = "en"
    
    if args[i][0]=='+':
        paragraphs = int(args[i])
        i += 1
    else:
        paragraphs = 1
        
    search = '_'.join(args[i:])
    url = "https://{0:s}.wikipedia.org/w/index.php?search={1:s}".format(language, search)
    print(url)

    fp = urllib.request.urlopen(url)
    mybytes = fp.read()
    content = mybytes.decode("utf8")
    fp.close()

    soup = BeautifulSoup(content, "html.parser")
    text = soup.find("div",{"class": "mw-parser-output"})
    text = text.findAll("p")
    text = [x.get_text() for x in text]
    text = '\n'.join(text)
    text = text.split('\n')
    text = [x for x in text if x]
    text = text[:paragraphs]
    text = '\n\n'.join(text)
    
    if text:
        print(text)
        return '"' + url + '"\n' + text
    return "I Could not find anything from {0:s}".format(url)
