# implementation of card game - Memory

import simplegui
import random

col = [i % 8 for i in range(16)]
state = 0
cards = [[ i % 8 for i in range(16)], False]
move = 0
cardone = 0
cardtwo = 1

# helper function to initialize globals
def init():
    global state, move, cards
    # store the position of cards as list of lists
    cards = [[col[0], False],[col[1], False],[col[2], False],[col[3], False],
    [col[4], False],[col[5], False],[col[6], False],[col[7], False],
    [col[8], False],[col[9], False],[col[10], False],[col[11], False],
    [col[12], False],[col[13], False],[col[14], False],[col[15], False]]
    
    # shuffle the cards
    random.shuffle(cards)
    state = 0
    move = 0

     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, move, cards, cardone, cardtwo
    
    if 0 <= pos[1] <= 100 and cards[pos[0] // 50][1] == False:
        if state == 0:
            state = 1
            cardone = pos[0] // 50
            cards[(pos[0] // 50)][1] = True
        elif state == 1:
            state = 2
            cardtwo = pos[0] // 50
            cards[(pos[0] // 50)][1] = True
            move += 1
        elif state == 2:
            state = 1
            if cards[cardone][0] != cards[cardtwo][0]:
                cards[cardone][1] = False
                cards[cardtwo][1] = False
            cardone = pos[0] // 50
            cards[pos[0] // 50][1] = True
                                  
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global cards, state
    label.set_text("Moves = " + str(move))
    for col in range(len(cards)):
        if cards[col][1] == True:
            canvas.draw_text(str(cards[col][0]), (col*50 + 10, 75), 50, "Grey")
        elif cards[col][1] == False:
            canvas.draw_polygon([(col*50, 0), ((col+1)*50, 0), ((col+1)*50, 100), (col*50, 100)] ,1, "Black", "Green") 


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", init)
label = frame.add_label("Moves = 0")

# initialize global variables
init()

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
frame.start()
