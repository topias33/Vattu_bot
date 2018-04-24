import sys
import time
import random
import datetime
import telepot
import subprocess
import shlex

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print 'Got command: %s' % command
    
    tag = command.split()[0]
    args = arguments(command)
    
    if tag == "/bash":
        bot.sendMessage(chat_id, bash(args))
    elif tag == "/bash":
        bot.sendMessage(chat_id, math(args))
    elif tag == "/hei":
        bot.sendMessage(chat_id, 'Hello World from githubbbb')

def bash(args):
    str = subprocess.check_output(args, stderr=subprocess.STDOUT)
    print str
    return str

def math(args):
    print "working on it"
    
def arguments(command):
    args = shlex.split(command)
    args.pop(0) # .pop(0) removes ex. '/bash'
    print args
    return args
            

bot = telepot.Bot('555366873:AAG6ZRWJjmSFwuYFEweQDZCfiSqtECvpt9M')
bot.message_loop(handle)

print 'I am listening...'

while 1:
     time.sleep(10)
        
#https://docs.python.org/3/library/subprocess.html
#https://stackoverflow.com/questions/4760215/running-shell-command-from-python-and-capturing-the-output
