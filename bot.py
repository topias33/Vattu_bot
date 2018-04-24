import sys
import time
import random
import datetime
import telepot
import subprocess
import shlex

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text'].encode("utf-8")

    print 'Got command: %s' % command
    
    if command.split()[0] == "/bash":
        bash(command)
        #bot.sendMessage(chat_id, bash(command))
    if command == '/hei':
        bot.sendMessage(chat_id, 'Hello World from githubbbb')

def bash(command):
    args = shlex.split(command)
    args.pop(0) # .pop(0) removes '/bash'
    print args
    str = subprocess.check_output(args, stderr=subprocess.STDOUT)
    print str
    #return str
            

bot = telepot.Bot('555366873:AAG6ZRWJjmSFwuYFEweQDZCfiSqtECvpt9M')
bot.message_loop(handle)

print 'I am listening...'

while 1:
     time.sleep(10)
        
#https://docs.python.org/3/library/subprocess.html
#https://stackoverflow.com/questions/4760215/running-shell-command-from-python-and-capturing-the-output
