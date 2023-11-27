import pygame 
from pygame import Vector2
import random
from pygame.transform import rotozoom
import os
# this class creates the ship
class Ship:
    def __init__(self, position):
        self.position = Vector2(position)
        self.image= pygame.image.load('/Users/gregorirodriguez/Desktop/Games/Asteroids/images/ship.png')
        self.forward = Vector2(0,-1)
        self.bullets = []

    
    
    def update(self):
        is_key_pressed = pygame.key.get_pressed()
        if is_key_pressed[pygame.K_UP]:
            self.position += self.forward
        if is_key_pressed[pygame.K_LEFT]:
        #this line makes the ship rotate to the left
            self.forward = self.forward.rotate(-1)
        # this line makes the ship rotate to the right
        if is_key_pressed[pygame.K_RIGHT]:
            self.forward = self.forward.rotate(1)
        if is_key_pressed [pygame.K_SPACE]:
            # this code is for when the bullet is created "fired" and we need to pass the position of the ship and the direction the bullet is going 
            self.bullets.append(Bullet(Vector2(self.position),self.forward * 10))
            #the code below make the ship boost foward because in python everything is a "pointer"  
            #self.bullets.append(Bullet(self.position,self.forward * 1.1))
            
    def draw(self,screen):
        # this block of code makes the ship rotate 
        angle= self.forward.angle_to(Vector2(0,-1))
        rotated_surface = rotozoom(self.image, angle,1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position= self.position - rotated_surface_size//2
        screen.blit(rotated_surface, blit_position)
# this class creates the Asteroid

class Bullet:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity
        
    def update(self):
        self.position += self.velocity
    
    def draw(self, screen):
        pygame.draw.rect(screen,(255,0,0),[self.position.x, self.position.y, 5,5])


class Asteroid:
    def __init__(self, position):
        self.position = Vector2(position)
        self.velocity = Vector2(random.randint(-3,3),random.randint(-3,3))
        self.image= pygame.image.load('/Users/gregorirodriguez/Desktop/Games/Asteroids/images/asteroid1.png')
    
    #this updates the velocity of the asteriod
    def update(self):
        self.position+= self.velocity
       
        # this make sure that the asteriods always returns back to the screen if they leave in the x axis. 
        
        if self.position.x < out_of_bounce[0] or self.position.x > out_of_bounce[2]:
            self.velocity.x *= -1
         
         # this make sure that the asteriods always returns back to the screen if they leave in the y axis. 

        if self.position.y < out_of_bounce[1] or self.position.y < out_of_bounce[3]:
            self.velocity.y *= -1
    
    def draw(self,screen):
        screen.blit(self.image,self.position)

pygame.init()
screen = pygame.display.set_mode((800,800))
pygame.display.set_caption("Asteroids")

# this the background
background = pygame.image.load(os.path.join('/Users/gregorirodriguez/Desktop/Games/Asteroids/images/space.png'))


game_over = False
ship = Ship((100,700,))
asteroids = []
#this is the max radios that the asteroids can move until they return back 
out_of_bounce = [-150,-150, 950, 950]

# this code make 10 astoriods in the screen 
for i in range(10):
        asteroids.append(Asteroid((random.randint(0,screen.get_width()),random.randint(0,screen.get_height()))))
clock = pygame.time.Clock()

# this is the while loop that runs throught the game 
while not game_over:
    clock.tick(55)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
    screen.blit(background, (0,0))
    # this updates the ship on the game window
    ship.update()
    ship.draw(screen)
    # this updates the asteroid on the game window
    for a in asteroids:
        a.update()
        a.draw(screen)
    # this updates the bullets that the ship is fireing on the game window
    for b in ship.bullets:
        b.update()
        b.draw(screen)


    pygame.display.update()
pygame.quit()