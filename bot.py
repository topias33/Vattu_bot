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

import operator
import math as the_real_math

#when running pass in the token as the first parameter e.g. python3.4 file.py token
TOKEN = sys.argv[1] 

quiz_bool = {}

mood = ['hungry', 'happy', 'tired', 'sad','good','amused','anxious','bored','energetic', 'excited','joyful','playful','cheerful','blissful', 'dreamy'];

abbrevations = wikiCall.getAbbreviation()

def handle(msg, mcBool = False):
    print("\n")
    
    global chat_id, quiz_bool, mc_bool
    mc_bool = mcBool
    
    if mc_bool:
        username = msg[0]
        chat_id = 0
        command = msg[1]
    else:
        username = msg['from']['username']
        chat_id = msg['chat']['id']
        command = msg['text']
    
    permissions = read_file('permissions', '~/Desktop/').split('\n')
    
    
    if  str(username) in permissions:
        permission = True
    else:
        permission = False
        
    logString = log(username, command)
    
    print(logString)
    
    if command[0] is not '/':
        if quiz_bool.get(chat_id, [0])[0]:
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
                bot_print('Starting Minecraft server...')
                os.chdir('/home/pi/test')
                exe = 'java -Xmx512M -Xms512M -jar server.jar nogui'
                process = Popen(shlex.split(exe), stdin=PIPE, stdout=PIPE, stderr=PIPE)
            else:
                bot_print('Server is not running.')
        else:
            process.stdin.write(bytes(args+'\n', 'UTF-8'))
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
            weatherString=weather[3]
            weatherStringEn=translate('en '+weatherString)
            bot_print(weatherStringEn)
            
        else:
            if args =='all':
                for i in range(len(dayTimes)):
                    weatherString+=str(days[i])+' klo '+ str(dayTimes[i]) +' =>'+str(dayTemp[i])+'C '+daySymb[i]+'\n'
                weatherStringEn=translate('en '+weatherString)
                bot_print(weatherStringEn)
            if args =='sun':
                weatherString+=str(sunRise[0])+' ja '+str(sunRise[1])
                weatherStringEn=translate('en '+weatherString)
                bot_print(weatherStringEn)
                
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
        bot_print(translate('en ' + fdString)) 
       
    elif tag == "/hi":
        bot_print('Hello! How are you? I am feeling ' + str(random.choice(mood)+ "."))
    
    elif tag in ["/lwiki", "/lwikipedia"]:
        bot_print(wiki(args))
    
    elif tag in ["/wiki", "/wikipedia"]:
        argsS=args.split(' ')
        if argsS[0].lower() in abbrevations:
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
        
    elif tag == '/quiz':
        if args:
            args = args.split()
            num_rounds = int(args[0])
            if len(args)>1:
                num_players = int(args[1])
            else:
                num_players = 1
        else:
            num_rounds = 1
            num_players = 1
            
        userdict = {}    
        userdict[username] = [1, 0]
        quiz_bool[chat_id] = [False, userdict, num_rounds, num_players, []]    
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
        return output
    return "Done"    

def bash_joke(args):
    file = read_file('jokes.txt')
    files = file.split('\n')
    files = list(filter(None, files))
    
    if not args:
        shuffle(files)
        joke = files[0]
    elif args in ['list','l']:
        jokes = []
        for line in files:
            line_list = line.split(' . ', 1)
            if line_list[0]:    
                jokes.append(line_list[0].capitalize())
        return 'Jokes: ' + ', '.join(set(jokes)), '' 
    else:
        temp = args.partition(' . ')
        args = temp[0].upper()+temp[1]+temp[2]
        joke = ''
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
            add_to_file('jokes.txt', [args])
            return 'done', ''
    joke_list = joke.replace(' . ', '\n', 1).rsplit(' : ', 1)
    joke = joke_list[0]
    if len(joke_list) > 1:
        return joke, joke_list[1]
    return joke, ''

def bot_print(msg):
    global chat_id, mc_bool
    print(log('Bot', msg))
    if mc_bool:
        process.stdin.write(bytes('say '+msg+'\n', 'UTF-8'))
        process.stdin.flush()
    else:
        bot.sendMessage(chat_id, msg)
    
def log(username, msg):
    time = bash("date \'+%Y-%m-%d %H:%M:%S\'", False).rstrip()
    username += ':'
    msg = msg.replace("\n"," n ")
    logString = ' '.join([time,username,msg])
    global chat_id
    add_to_file('log' + str(chat_id), [logString], gap='\n>')
    return '>'+logString

