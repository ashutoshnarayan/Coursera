# program template for Spaceship - Rice Rocks Game
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
start_score = 0
score = start_score
time = 0
start_lives = 3
lives = start_lives
started = False

MAX_ROCKS = 12
MISSILE_AGE = 60
MIN_SHIP_TO_NEW_ROCK_DIST = 100
EXPLOSION_AGE = 79

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

animated_asteroid_info = ImageInfo([64, 64], [128, 128], 64, None, True)
animated_asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/asteroid1.opengameart.warspawn.png")
# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")
explosion_info2 = ImageInfo([50, 50], [100, 100], 50, 24, True)
explosion_image2 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/explosion.hasgraphics.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "White", "White")
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , 
                              self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)
    def update(self):
        # update angle
        self.angle += self.angle_vel
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        # update velocity
        if self.thrust:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * .1
            self.vel[1] += acc[1] * .1
        self.vel[0] *= .99
        self.vel[1] *= .99
    
    def set_thrust(self, on):
        self.thrust = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
    
    def increment_angle_vel(self):
        self.angle_vel += .05 
    
    def decrement_angle_vel(self):
        self.angle_vel -= .05
    
    def shoot(self):
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
        a_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
    
    def get_position(self):
        return self.pos
        
    def set_position(self, new_pos):
        self.pos = [new_pos[0], new_pos[1]]
        
    def set_vel(self, new_vel):
        self.vel = [new_vel[0],new_vel[1]]
        
    def get_radius(self):
        return self.radius    
    
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "Red", "Red")
        global rock_timer
        if self.animated:
            EXPLOSION_DIM = [9, 9]
            explosion_index = [self.age % EXPLOSION_DIM[0], (self.age // EXPLOSION_DIM[0]) % EXPLOSION_DIM[1]]  
            canvas.draw_image(explosion_image2, [self.image_center[0] + explosion_index[0] * self.image_size[0], 
                     self.image_center[1] + explosion_index[1] * self.image_size[1]], 
                     self.image_size, self.pos, self.image_size)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, self.image_size, self.angle)
    
    def update(self):
        # update angle
        self.angle += self.angle_vel
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT       
        self.age += 1
     
    def get_position(self):
        return self.pos
        
    def get_radius(self):
        return self.radius
    
    def get_age(self):
        return self.age
    
    def collide(self, other_object):
        ''' detect and handle collisions. '''
        # how far from both objects' centers
        distance = dist(self.get_position(), other_object.get_position())
        if distance <= self.radius + other_object.get_radius():
            # there was a collision
            return True
        return False
    
# key handlers to control ship   
def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
        
def keyup(key):
    # this is important: check what key was released, so that you adjust only the things that that key controlled.
    if key == simplegui.KEY_MAP['left']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(False)

# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, score, lives, start_score, start_lives
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
    # reset counters
    score = start_score
    lives = start_lives
  
def draw(canvas):
    global time,started, set_rocks, lives, rock_timer
    
    # animiate background
    time += 1
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime = (time / 8) % center[0]
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, [center[0] - wtime, center[1]], [size[0] - 2 * wtime, size[1]], 
                                [WIDTH / 2 + 1.25 * wtime, HEIGHT / 2], [WIDTH - 2.5 * wtime, HEIGHT])
    canvas.draw_image(debris_image, [size[0] - wtime, center[1]], [2 * wtime, size[1]], 
                                [1.25 * wtime, HEIGHT / 2], [2.5 * wtime, HEIGHT])

    
    # draw UI
    canvas.draw_text("Lives", [50, 50], 22, "White")
    canvas.draw_text("Score", [680, 50], 22, "White")
    canvas.draw_text(str(lives), [50, 80], 22, "White")
    canvas.draw_text(str(score), [680, 80], 22, "White")

    # draw ship and sprites
    my_ship.draw(canvas)
    # draw and update sprites
    process_sprite_group(set_rocks, canvas)
    # draw and update missiles
    process_sprite_group(missile_group, canvas)
    # draw and update explosions
    process_sprite_group(explosion_group, canvas)
    
    # check for collisions between the ship and rocks
    if group_collide(set_rocks, my_ship):
        # decrease the number of lives by one, no matter how many rocks we collided with
        lives -= 1
        if lives == 0:
            # stop the game
            started = False
            # remove all rocks (new ones will not be added by the timer)
            set_rocks = set([])
            # put the ship in the center
            my_ship.set_position([WIDTH / 2, HEIGHT / 2])
            my_ship.set_vel([0, 0])
        
    # collisons between missiles and rocks
    group_group_collide(set_rocks, missile_group)
    
    # update ship and sprites
    my_ship.update()

    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH/2, HEIGHT/2], 
                          splash_info.get_size())

# timer handler that spawns a rock    
def rock_spawner():
    global set_rocks, started
    # keep creating rocks until limit reached
    if len(set_rocks) < MAX_ROCKS and started:
        # don't spawn too close to the ship
        rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        # keep picking a new position until you find the right one
        while dist(rock_pos, my_ship.get_position()) < MIN_SHIP_TO_NEW_ROCK_DIST:
            rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        rock_vel = [random.random() * .7 - .3, random.random() * .7 - .3]
        rock_avel = random.random() * .2 - .1
        a_rock = Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info)
        set_rocks.add(a_rock)
                
# processing a group of sprites
def process_sprite_group(sprite_group, canvas):
    # removal before update() and draw() because aging done there.
    # handle removal of old missiles
    missile_remove = set([])
    for a_missile in missile_group:
        if a_missile.get_age() > MISSILE_AGE:
            missile_remove.add(a_missile)
    missile_group.difference_update(missile_remove)
    # handle removal of old explosions
    explosion_remove = set([])
    for explosion in explosion_group:
        # image is tiles 9x9, so indexes starting from age 0-80 is a whole life cycle?
        if explosion.get_age() > EXPLOSION_AGE:
            explosion_remove.add(explosion)
        # actual removal
        explosion_group.difference_update(explosion_remove)
    
    # update and draw each sprite
    for a_sprite in sprite_group:
        a_sprite.update()
        a_sprite.draw(canvas)
        
# check for collisions between one object and a group
def group_collide(group, other_object):
    global explosion_group
    collision_counter = 0
    tobremoved = set([])
    for a_sprite in group:
        if a_sprite.collide(other_object):
            # remove this rock from the group
            tobremoved.add(a_sprite)
            collision_counter += 1
            # create a new explosion
            # pos, vel, ang, ang_vel, image, info, sound = None
            explosion_pos = a_sprite.get_position()
            new_explosion = Sprite(explosion_pos, [0,0], 0, 0, explosion_image2, explosion_info2, explosion_sound)
            explosion_group.add(new_explosion)
    # remove that sprite from the group
    group.difference_update(tobremoved)
    return collision_counter

# check for collisions between two groups of objects
def group_group_collide(group1, group2):
    ''' group1 will happen to be rocks '''
    global score
    number_collisions = 0
    tobremoved = set([])
    # iterate through the first group and check for collision with all elements in the other group
    for a_missile in group2:
        if group_collide(group1, a_missile):
            number_collisions += 1
            tobremoved.add(a_missile)
           
    group2.difference_update(tobremoved)
    score += number_collisions
    return number_collisions
        
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
set_rocks = set([])
missile_group = set([])
explosion_group = set([])

# register handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
