from random import shuffle
import string

def quiz_start(questions, amount = 1):
    questions = questions.split('\n')
    questions = list(filter(None, questions))
    shuffle(questions)
    try:
        amount = int(amount)
    except:
        amount = 1
    return [questions[:amount], 0]

def quiz_next(game_questions, i):
    if i < len(game_questions):
        question, answer = game_questions[i].rsplit(' ? ',1)
        i += 1
        return [question, answer]
    return []

def quiz_check(guess, answer):
    whitelist = string.ascii_letters + string.digits + ' '
    answer = ''.join(char for char in answer if char in whitelist).lower()
    guess = ''.join(char for char in guess if char in whitelist).lower()
    return guess == answer
