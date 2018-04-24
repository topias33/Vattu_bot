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
    if command == '/hei':
        bot.sendMessage(chat_id, 'Hello World from githubbbb')

def bash(command):
    args = shlex.split(command)
    args.pop(0) # .pop(0) removes '/bash'
    print args
    process = subprocess.Popen(args, stdout=subprocess.PIPE, shell=True)
    str = process.stdout.decode('utf-8')
    print str
    #return str
            

bot = telepot.Bot('555366873:AAG6ZRWJjmSFwuYFEweQDZCfiSqtECvpt9M')
bot.message_loop(handle)

print 'I am listening...'

while 1:
     time.sleep(10)
        
#https://docs.python.org/3/library/subprocess.html
#import shlex, subprocess
#command_line = input()
#/bin/vikings -input eggs.txt -output "spam spam.txt" -cmd "echo '$MONEY'"
#args = shlex.split(command_line)
#print(args)
#['/bin/vikings', '-input', 'eggs.txt', '-output', 'spam spam.txt', '-cmd', "echo '$MONEY'"]
#p = subprocess.Popen(args) # Success!
