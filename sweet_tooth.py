import pygame
import os 
import random
import pickle

# For Release Version Only
"""
width = input("Enter Width: ")
height = input("Enter Height: ")
RESOLUTION = (width, height)
"""




# Hi Sunny
RESOLUTION = (900, 840)

class Object(object):
    def __init__(self, width, height, x_cord, y_cord, colour):
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.rect = pygame.Rect(x_cord, y_cord, width, height)
        self.colour = colour

    def move(self, direction):
        if self.rect.y <= 2:
            self.rect.y += RESOLUTION[1]-player.rect.height-10
        elif self.rect.y >= RESOLUTION[1]-player.rect.height:
            self.rect.y -= RESOLUTION[1]-player.rect.height-10
        elif direction == "up":
            self.rect.y += -8
        elif direction == "down":
            self.rect.y += 8
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
    def __init__(self, width, height, x_cord, y_cord, colour, score):
        Object.__init__(self, width, height, x_cord, y_cord, colour)
        candies.append(self)
        self.score = score

def high_score_func():
    try:
        high_score = pickle.load( open('highscore.p', 'rb'))
        if player.score > high_score:
            high_score = player.score
            pickle.dump(high_score, open('highscore.p', 'wb'))
    except EOFError:
        high_score = player.score
        pickle.dump(high_score, open('highscore.p', 'wb'))
    if high_score > player.score:
            return high_score
    else:
        high_score = player.score
        return high_score

def spawn_barrier():
    if random.randint(0, 1) == 1:
        while True:
            x = RESOLUTION[0] + 1
            y = random.randrange(0, RESOLUTION[1] - RESOLUTION[1]/3, RESOLUTION[1]/30)
            for barrier in barriers:
                if barrier.rect.x == x or barrier.rect.y == y:
                    continue
            break

        Barrier(RESOLUTION[0]/15, RESOLUTION[1]/3, x, y, BARRIER_C)
    else:
        while True:
            x = RESOLUTION[0] + 1
            y = random.randrange(0, RESOLUTION[1] - RESOLUTION[1]/3, RESOLUTION[1]/30)
            for barrier in barriers:
                if barrier.rect.x == x or barrier.rect.y == y:
                    continue
            break

        Barrier(RESOLUTION[0]/3, RESOLUTION[1]/15, x, y, BARRIER_C)

def spawn_candy():
    while True:
        x = RESOLUTION[0] + 1
        y = random.randrange(0, RESOLUTION[1])
        for candy in candies:
            if candy.rect.x == x or candy.rect.y == y:
                continue
        for barrier in barriers:
            if barrier.rect.x == x or barrier.rect.y == y:
                continue
        break
    rarity(Candy(RESOLUTION[0]/30, RESOLUTION[1]/30, x, y, CANDY_C_1, 1))
  
def destroy():
    global candies
    for barrier in barriers:
        if barrier.rect.x < -360:
            barriers.remove(barrier)
            del barrier
    for candy in candies:
        if candy.rect.x < -360:
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

def rarity(candy):
    num = random.randint(1, 100)
    if num > 30:
        candy.score = 1
        candy.colour = CANDY_C_1
    elif 5 <= num <= 30:
        candy.score = 2
        candy.colour = CANDY_C_2
    else:
        candy.score = 5
        candy.colour = CANDY_C_3

