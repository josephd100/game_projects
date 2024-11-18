import pygame 
from pygame.locals import *
import sys 
import random 

pygame.init()

#Maximize the frame rate
clock = pygame.time.Clock()
fps = 60

screen_width, screen_height = 864, 936
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Splashy Fish')

#Define font 
font = pygame.font.SysFont('Bauhaus 93', 60)

#Define color
white = (255, 255, 255)

#Define Game Variables
ground_scroll = 0
scroll_speed = 4
flying_start = False 
game_over = False
pipe_gap = 150
pipe_frequency = 1500 #milliseconds 
last_pipe = pygame.time.get_ticks()
score = 0
pass_pipe = False 

#Load images
background = pygame.image.load('/Users/josephdaly/Desktop/Projects/python_games/flappy_bird/img.py/bg.png')
ground_img = pygame.image.load('/Users/josephdaly/Desktop/Projects/python_games/flappy_bird/img.py/ground.png')
button_img = pygame.image.load('/Users/josephdaly/Desktop/Projects/python_games/flappy_bird/img.py/restart.png')

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    score = 0
    return score 

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'/Users/josephdaly/Desktop/Projects/python_games/flappy_bird/img.py/bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False
    
    def update(self):
        #Gravity
        if flying_start == True:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel) 
        
        if game_over == False: 
        #Jumping: when the mouse detects a jump then vel - 10. When the mouse is not clicked then set back to False.
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            self.counter += 1
            flap_cooldown = 5
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('/Users/josephdaly/Desktop/Projects/python_games/flappy_bird/img.py/pipe.png')
        self.rect = self.image.get_rect()

        #position 1 is from the top, -1 is from the bottom 
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()

class Button():
    def __init__(self, x, y, image):
        self.image = image 
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    
    def draw(self):

        action = False 

        # Get mouse position  
        pos = pygame.mouse.get_pos()

        # Check if mouse is over button 
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True 
                
        # Draw button                   
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action 

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))

bird_group.add(flappy)

button = Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img)

#Reformat the image
game_background = pygame.transform.scale(background, (screen_width, screen_height))
#Create loop to run the game

while True:

    #clock rate 
    clock.tick(fps)

    #Add the background
    screen.blit(game_background, (0, 0))

    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)

    #Add the scrolling background
    screen.blit(ground_img, (ground_scroll,768))

    #Check the score 
    if len(pipe_group) > 0:
        if bird_group.sprites ()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites ()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe = True 
        if pass_pipe == True: 
            if bird_group.sprites ()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1 
                pass_pipe = False 

    draw_text(str(score), font, white, int(screen_width /  2), 20)


    #Look for collision
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True 


    #Check if flappy has hit the ground 
    if flappy.rect.bottom >= 768:
        game_over = True 
        flying_start = False 

    if game_over == False and flying_start == True:
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now 

        ground_scroll -= scroll_speed 
        if abs(ground_scroll) > 35:
            ground_scroll = 0
            
        #If the ground is no longer scrolling, stop generating pipes
        pipe_group.update()

    #Check for game over and reset 
    if game_over == True:
        if button.draw() == True:
            game_over == False 
            reset_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.quit()
        if event.type == pygame.MOUSEBUTTONDOWN and flying_start == False and game_over == False:
            flying_start = True
    
    pygame.display.update()