import sys
import time
import random
import datetime
import telepot
from subprocess import check_output, Popen, PIPE, STDOUT
import shlex
from nsp import Nsp
import joke
import quiz
from random import shuffle
import flagDayyy
import os

import wikiCall
import callWeather

from translator import translate

#when running pass in the token as the first parameter e.g. python3.4 file.py token
TOKEN = sys.argv[1] 

quiz_bool = {}
quiz_guesses = 1

process = None

def handle(msg):
    print("\n")
    
    global chat_id
    username = msg['from']['username']
    permissions = read_file('permissions', '~/Desktop/').split('\n')
    chat_id = msg['chat']['id']
    command = msg['text']
    
    if  str(username) in permissions:
        permission = True
    else:
        permission = False
        
    logString = log(username, command)
    
    print(logString)
    
    if command[0] is not '/':
        quiz_game(command, username)
        return
    
    tag = command.split()[0]
    args = arguments(command)
    
    if tag in ["/bash","/b"]:
        if permission:
            bot_print(bash(args))
        else:
            bot_print('You do not have permission.')
    
    elif tag == '/log':
        full_log = read_file('log' + str(chat_id))
        if args == 'f':
            bot_print(full_log)
        else:
            short_log = []
            for line in full_log.split('\n>'):
                if len(line) > 49:
                    line = line[:49] + '...'
                short_log.append(line)
            bot_print('\n'.join(short_log))
    
    elif tag in ['/translate','/tr']:
        bot_print(translate(args))
    
    elif tag == "/mc":
        global process
        if process is None:
            if args == 'start':
                os.chdir('/home/pi/test')
                exe = 'java -Xmx512M -Xms512M -jar server.jar nogui'
                process = Popen(shlex.split(exe), stdin=PIPE, stdout=PIPE, stderr=PIPE)
            else:
                bot_print('Server is not running.')
        else:
            #process.stdout.flush()
            #print(process.stdout.readline())
            process.stdin.write(bytes(cmd+'\n', 'UTF-8'))
            process.stdin.flush()
            
            
    
    elif tag in ["/math","/m"]:
        bot_print(math(args))
        
    elif tag == "/hello":
        bot_print('Hello World from githubbbb')
        
    elif tag == "/weather":
        weather=callWeather.weather()
        sunRise=callWeather.sunRisee()
        days=weather[0]
        dayTimes=weather[1]
        dayTemp=weather[2]
        daySymb=weather[4]
        
        weatherString=''
        if args=='':
            bot_print(weather[3])
            
        else:
            if args =='all':
                for i in range(len(dayTimes)):
                    weatherString+=str(days[i])+' klo '+ str(dayTimes[i]) +' =>'+str(dayTemp[i])+'C '+daySymb[i]+'\n'
                bot_print(weatherString)
            if args =='sun':
                weatherString+=str(sunRise[0])+' ja '+str(sunRise[1])
                bot_print(weatherString)
                
    elif tag == '/fd':
        if args=='':
            today=datetime.datetime.now()
            todaydate=today.strftime('%d.%m')
            flagday=flagDayyy.flagDay(todaydate)
            
            if flagday[0]==None:
                fdString=flagday[1]
            elif flagday[1]==None:
                fdString="Today there is no flag day xD"
            else:
                fdString=flagday[0]+'\n\n'+flagday[1]
            
        else:
            flagday=flagDayyy.flagDay(args)
            if flagday[0]==None:
                fdString=flagday[1]
            elif flagday[1]==None:
                fdString="Today there is no flag day xD"
            else:
                fdString=flagday[0]+'\n\n'+flagday[1] 
        if not fdString:
            fdString = 'That day isnt flag day'
        bot_print(fdString) 
       
    elif tag == "/hi":
        bot_print('Miten menee?')
    
    elif tag == '/fwiki':
        codes=wikiCall.getAbbreviation()
        argsS=args.split(' ')
        if argsS[0].lower() in codes:
            code=argsS[0].lower()
            searchS=' '.join(argsS[1:len(argsS)])
        else:
            code='en'
            searchS=args
        bot_print(wikiCall.wikiSearch(searchS, code))    
    
    elif tag == "/time":
        bot_print(bash("date"))
        
    elif tag in ['/joke','/j']:
        joke, answer = bash_joke(args)
        bot_print(joke)
        if answer:
            time.sleep(3)
            bot_print(answer)
            
    elif tag in ["/wiki", "/wikipedia"]:
        bot_print(wiki(args))
        
    elif tag == '/quiz':
        if args:
            num_rounds = int(args[0])
            if len(args)>1:
                num_players = int(args[1])
            else:
                num_players = 0
        else:
            num_rounds = 1
            num_players = 0
            
        userdict[username] = [1, 0]
        quiz_bool[chat_id] = [False, userdict, num_rounds, num_players]    
        quiz_game(tag, username)
            
        
        
        
    
    elif tag == '/help' and args:
        bot_print(help(args))
    else:
        bot_print(help('help'))

