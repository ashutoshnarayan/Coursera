# template for "Stopwatch: The Game"
import simplegui
import random

# define global variables
counter = 0
# calculates the number of times stop button is pressed when user wins
stop_pressed = 0 
# calculates the number of times stop button is pressed
no_of_times_stop_pressed = 0
# stores the value of that the time is a whole number.
whole_number = 0
# checks if stop watch is running or not when the game has begun
is_stop_watch_running = False


# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    total_int_seconds = t // 10 # total time in seconds
    d = t % 10 # tenths of seconds
    bc = total_int_seconds % 60 # seconds
    a = total_int_seconds // 60 # minutes
    if ( bc <= 9 ):
        string = str(a) +':' + '0' + str(bc) + '.' + str(d)
    else:
        string = str(a) + ':' + str(bc) + '.' + str(d)
    return string   
        
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_button():
    global is_stop_watch_running
    if is_stop_watch_running == False:
        timer.start()
        is_stop_watch_running = True
    

def stop_button():
    global is_stop_watch_running, stop_pressed, no_of_times_stop_pressed, counter
    if is_stop_watch_running == True:
        timer.stop()
        is_stop_watch_running = False
        if counter % 10 == 0:
            stop_pressed += 1
    no_of_times_stop_pressed +=1
    
def reset_button():
    global is_stop_watch_running, counter, no_of_times_stop_pressed, stop_pressed
    if is_stop_watch_running == True:
        timer.stop()
        is_stop_watch_running = False
    counter = 0
    no_of_times_stop_pressed = 0 # set the value to 0 when game is reset
    stop_pressed = 0 # set the value to 0 if game is reset
    
        
# define event handler for timer with 0.1 sec interval
def timer_handler():
    global counter
    if counter <=6000: # restricts game till 10 minutes
        counter += 1
    else:
        counter = 0
    format(counter)

# define draw handler
def draw(canvas):
    global counter, stop_pressed, no_of_times_stop_pressed
    stop_pressed_str = str(stop_pressed)
    no_of_times_stop_pressed_str = str(no_of_times_stop_pressed)
    s = format(counter)
    canvas.draw_text(s, [50,100], 35, "White")
    canvas.draw_text(stop_pressed_str + '/' + no_of_times_stop_pressed_str, [100,30], 35, "Blue")
    
    
# create frame
frame = simplegui.create_frame("Stop Watch", 200,200)

# register event handlers
frame.add_button("Start", start_button, 50)
frame.add_button("Stop", stop_button, 50)
frame.add_button("Reset", reset_button, 50)
frame.set_draw_handler(draw)
timer = simplegui.create_timer(100,timer_handler)
# start frame
frame.start()
