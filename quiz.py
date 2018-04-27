from random import shuffle

game_questions = []
i = 0
answer = ''

def quiz_start(amount = 1):
    questions = ['1 + 1=>2','What do you get when you mix blue and yellow?=>green'] #test
    shuffle(questions)
    global game_questions, i
    try:
        amount = int(amount)
    except:
        amount = 1
    game_questions = questions[:amount]
    i = 0

def quiz_next():
    global game_questions, i, answer
    if i < len(game_questions):
        question, answer = game_guestions[i].rsplit('=>',1)
        i += 1
        return question
    return ''

def quiz_check(guess):
    guess = guess.lower()
    return guess == answer
