import sys
import time
import random
import datetime
import telepot
import subprocess
import shlex
from nsp import Nsp
#import rpyc

#when running pass in the token as the first parameter e.g. python file.py token
TOKEN = sys.argv[0] 

#connect to mc server using rpyc http://rpyc.readthedocs.io/en/latest/tutorial/tut1.html
#conn = rpyc.classic.connect('localhost', port=25565)
#rsys = conn.modules.sys
#minidom = conn.modules["xml.dom.minidom"]

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    
    #if quiz_bool:
    #    print("Quiz is on")
    
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
    #elif tag == "/mc":
        #print("Hello World!", file=conn.modules.sys.stdout)
    #elif tag == "/quiz":
        #quiz()
    else:
        bot.sendMessage(chat_id, bash("cat ~/vattu/help"))

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
        return "Use /wiki ( .en, .fi, .ru etc. ) Your search\ne.g. /wiki .fi one punch man"
    
    i = 0
    
    if args[i][0]=='.':
        language = args[i][1:]
        i += 1
    else:
        language = "en"
        
    search = '_'.join(args[i:])
    
    url = "https://{0:s}.wikipedia.org/w/index.php?search={1:s}".format(language, search)
    print("URL: " + url)
    return url

#def quiz():
#    q = ['1+1=2','When you mix blue and yellow you get?=Green']
#    
#    if not quiz_bool:
#        quiz_bool = True
    

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
