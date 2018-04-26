import sys
import time
import random
import datetime
import telepot
import subprocess
import shlex
from nsp import Nsp

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
    elif tag == "/hei":
        bot.sendMessage(chat_id, 'Hello World from githubbbb')
    elif tag == "/moi":
        bot.sendMessage(chat_id, 'Miten menee?')
    elif tag in ["/joke", "/j"]:
        bot.sendMessage(chat_id, joke(args))
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
        command = "cat ./jokes/{0}".format(args)
    else:
        command = "echo {0} > ./jokes/{1}".format(' '.join(args[1:]), args[0])
    return bash(command)

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
