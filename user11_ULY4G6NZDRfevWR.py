# "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import math
import random

# initialize global variables used in your code
count_of_guesses = 7
game_range = 100
secret_number = random.randrange(0, 100)
startgame = 0
# By default game in the range 0-100 starts.
print "New Game. Range in between 0 to 100"
print "Number of remaining guesses is ", count_of_guesses
    
# define event handlers for control panel
    
def range100():
    # button that changes range to range [0,100] and restarts
    global count_of_guesses, game_range
    secret_number = random.randrange(0,100)
    count_of_guesses = 7
    game_range = 100    
    print "New Game. Range in between 0 to 100"
    print "Number of remaining guesses is ", count_of_guesses    
    
def range1000():
    # button that changes range to range [0,1000] and restarts
    global count_of_guesses, game_range    
    count_of_guesses = 10
    game_range = 1000
    secret_number = random.randrange(0,1000)
    print "New Game. Range is between 0 to 1000"
    print "Number of remaining guesses is ", count_of_guesses
                
def get_input(guess):
    # main game logic goes here	
    global count_of_guesses, secret_number, startgame
    guess = int(guess)
    print "Guess was:" ,guess    
    count_of_guesses -= 1
    if guess == secret_number:
        print "Number of remaining guesses is ", count_of_guesses
        print "Correct.."
        startgame = 1
    if guess < secret_number:
        print "Number of remaining guesses is ", count_of_guesses
        print "Lower.."
    if guess > secret_number:
        print "Number of remaining guesses is ", count_of_guesses
        print "Higher.."
    if count_of_guesses == 0:
        startgame = 1
        if guess != secret_number:
            print "You ran out of guesses. Correct number was", secret_number
    
    if(startgame == 1):
        if(game_range == 100):
            range100()
        else:
            range1000()
        startgame = 0    

# create frame
f = simplegui.create_frame("Guess the number", 200, 200)

# register event handlers for control elements

f.add_button("Range is [0,100]", range100, 200)
f.add_button("Range is [0,1000]", range1000, 200)
f.add_input("Enter the number", get_input, 200)

# start frame
f.start()
