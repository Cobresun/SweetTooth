import pygame, os
from random import randint, randrange

# For Release Version Only
"""
width = input("Enter Width: ")
height = input("Enter Height: ")
RESOLUTION = (width, height)
"""

class Object(object):
    def __init__(self, width, height, x_cord, y_cord, colour):
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.rect = pygame.Rect(x_cord, y_cord, width, height)
        self.colour = colour

    def move(self, direction):
        if self.rect.y <= 2:
            self.rect.y += 1
        elif self.rect.y >= 798:
            self.rect.y += -1
        elif direction == "up":
            self.rect.y += -5
        elif direction == "down":
            self.rect.y += 5
        elif direction == "left":
            self.rect.x += -5

class Player(Object):
    def __init__(self, width, height, x_cord, y_cord, colour, health, score):
        Object.__init__(self, width, height, x_cord, y_cord, colour)
        self.health = health
        self.score = score

class Health(object):
    def __init__(self):
        self.rect_1 = pygame.Rect(30, 30, 30, 30)
        self.rect_2 = pygame.Rect(70, 30, 30, 30)
        self.rect_3 = pygame.Rect(110, 30, 30, 30)
        self.colour_1 = HEARTS_C
        self.colour_2 = HEARTS_C
        self.colour_3 = HEARTS_C

class Barrier(Object):
    def __init__(self, width, height, x_cord, y_cord, colour):
        Object.__init__(self, width, height, x_cord, y_cord, colour)
        barriers.append(self)

class Candy(Object):
    def __init__(self, width, height, x_cord, y_cord, colour):
        Object.__init__(self, width, height, x_cord, y_cord, colour)
        candies.append(self)

def spawn_barrier():
    if randint(0, 1) == 1:
        while True:
            x = RESOLUTION[0] + 1
            y = randrange(0, RESOLUTION[1] - RESOLUTION[1]/3, 30)
            for barrier in barriers:
                if barrier.rect.x == x or barrier.rect.y == y:
                    continue
            break

        Barrier(RESOLUTION[0]/15, RESOLUTION[1]/3, x, y, BARRIER_C)
    else:
        while True:
            x = RESOLUTION[0] + 1
            y = randrange(0, RESOLUTION[1] - RESOLUTION[1]/3, 30)
            for barrier in barriers:
                if barrier.rect.x == x or barrier.rect.y == y:
                    continue
            break

        Barrier(RESOLUTION[0]/3, RESOLUTION[1]/15, x, y, BARRIER_C)

def spawn_candy():
    while True:
        x = RESOLUTION[0] + 1
        y = randrange(0, RESOLUTION[1] - RESOLUTION[1]/3, 30)
        for candy in candies:
            if candy.rect.x == x or candy.rect.y == y:
                continue
        for barrier in barriers:
            if barrier.rect.x == x or barrier.rect.y == y:
                continue
        break

    Candy(RESOLUTION[0]/30, RESOLUTION[1]/30, x, y, CANDY_C)

def destroy():
    for barrier in barriers:
        if barrier.rect.x < -60:
            barriers.remove(barrier)
            del barrier
    for candy in candies:
        if candy.rect.x < -60:
            candies.remove(candy)
            del candy

def collision(obj):
    if obj.rect.x <= player.rect.x <= obj.rect.x+obj.rect.width or obj.rect.x <= player.rect.x+player.rect.width <= obj.rect.x+obj.rect.width:
        if obj.rect.y <= player.rect.y <= obj.rect.y+obj.rect.height or obj.rect.y <= player.rect.y+player.rect.height <= obj.rect.y+obj.rect.height:
            if type(obj).__name__ == 'Barrier':
                barriers.remove(obj)
            if type(obj).__name__ == 'Candy':
                candies.remove(obj)
            del obj
            return False
    return True

# Initialize Pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

# Set Up Display
pygame.display.set_caption("Diabetes")
# Resolution for testing Only
RESOLUTION = (900, 840)
SCREEN = pygame.display.set_mode(RESOLUTION)
CLOCK = pygame.time.Clock()
font = pygame.font.SysFont(None, 60)

# Initialize Colours
CANDY_C = (173,255,47)
PLAYER_C = (94,149,152)
BARRIER_C = (141,122,126)
HEARTS_C = (255,7,131)
BACKGROUND_C = (255,248,245)
SCORE_C = (254,127,30)

# Initialize Player
player = Player(RESOLUTION[0]/30, RESOLUTION[1]/30, RESOLUTION[0]/2.5, RESOLUTION[1]/2, PLAYER_C, 3, 0)
health = Health()

# Initialize Lists 
barriers = []
candies = []

# Initialize Timers
SPAWN = pygame.USEREVENT
barrier_spawn_rate = 1000
pygame.time.set_timer(SPAWN, barrier_spawn_rate)

MINUTE = pygame.USEREVENT+1
pygame.time.set_timer(MINUTE, 1000*10)


RUNNING = True

while RUNNING:

# Sets Framerate
    CLOCK.tick(60)

# Leave Game & Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            RUNNING = False
        elif event.type == SPAWN:
            spawn_barrier()
            spawn_candy()
        elif event.type == MINUTE:
            barrier_spawn_rate -= 200
            pygame.time.set_timer(SPAWN, barrier_spawn_rate)

# Garbage Collector 
    destroy()

# Collision
    for barrier in barriers:
        if not collision(barrier):
            player.health -= 1
            player.rect.x += 100
            if health.colour_1 == (255,7,131):
                health.colour_1 = (0, 0, 0)
            elif health.colour_2 == (255,7,131):
                health.colour_2 = (0, 0, 0)
            elif health.colour_3 == (255,7,131):
                health.colour_2 = (0, 0, 0)
    for candy in candies:
        if not collision(candy):
            player.score += 1

# Move Player
    key = pygame.key.get_pressed()
    if key[pygame.K_w]:
        player.move("up")
    if key[pygame.K_s]:
        player.move("down")

# Move All Barriers
    for barrier in barriers:
        barrier.move("left")

# Move All Candies
    for candy in candies:
        candy.move("left")

# End game 
    if player.health < 1:
        RUNNING = False

# Drawing The Screen
    SCREEN.fill(BACKGROUND_C)

    pygame.draw.rect(SCREEN, player.colour, player.rect)
    
    for candy in candies:
        pygame.draw.rect(SCREEN, candy.colour, candy.rect)

    for barrier in barriers:
        pygame.draw.rect(SCREEN, barrier.colour, barrier.rect)

    pygame.draw.rect(SCREEN, health.colour_1, health.rect_1)
    pygame.draw.rect(SCREEN, health.colour_2, health.rect_2)
    pygame.draw.rect(SCREEN, health.colour_3, health.rect_3)

    score = font.render("Candies: " + str(player.score), True, SCORE_C)
    SCREEN.blit(score, (RESOLUTION[0]-360 , 30))

    pygame.display.flip()

END = True

while END:

# Sets Framerate
    CLOCK.tick(60)

# Leave Game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            END = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            END = False
        elif event.type == SPAWN:
            spawn_barrier()    

# Draw Screen
    SCREEN.fill(BACKGROUND_C)
    end_text = font.render("THE END", True, SCORE_C)
    SCREEN.blit(end_text, (RESOLUTION[0]/2 - RESOLUTION[0]/5, RESOLUTION[1]/2 - RESOLUTION[1]/6))
    SCREEN.blit(score, (RESOLUTION[0]-360 , 30))

    pygame.display.flip()

# The End 