def bash(args, output_bool=True):
    try:
        output = check_output(args, stderr=STDOUT, shell=True)
    except:
        if output_bool:
            return 'No return for '+args
        return ''
    if output:
        output = str(output, 'utf8')
        if output_bool:
            print("Output: %s" % output.replace('\n','\n\t'))
        return output
    return "Done"    

def bash_joke(args):
    file = read_file('jokes.txt')
    files = file.split('\n')
    temp = args.partition(' . ')
    args = temp[0].upper()+temp[1]+temp[2]
    joke = ''
    if not args:
        shuffle(files)
        joke = files[0]
    else:
        name = args.split(' . ', 1)[0]
        for line in files:
            if line.split(' . ', 1)[0] == name:
                joke = line
                break
        if ' . ' not in args:
            if not joke:
                return 'There is no joke of that name.', ''
        else:
            if joke.split(' . ', 1)[0] == name:
                return 'Name is allready in use.', ''
            print(add_to_file('jokes.txt', [args]))
            return 'done', ''
    joke_list = joke.replace(' . ', '\n', 1).rsplit(' : ', 1)
    joke = joke_list[0]
    if len(joke_list) > 1:
        return joke, joke_list[1]
    return joke, ''

def bot_print(msg):
    global chat_id
    log('Bot', msg)
    bot.sendMessage(chat_id, msg)
    
def log(username, msg):
    time = bash("date \'+%Y-%m-%d %H:%M:%S\'", False).rstrip()
    username += ':'
    msg = msg.replace("\n"," n ")
    logString = '  '.join([time,username,msg])
    global chat_id
    add_to_file('log' + str(chat_id), [logString], gap='\n>')
    return logString

def help(name):
    file = read_file('help')
    files = file.split('\n')
    name = name.upper()
    content = []
    commands = []
    for line in files:
        line_list = line.split(' . ', 1)
        if line_list[0] == name:
            content.append(line_list[1])
        if line_list[0]:    
            commands.append(line_list[0].capitalize())
    if not content:
        return 'There is no command of that name.'
    if name == 'HELP':
        return '\n'.join(content) + '\nCommands: ' + ', '.join(set(commands)) 
    return '\n'.join(content)

def read_file(filename, path='~/vattu/'):
    return bash('cat '+path+filename, False)

def add_to_file(filename, content_list=[], path='~/vattu/', gap='\n'):
    file = read_file(filename, path=path)
    if not file:
        content = gap.join(content_list)
        msg = 'New file created.'
        output = bash('echo -n "'+content+'" > '+path+filename, False)
    else:
        content = gap.join(content_list)
        msg = 'File modified.'
        output = bash('echo -n "'+gap+content+'" >> '+path+filename, False)    
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

def quiz_game(guess, user):
    global quiz_bool, chat_id    
    qbool, userdict, num_rounds, num_players = quiz_bool.get(chat_id)
    qguesses, correct = userdict.get(user, [1,0])
    
    ready = False
    
    gen = (key for key, value in userdict.items() if value)
    if gen:
        players = [for key in gen]
    else:
        players = []
        
    if not qbool:
        if len(players) >= num_players:
            qbool = ready = True
            print('quiz starts')
            quiz.quiz_start(read_file('quiz_questions'), num_rounds)
            next = quiz.quiz_next()
            if next:
                bot_print(next)
            else:
                qbool = False
                bot_print('Quiz has ended.')
        else:
            bot_print('Player #' + str(len(players) + 1) + ' say hello!') #or anything else
    
    elif guess == '/quiz':
        qbool = False
        print('quiz forced to end')
        bot_print('Quiz has been forced to end.')
    
    else:
        if not ready:
            if quiz.quiz_check(guess):
                bot_print(guess + ' is correct')
                ready = True
            else:
                qguesses -= 1
                gen = (key for key, value in userdict.items() if value and key not user)
                if gen:
                    users = ', '.join([for key in gen])
                    bot_print(guess + ' is Incorrect.\n'+users+' may still have a try.')
                else:
                    bot_print(guess + ' is Incorrect.')
                    ready = True
                
        if ready:
            next = quiz.quiz_next()
            if next:
                for key, value in userdict.items():
                    userdict[key][0] = 1
                bot_print(next)
            else:
                qbool = False
                print('quiz ends')
                bot_print('Quiz has ended.')
                
        userdict[user] = [qguesses, correct]
        quiz_bool[chat_id] = [qbool, userdict, num_rounds, num_players]

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)

print ('I am listening...')

while 1:
    time.sleep(10)
    if process is not None:
        print(process.stdout.readline())
        
#https://docs.python.org/3/library/subprocess.html
#https://stackoverflow.com/questions/4760215/running-shell-command-from-python-and-capturing-the-output

#https://stackoverflow.com/questions/2371436/evaluating-a-mathematical-expression-in-a-string