def main():
    global RUNNING, MENU, END, INTRO, barrier_spawn_rate, high_score, barriers, candies, health

    if INTRO:
        while INTRO:
            # Sets Framerate
            CLOCK.tick(60)

            # Leave Game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    RUNNING = False
                    END = False
                    MENU = False
                    INTRO = False
                elif event.type == pygame.KEYDOWN:
                    MENU = False
                    RUNNING = True
                    END = False
                    INTRO = False
            # Draw Screen
            SCREEN.fill(BACKGROUND_C)
            end_text = font.render("Get Candy!", True, TITLE_C)
            end_text_2 = font.render("Hit Any Key To Start", True, TITLE_C)
            
            SCREEN.blit(end_text, (RESOLUTION[0]/2 - RESOLUTION[0]/4, RESOLUTION[1]/2 - RESOLUTION[1]/6))
            SCREEN.blit(end_text_2, (RESOLUTION[0]/2 - RESOLUTION[0]/4, RESOLUTION[1]/4 - RESOLUTION[1]/6))

            pygame.display.flip()
    if RUNNING:
        while RUNNING:

        # Sets Framerate
            CLOCK.tick(60)
        # Leave Game & Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    RUNNING = False
                    END = False
                    MENU = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    RUNNING = False
                    MENU = True
                    
                elif event.type == SPAWN:
                    if len(barriers) < 10:
                        spawn_barrier()
                    spawn_candy()
                elif event.type == MINUTE:
                    if not barrier_spawn_rate == 200:
                        barrier_spawn_rate -= 200
                        pygame.time.set_timer(SPAWN, barrier_spawn_rate)

        # Garbage Collector 
            destroy()
        
        # Collision
            for barrier in barriers:
                if not collision(barrier):
                    player.health -= 1
                    player.rect.x += 30
                    if health.colour_3 == (255,7,131):
                        health.colour_3 = BLACK_C
                    elif health.colour_2 == (255,7,131):
                        health.colour_2 = BLACK_C
                    elif health.colour_1 == (255,7,131):
                        health.colour_1 = BLACK_C
            for candy in candies:
                if not collision(candy):
                    player.score += candy.score
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
                END = True
                pygame.mixer.music.load('death.aif')
                pygame.mixer.music.play()

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

            score = font.render("Candies: " + str(player.score), True, TITLE_C)
            SCREEN.blit(score, (RESOLUTION[0]-360 , 30))

            pygame.display.flip()
    if END:
        while END:

        # Sets Framerate
            CLOCK.tick(60)

        # Leave Game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    RUNNING = False
                    END = False
                    MENU = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    RUNNING = False
                    END = False
                    MENU = False  
                elif event.type == pygame.KEYDOWN:
                    END = False
                    RUNNING = True
                    player.health = 3
                    barrier_spawn_rate = 1000
                    health = Health()
                    barriers = []
                    candies = [] 
                    player.rect.x -=90
                    player.score = 0
                    barrier_spawn_rate = 1000
                    pygame.time.set_timer(SPAWN, barrier_spawn_rate)

        # Draw Screen
            SCREEN.fill(BACKGROUND_C)
            end_text = font.render("High Score: " + str(high_score_func()) , True, TITLE_C)
            score = font.render("Candies: " + str(player.score), True, TITLE_C)
            instruction = font.render("Press any key to continue.", True, TITLE_C)
            SCREEN.blit(end_text, (RESOLUTION[0]/2 - RESOLUTION[0]/4, RESOLUTION[1]/2 - RESOLUTION[1]/6))
            SCREEN.blit(score, (RESOLUTION[0]-360 , 30))
            SCREEN.blit(instruction, (RESOLUTION[0]-700 , 500))
            pygame.display.flip()
    if MENU:
        while MENU:
        # Sets Framerate
            CLOCK.tick(60)

        # Leave Game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    RUNNING = False
                    END = False
                    MENU = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    MENU = False
                    RUNNING = True

        # Draw Screen
            SCREEN.fill(BACKGROUND_C)
            end_text = font.render("MENU ", True, TITLE_C)
            SCREEN.blit(end_text, (RESOLUTION[0]/2 - RESOLUTION[0]/4, RESOLUTION[1]/2 - RESOLUTION[1]/6))

            pygame.display.flip()

# Initialize Pygame
os.environ["SDL_VIDEO_CENTERED"] =  "1"
pygame.init()

# Set Up Display
pygame.display.set_caption("Sweet Tooth")
SCREEN = pygame.display.set_mode(RESOLUTION)
CLOCK = pygame.time.Clock()
font = pygame.font.SysFont("none", 60)

# Colours
CANDY_C_1 = (102,244,255)
CANDY_C_2 = (255,102,128)
CANDY_C_3 = (247,151,31)
BLACK_C = (0, 0, 0)
PLAYER_C = (94,149,152)
BARRIER_C = (141,122,126)
HEARTS_C = (255,7,131)
BACKGROUND_C = (255,248,245)
TITLE_C = (254,127,30)

# Initialize Player
player = Player(RESOLUTION[0]/30, RESOLUTION[1]/30, 
    RESOLUTION[0]/2.5, RESOLUTION[1]/2, PLAYER_C, 3, 0)
high_score = 0

# Initialize Lists 
barriers = []
candies = []

# Initialize Timers
SPAWN = pygame.USEREVENT
barrier_spawn_rate = 1000
pygame.time.set_timer(SPAWN, barrier_spawn_rate)

MINUTE = pygame.USEREVENT+1
pygame.time.set_timer(MINUTE, 1000*10)

RUNNING = False
END = False
MENU = False
INTRO = True
high_score_func()
health = Health()

while True:
    main()
    if RUNNING or END or MENU or INTRO:
        continue
    else:
        break

if __name__ == '__main__':
    main()
