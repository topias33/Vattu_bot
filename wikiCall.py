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
        
        mainP=soup.find('p').text
        removeList=[]
        
        for i in range(100):
            ii="["+str(i)+"]"
            removeList.append(ii)
        
        for item in removeList:
            mainP=mainP.replace(item,'')
        print(len(mainP))
    except:
        mainP=''   
    
    if len(mainP)<15:
        mainP="Page didn't found"
    elif mainP[-3:len(mainP)]=="to:":
        mainP="Too many similarities, please give more specific argument"
        
    
    return mainP

