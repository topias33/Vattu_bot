from random import shuffle

game_questions = []
i = 0
answer = ''

def quiz_start(questions, amount = 1):
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
        question, answer = game_questions[i].rsplit('=>',1)
        i += 1
        return question
    return ''

def quiz_check(guess):
    guess = guess.lower()
    return guess == answer
