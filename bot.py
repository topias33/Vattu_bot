import sys
import time
import random
import datetime
import telepot
import subprocess
import shlex
from nsp import Nsp

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    
    if command[0] is not '/':
        return
    
    print ('Command: %s' % command)
    
    tag = command.split()[0]
    args = arguments(command)
    
    if tag in ["/bash","/b"]:
        bot.sendMessage(chat_id, bash(args))
    elif tag in ["/math","/m"]:
        bot.sendMessage(chat_id, math(args))
    elif tag == "/hei":
        bot.sendMessage(chat_id, 'Hello World from githubbbb')
    else:
        bot.sendMessage(chat_id, bash("cat help"))

def bash(args):
    if Type(args) is list:
        args = ' '.join(args)
    output = subprocess.check_output(args, stderr=subprocess.STDOUT, shell=True)
    print(output)
    if output:
        return output
    return "Done"    

def math(args):
    nsp = Nsp()
    result = nsp.eval(''.join(args))
    print (result)
    return result
    
def arguments(command):
    args = shlex.split(command)
    args.pop(0) # .pop(0) removes ex. '/bash'
    print ("Args: %s" % args)
    return args
            

bot = telepot.Bot('555366873:AAG6ZRWJjmSFwuYFEweQDZCfiSqtECvpt9M')
bot.message_loop(handle)

print ('I am listening...')

while 1:
     time.sleep(3)
        
#https://docs.python.org/3/library/subprocess.html
#https://stackoverflow.com/questions/4760215/running-shell-command-from-python-and-capturing-the-output

#https://stackoverflow.com/questions/2371436/evaluating-a-mathematical-expression-in-a-string
