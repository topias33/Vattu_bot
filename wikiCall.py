from bs4 import BeautifulSoup
import requests
def getAbbreviation():
    source = requests.get('http://sustainablesources.com/resources/country-abbreviations/').text
    soup = BeautifulSoup(source, 'html.parser')
    countryCodeSoup=soup.find('div',class_="post-bodycopy clearfix")
    codes=[]
    codesX=[]
    codesXX=[]
    for textii in countryCodeSoup.find_all('tr'):
        codes.append(textii.text)
    for i in range(len(codes)):
        list=codes[i].split('\n')
        for ii in list:
            codesX.append(ii)
    for iii in codesX:
        if iii!='' and len(iii)==2:
            if iii.isupper()==False:
                codesXX.append(iii)
    codesXX.insert(0,'en')
   
    return codesXX

def wikiSearch(searchString,languageString=None):
    #return string
    try:
        search=searchString
        if languageString!=None:
            language=languageString
        else:
            language='en'
        try:
            source = requests.get('https://'+language+'.wikipedia.org/wiki/'+search).text
            soup = BeautifulSoup(source, 'html.parser')
        except:
            source = requests.get('https://en.wikipedia.org/wiki/'+search).text
            soup = BeautifulSoup(source, 'html.parser')
        
        #mainP=soup.find('p').text
        pS=[]
        
        for a in soup.find_all('p'):
            if len(a.text)>30:
                for e in a.text:
                    if e == '.':
                        pS.append(a.text)
                        
        count=0
        counts=[]
        
        for b in pS:
            for c in b:
                if c =='.':
                    count+=1
            counts.append(count)
            count=0
        pos=0
        for d in counts:
            if d>1:
                newpS=pS[pos]
                break;
            pos+=1
        #print('counts',counts)
        #print('pos',pos)
        
        #print(newpS)        
        if counts[0]>1:
            mainP=pS[0]
        else:
            mainP=pS[0]+' '+pS[1]
        
        removeList=['()']
        #print('MAINP',mainP)
        #print(pS)
        y=re.sub(r"([/]).*?\1(.*)",'\\2',mainP,0)
        
        howManySlahes=0
        for i in mainP:
            if i=="/":
                howManySlahes+=1
        
        for ii in range(howManySlahes):
            y=re.sub(r"([/]).*?\1(.*)",'\\2',y,0)
        mainP=y
        
        for i in range(100):
            ii="["+str(i)+"]"
            removeList.append(ii)
        
        for item in removeList:
            mainP=mainP.replace(item,'')
        #remove double space
        mainP=re.sub(' +',' ',mainP)
        #print(len(mainP))
    except:
        mainP=''   
    
    if len(mainP)<15:
        mainP="Page didn't found"
    elif mainP[-3:len(mainP)]=="to:":
        mainP="Too many similarities, please give more specific argument"
        
    
    return mainP


