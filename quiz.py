from random import shuffle

def quiz_start(amount = 1):
    q = ['1 + 1=2','What do you get when you mix blue and yellow?=green'] #test
    
    shuffle(q)
    
    q = q[:amount]

def quiz_game():
    
