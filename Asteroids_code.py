import pygame 
from pygame import Vector2
import random
from pygame.transform import rotozoom
import os
from pygame.mixer import Sound

asteroid_images = ['/Users/gregorirodriguez/Desktop/Games/Asteroids/images/asteroid1.png','/Users/gregorirodriguez/Desktop/Games/Asteroids/images/asteroid2.png', '/Users/gregorirodriguez/Desktop/Games/Asteroids/images/asteroid3.png']


# this class is so that when the ship goes off screen it raps around to the other side 
def wrap_position(position, screen):
    x, y = position 
    w, h = screen.get_size()
    return Vector2(x % w , y % h)


def blit_rotated(position,image, forward,screen):
    angle= forward.angle_to(Vector2(0,-1))
    rotated_surface = rotozoom(image, angle,1.0)
    rotated_surface_size = Vector2(rotated_surface.get_size())
    blit_position= position - rotated_surface_size//2
    screen.blit(rotated_surface, blit_position)

# this class creates the ship
class Ship:
    def __init__(self, position):
        self.position = Vector2(position)
        self.image= pygame.image.load('/Users/gregorirodriguez/Desktop/Games/Asteroids/images/ship.png')
        self.forward = Vector2(0,-1)
        self.bullets = []
        self.can_shoot = 0
        self.drift = (0,0)
        self.shoot = Sound(os.path.join('/Users/gregorirodriguez/Desktop/Games/Asteroids/asteroidSounds/shoot.wav'))


    
    
    def update(self):
        is_key_pressed = pygame.key.get_pressed()
        if is_key_pressed[pygame.K_UP]:
            self.position += self.forward
            self.drift = (self.drift + self.forward)/1.6
        if is_key_pressed[pygame.K_LEFT]:
        #this line makes the ship rotate to the left
            self.forward = self.forward.rotate(-1)
        # this line makes the ship rotate to the right
        if is_key_pressed[pygame.K_RIGHT]:
            self.forward = self.forward.rotate(1)
        if is_key_pressed [pygame.K_SPACE] and self.can_shoot == 0 :
            # this code is for when the bullet is created "fired" and we need to pass the position of the ship and the direction the bullet is going 
            self.bullets.append(Bullet(Vector2(self.position),self.forward * 10))
            #this play the shooting sound when you press the space bar
            self.shoot.play()

            # this is the amount of second you need to wait before a new bullet can be fired 
            self.can_shoot= 400
        self.position+= self.drift
        if self.can_shoot >0 :
            self.can_shoot -= clock.get_time()
        else:
            self.can_shoot = 0

            #the code below make the ship boost foward because in python everything is a "pointer"  
            #self.bullets.append(Bullet(self.position,self.forward * 1.1))
            
    def draw(self,screen):
       # this is a instance of the wrap_position to make the ship goes of the screen it raps around to the other side 
        self.position =wrap_position(self.position, screen)
        # this block of code makes the ship rotate 
        blit_rotated(self.position, self.image, self.forward, screen)

# this class creates the Bullets
class Bullet:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity
        
    def update(self):
        self.position += self.velocity
    
    def draw(self, screen):
        pygame.draw.rect(screen,(255,0,0),[self.position.x, self.position.y, 5,5])

# this class creates the Asteroid
class Asteroid:
    def __init__(self, position, size):
        self.position = Vector2(position)
        self.velocity = Vector2(random.randint(-3,3),random.randint(-3,3))
        self.image= pygame.image.load(asteroid_images[size])
        self.radius = self.image.get_width()//2
        self.explode = Sound(os.path.join('/Users/gregorirodriguez/Desktop/Games/Asteroids/asteroidSounds/explode.mp3'))
        self.size = size
        
    #this updates the velocity of the asteriod
    def update(self):
        self.position+= self.velocity
       
        # this make sure that the asteriods always returns back to the screen if they leave in the x axis. 
        #if self.position.x < out_of_bounce[0] or self.position.x > out_of_bounce[2]:
        #    self.velocity.x *= -1
         
        # this make sure that the asteriods always returns back to the screen if they leave in the y axis. 
        #if self.position.y < out_of_bounce[1] or self.position.y < out_of_bounce[3]:
        #    self.velocity.y *= -1
    
    def draw(self,screen):
        # this is a instance of the wrap_position so that when the Asteroid goes of the screen they rap around to the other side 
        self.position =wrap_position(self.position, screen)
        blit_rotated(self.position, self.image, self.velocity, screen)
    #this is collision detection 
    def hit(self, position):
        if self.position.distance_to(position)<= self.radius:
            #this plays the sound when any object get "hit" 
            self.explode.play()
            return True
        return False

   
    

pygame.init()
screen = pygame.display.set_mode((800,800))
pygame.display.set_caption("Asteroids")

# this the background
background = pygame.image.load(os.path.join('/Users/gregorirodriguez/Desktop/Games/Asteroids/images/space.png'))


game_over = False
ship = Ship((screen.get_width()//2 ,screen.get_height()//2))
asteroids = []
#this is the max radios that the asteroids can move until they return back 
out_of_bounce = [-150,-150, 950, 950]

# this code make 10 astoriods in the screen 


for i in range(5):
        asteroids.append(Asteroid((random.randint(0,screen.get_width()),random.randint(0,screen.get_height())),0))
clock = pygame.time.Clock()

font = pygame.font.SysFont('Arial',80, True, False)
text_loser = font.render("  YOU LOST ! " , True, (255,255,255))
text_loser_position= ((screen.get_width()-text_loser.get_width())//2,(screen.get_height()-text_loser.get_height())//2)


text_win = font.render("  YOU WIN ! " , True, (255,255,255))
text_win_position= ((screen.get_width()-text_win.get_width())//2,(screen.get_height()-text_win.get_height())//2)



# this is the while loop that runs throught the game 
while not game_over:
    clock.tick(55)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
    screen.blit(background, (0,0))

    if ship is None:
        screen.blit(text_loser, text_loser_position)
        pygame.display.update()
        continue

    if len(asteroids)==0:
        screen.blit(text_win, text_win_position)
        pygame.display.update()
        continue
    # this updates the ship on the game window
    ship.update()
    ship.draw(screen)
    # this updates the asteroid on the game window
    for a in asteroids:
        a.update()
        a.draw(screen)

        if a.hit(ship.position):
            ship = None
            break
    if ship is None:
        continue
    
    deadBullets = []
    deadAsteroids = []
    # this updates the bullets that the ship is fireing on the game window
    for b in ship.bullets:
        b.update()
        b.draw(screen)
        if b.position.x < out_of_bounce[0] or b.position.x > out_of_bounce[2] or b.position.y < out_of_bounce[1] or b.position.y > out_of_bounce[3] :
            if not deadBullets.__contains__(b):
                deadBullets.append(b)

        for a in asteroids:
            if a.hit(b.position):
                if not deadBullets.__contains__(b):
                    deadBullets.append(b)
                if not deadAsteroids.__contains__(a):   
                    deadAsteroids.append(a)

    for b in deadBullets:
        
        
        ship.bullets.remove(b)

    for a in deadAsteroids:
        if a.size <2: 
            asteroids.append(Asteroid(a.position, a.size +1))
            asteroids.append(Asteroid(a.position, a.size +1))
        asteroids.remove(a)    


    pygame.display.update()
pygame.quit()
