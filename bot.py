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
    
    if command.split()[0] == "/bash":
        bash(command)
        #bot.sendMessage(chat_id, bash(command))
    if command == '/hei':
        bot.sendMessage(chat_id, 'Hello World from githubbbb')

def bash(command):
    args = shlex.split(command)
    args.pop(0) # .pop(0) removes '/bash'
    print args
    try:
        str = subprocess.check_output(string_command, stderr=subprocess.STDOUT)
        print str
    except subprocess.CalledProcessError as e:
        print e.output
        print 'Error running command: ' + '"' + e.cmd + '"' + ' see above shell error'
        print 'Return code: ' + str(e.returncode)
        #return e.cmd
    #return str
            

bot = telepot.Bot('555366873:AAG6ZRWJjmSFwuYFEweQDZCfiSqtECvpt9M')
bot.message_loop(handle)

print 'I am listening...'

while 1:
     time.sleep(10)
        
#https://docs.python.org/3/library/subprocess.html
#https://stackoverflow.com/questions/4760215/running-shell-command-from-python-and-capturing-the-output
