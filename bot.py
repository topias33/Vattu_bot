import sys
import time
import random
import datetime
import telepot
import subprocess
import shlex
from nsp import Nsp
from bs4 import BeautifulSoup
import urllib.request

#when running pass in the token as the first parameter e.g. python file.py token
TOKEN = sys.argv[1] 

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    
    if command[0] is not '/':
        return
    
    tag = command.split()[0]
    args = arguments(command)
    
    print ('\nCommand: %s' % tag)
    print ("Args: %s" % args)
    
    if tag in ["/bash","/b"]:
        bot.sendMessage(chat_id, bash(args))
    elif tag in ["/math","/m"]:
        bot.sendMessage(chat_id, math(args))
    elif tag == "/hello":
        bot.sendMessage(chat_id, 'Hello World from githubbbb')
    elif tag == "/hi":
        bot.sendMessage(chat_id, 'Miten menee?')
    elif tag == "/time":
        bot.sendMessage(chat_id, bash("date"))
    elif tag in ["/joke", "/j"]:
        bot.sendMessage(chat_id, joke(args))
    elif tag in ["/wiki", "/wikipedia"]:
        bot.sendMessage(chat_id, wiki(args))
    else:
        bot.sendMessage(chat_id, bash("cat help"))

def bash(args):
    output = subprocess.check_output(args, stderr=subprocess.STDOUT, shell=True)
    if output:
        output = str(output, 'utf8')
        print("Output: %s" % output.replace('\n','\n\t'))
        return output
    return "Done"    

def joke(args):
    if not args:
        args = "joke0" #random joke
        return bash("cat ./jokes/{0}".format(args))
    args = args.split()
    if len(args) == 1:
        command = "cat ./jokes/{0}".format(args[0])
    else:
        command = "echo {0} > ./jokes/{1}".format(' '.join(args[1:]), args[0])
    return bash(command)

def wiki(args):
    if args:
        args = args.split()
    else:
        return "Use /wiki .(en,fi,ru etc.) +(number of lines) search\ne.g. /wiki .fi +2 raspberry pi"
    
    i = 0
    
    if args[i][0]=='.':
        language = args[i]
        i += 1
    else:
        language = "en"
    
    if args[i][0]=='+':
        lines = int(args[i])
        i += 1
    else:
        lines = 1
        
    search = '_'.join(args[i:])
    
    url = "https://{0:s}.wikipedia.org/wiki/{1:s}".format(language, search)

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
    text = text[:lines]
    text = '\n'.join(text)
    
    if text:
        print(text)
        return text
    return "I Could not find anything from {0:s}".format(url)


def math(args):
    nsp = Nsp()
    args = args.replace(' ','')
    result = nsp.eval(args)
    result = "{0:s} = {1:g}".format(args,result)
    print (result)
    return result
    
def arguments(command):
    args = shlex.split(command)
    args.pop(0) # .pop(0) removes ex. '/bash'
    args = ' '.join(args)
    return args
            

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)

print ('I am listening...')

while 1:
     time.sleep(3)
        
#https://docs.python.org/3/library/subprocess.html
#https://stackoverflow.com/questions/4760215/running-shell-command-from-python-and-capturing-the-output

#https://stackoverflow.com/questions/2371436/evaluating-a-mathematical-expression-in-a-string