def help(name):
    file = read_file('help')
    files = file.split('\n')
    files = list(filter(None, files))
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
        return 'All languages: ' + ', '.join(abbrevations)
    
    i = 0
    
    if args[i] in abbrevations:
        language = args[i]
        i += 1
    else:
        language = "en"
        
    search = '_'.join(args[i:])
    
    url = "https://{0:s}.wikipedia.org/w/index.php?search={1:s}".format(language, search)
    return url    

def math(args):
    nsp = Nsp()
    args = args.replace(' ','')
    result = nsp.eval(args)
    result = "{0:s} = {1:g}".format(args,result)
    return result
    
def arguments(command):
    args = shlex.split(command)
    args.pop(0) # .pop(0) removes ex. '/bash'
    args = ' '.join(args)
    return args

def quiz_game(guess, user):
    global quiz_bool, chat_id    
    qbool, userdict, num_rounds, num_players, gameList = quiz_bool.get(chat_id)
    userdict.get(user, [1,0])
    
    ready = False
    show_scoreboard = False
    
    players = list(key for key, value in userdict.items())
        
    if not qbool:
        qbool = True
        ready = True
        bot_print('Quiz started')
        bot_print('Rounds: '+str(num_rounds))
        bot_print('Players: '+str(num_players))
        gameList = quiz.quiz_start(read_file('quiz_questions'), num_rounds)
    
    elif guess == 'stop':
        qbool = False
        bot_print('Quiz stopped.')
        show_scoreboard = True
    
    if qbool:
        if not ready and userdict[user][0]:
            if quiz.quiz_check(guess, gameList[2]):
                userdict[user][1] += 1
                bot_print(guess + ' is correct.')
                ready = True
            else:
                userdict[user][0] -= 1
                if len(players) == 1 and num_players == 1:
                    bot_print(guess + ' is incorrect.')
                    ready = True
                else:
                    players_guessed = len(list(key for key, value in userdict.items() if not value[0]))
                    players_not_guessed = len(players) - players_guessed
                    if len(players) < num_players:
                        players_not_guessed = num_players - players_guessed
                    
                    if players_not_guessed:
                        aString = guess + ' is incorrect.\nBut '+str(players_not_guessed)+' player{} may still have a try.'
                        if players_not_guessed > 1:
                            bot_print(aString.format('s'))
                        else:
                            bot_print(aString.format(''))
                        
                    else:
                        bot_print(guess + ' is incorrect.')
                        ready = True      
        if ready:
            time.sleep(1.5)
            next, gameList = quiz.quiz_next(*gameList[:2])
            if next:
                for key, value in userdict.items():
                    userdict[key][0] = 1
                bot_print('Question:\n\n'+next)
            else:
                qbool = False
                bot_print('Quiz has ended.')
                show_scoreboard = True
                
    quiz_bool[chat_id] = [qbool, userdict, num_rounds, num_players, gameList]
    
    if show_scoreboard:
        userdict = quiz_bool.get(chat_id)[1]
        sorted_userdict = sorted(userdict.items(), key=lambda i: i[1][1], reverse=True)
        i = 1
        scoreboard = 'Scoreboard:'
        ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(the_real_math.floor(n/10)%10!=1)*(n%10<4)*n%10::4])
        for u in sorted_userdict:
            scoreboard += '\n' + ordinal(i) + ' ' + u[0] + ' - ' + str(u[1][1])
            i += 1
        bot_print(scoreboard)

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)

process = None
mc_bool = False

print ('I am listening...')

while 1:
    if process is not None:
        mc_log = process.stdout.readline().decode('utf8')
        if mc_log:
            print(mc_log)
            if '[Server thread/INFO]: Done' in mc_log:
                bot_print('Minecraft server is running...')
            elif "[Server thread/INFO]: Saving chunks for level 'world'/the_end" in mc_log:
                bot_print('Minecraft server has been stopped.')
                process = None
            elif '[Server thread/INFO]: <' in mc_log and ' pi ' in mc_log:
                mc_cmd = mc_log.split('<', 1)
                mc_cmd = mc_cmd[1].split('> pi ', 1)
                mc_msg = [mc_cmd[0], mc_cmd[1]]
                handle(mc_msg, True)
                #"[Server thread/INFO]: <topias33> hei"
                
        else:
            time.sleep(3)    
    else:
        time.sleep(3)
        
#https://docs.python.org/3/library/subprocess.html
#https://stackoverflow.com/questions/4760215/running-shell-command-from-python-and-capturing-the-output

#https://stackoverflow.com/questions/2371436/evaluating-a-mathematical-expression-in-a-string
