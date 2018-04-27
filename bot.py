import sys
import time
import random
import datetime
import telepot
import subprocess
import shlex
from nsp import Nsp
import joke
import quiz
from random import shuffle

#when running pass in the token as the first parameter e.g. python3.4 file.py token
TOKEN = sys.argv[1] 

quiz_bool = False

def handle(msg):
    print("\n")
    
    chat_id = msg['chat']['id']
    command = msg['text']
    
    global quiz_bool
    if quiz_bool and command[0] is not '/':
        if quiz.quiz_check(command):
            bot.sendMessage(chat_id, command + ' is correct')
            next = quiz.quiz_next()
            if next:
                bot.sendMessage(chat_id, next)
            else:
                quiz_bool = False
                print('quiz ends')
                bot.sendMessage(chat_id, 'Quiz has ended.')
        else:
            bot.sendMessage(chat_id, command + ' is Incorrect')
    
    if command[0] is not '/':
        return
    
    tag = command.split()[0]
    args = arguments(command)
    
    print ('Command: %s' % tag)
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
    elif tag in ['/bashjoke','/bjoke','/bj']:
        joke, answer = bash_joke(args)
        bot.sendMessage(chat_id, joke)
        if answer:
            time.sleep(10)
            bot.sendMessage(chat_id, answer)
    elif tag in ["/joke", "/j","/addjoke","/aj","/givejoke",'/gj']:
        if tag == '/joke' or tag =='/j':
            jokeX=joke.readrandomJoke()
            bot.sendMessage(chat_id,jokeX)
            jokeee(jokeX)
        elif tag == '/addjoke' or tag == '/aj':
            jokeList=joke.makeJoke(args)
            joke.addJoke(jokeList[1],jokeList[0])
            bot.sendMessage(chat_id,'Joke has been added')
        elif tag == '/givejoke' or tag == '/gj':
            jokeList=joke.readSpecificJoke(args)
            jokeee(jokeList)
    elif tag in ["/wiki", "/wikipedia"]:
        bot.sendMessage(chat_id, wiki(args))
    elif tag == '/quiz':
        quiz_bool = not quiz_bool
        if quiz_bool:
            print('quiz starts')
            quiz.quiz_start(args)
            next = quiz.quiz_next()
            if next:
                bot.sendMessage(chat_id, next)
            else:
                quiz_bool = False
                bot.sendMessage(chat_id, 'Quiz has ended.')
        else:
            print('quiz ends')
            bot.sendMessage(chat_id, 'Quiz has ended.')
    else:
        print('quiz ends')
        bot.sendMessage(chat_id, bash("cat ~/vattu/help"))

def jokeee(jokeList):
    print(jokeList)
    if not jokeList:
        return
    jokeName=jokeList[0]
    jokeJoke=jokeList[1]
    jokeAwnser=jokeList[2]
    sleeping=5
    if jokeName or jokeName=='noName' or jokeAwnser==None:
        if jokeName or jokeName=='noName':
            bot.sendMessage(chat_id,jokeJoke)
            time.sleep(sleeping)
            bot.sendMessage(chat_id,jokeAwnser)
        elif jokeAwnser==None:
            joke=jokeName+'\n'+jokeJoke
            bot.sendMessage(chat_id,joke)
        else:
            bot.sendMessage(chat_id,jokeJoke)
    else:      
        joke=jokeName+'\n'+jokeJoke
        time.sleep(sleeping)
        bot.sendMessage(chat_id,jokeAwnser)
        
def bash(args):
    output = subprocess.check_output(args, stderr=subprocess.STDOUT, shell=True)
    if output:
        output = str(output, 'utf8')
        print("Output: %s" % output.replace('\n','\n\t'))
        return output
    return "Done"    

def bash_joke(args):
    file = read_file('jokes.txt')
    files = file.split('\n')
    args_list = args.split()
    joke = ''
    if not args:
        shuffle(files)
        joke = files[0]
    else:
        for line in files:
            if line.split(' . ', 1)[0] == args_list[0]:
                joke = line
                break
        if len(args_list) == 1:
            if not joke:
                return 'There is no joke of that name.'
        else:
            if joke == args_list[0]:
                return 'Name is allready in use.'
            add_to_file('jokes.txt', args)
            return 'done'
    joke_list = joke.replace(' . ', '\n', 1).rsplit(' : ', 1)
    joke = joke_list[0]
    if len(joke_list) > 1:
        return joke, joke_list[1]
    return joke, ''

def read_file(filename, path='~/vattu/'):
    return bash('cat '+path+filename)

def add_to_file(filename, content_list=[], path='~/vattu/', gap='\n'):
    file = read_file(filename, path=path)
    if not file:
        file = gap.join(content_list)
        msg = 'New file created.'
    else:
        files = file.split(gap)
        files.append(content_list)
        file = gap.join(files)
        msg = 'File modified.'
    output = bash('echo '+file+' > '+path+filename)    
    return output, msg   
    
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

def quiz_game(chat_id):
    global quiz_bool
    next = quiz.quiz_next()
    if next:
        bot.sendMessage(chat_id, next)
    else:
        quiz_bool = False
        bot.sendMessage(chat_id, 'Quiz has ended.')
            

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)

print ('I am listening...')

while 1:
    time.sleep(10)
        
#https://docs.python.org/3/library/subprocess.html
#https://stackoverflow.com/questions/4760215/running-shell-command-from-python-and-capturing-the-output

#https://stackoverflow.com/questions/2371436/evaluating-a-mathematical-expression-in-a-string
