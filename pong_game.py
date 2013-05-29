# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2

# helper function that spawns a ball by updating the 
# ball's position vector and velocity vector
# if right is True, the ball's velocity is upper right, else upper left
def ball_init(right):
    global ball_pos
    global ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    if right:
        ball_vel = [ random.randrange(120, 240) / 60,
                     - random.randrange(60,  180) / 60]
    else:
        ball_vel = [ - random.randrange(120, 240) / 60,
                     random.randrange(60,  180) / 60]
        
# define event handlers

def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are floats
    global score1, score2  # these are ints
    # init score
    score1 = 0
    score2 = 0
    # init paddle position
    paddle1_pos = HEIGHT / 2
    paddle2_pos = HEIGHT / 2
    # init paddle velocity
    paddle1_vel = 0.0
    paddle2_vel = 0.0
    # init ball
    ball_init(True)

    
    
def draw_paddles(canvas):
    canvas.draw_polygon([(0, paddle1_pos - HALF_PAD_HEIGHT), 
                         (PAD_WIDTH - 2, paddle1_pos - HALF_PAD_HEIGHT), 
                         (PAD_WIDTH - 2, paddle1_pos + HALF_PAD_HEIGHT),
                         (0, paddle1_pos + HALF_PAD_HEIGHT)], 
                         2, "White", "White")
    
    canvas.draw_polygon([(WIDTH - 1, paddle2_pos - HALF_PAD_HEIGHT), 
                         (WIDTH - PAD_WIDTH + 2, paddle2_pos - HALF_PAD_HEIGHT), 
                         (WIDTH - PAD_WIDTH + 2, paddle2_pos + HALF_PAD_HEIGHT),
                         (WIDTH - 1, paddle2_pos + HALF_PAD_HEIGHT)], 
                         2, "White", "White")
def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
    # update paddle's vertical position, keep paddle on the screen
    pad_collide_hndl()
     
    # draw paddles
    draw_paddles(c) 
    
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    ball_collide_hndl()
    # draw ball and scores
    c.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")
    c.draw_text(str(score1), (150, 50), 32, "Red")
    c.draw_text(str(score2), (450, 50), 32, "Blue")
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    acc = 10
    # first player pushes pad up
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel -= acc
    # first player pushes pad down
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel += acc
    # second player pushes pad up
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= acc
    # second player pushes pad down
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel += acc
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    paddle1_vel = 0
    paddle2_vel = 0

    
# check for ball collision
def ball_collide_hndl():
    global ball_vel
    global score1, score2
    
    # top collision
    if ball_pos[1] < BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    # bottom collision
    if ball_pos[1] > HEIGHT - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
        
    # left collision
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
    # ball hits a paddle
        if ((ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT) and
           (ball_pos[1] >= paddle1_pos - HALF_PAD_HEIGHT)):
                # increade ball velocity by 10%
                ball_vel[0] = -ball_vel[0] * 1.1
    # mistake
        else:
            # right player gets a point
            score2 += 1
            ball_init(True)

    # right collision
    if ball_pos[0] >= WIDTH - BALL_RADIUS - PAD_WIDTH:
    # ball hits a paddle
        if ((ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT) and
           (ball_pos[1] >= paddle2_pos - HALF_PAD_HEIGHT)):
            # increade ball velocity by 10%
                ball_vel[0] = -ball_vel[0] * 1.1
    # mistake
        else: 
            # left player gets a point
            score1 += 1
            ball_init(False)


#check for pad collision
def pad_collide_hndl():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel
    # update and check first pad's position
    paddle1_pos += paddle1_vel
    if paddle1_pos < HALF_PAD_HEIGHT: 
        paddle1_pos = HALF_PAD_HEIGHT
    elif paddle1_pos > HEIGHT - HALF_PAD_HEIGHT: 
        paddle1_pos = HEIGHT - HALF_PAD_HEIGHT
    # update and check second pad's position
    paddle2_pos += paddle2_vel
    if paddle2_pos < HALF_PAD_HEIGHT: 
        paddle2_pos = HALF_PAD_HEIGHT
    elif paddle2_pos > HEIGHT - HALF_PAD_HEIGHT: 
        paddle2_pos = HEIGHT - HALF_PAD_HEIGHT

# restart button handler
def restart():
    new_game()
    
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.add_button("Restart", restart, 200)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
frame.start()
new_game()