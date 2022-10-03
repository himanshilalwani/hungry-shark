add_library("minim")
import random
import os

WIDTH = 880
HEIGHT = 550

currentscreen = 1 #variable for managing different screens
gameWin = False
path = os.getcwd()
player = Minim(this)
fishes = 0 #variable for changing the number of fish to be eaten in order to win

#structure:
    #description of modes
    #game classes
    #set up and draw functions, which control logic of modes


def doFirstScreen():
    background(255)
    img = loadImage(path + '/data/intro.jpeg')
    image(img, 0, 0, width, height)  
    fill(255)
    rect(340, 470, 200, 50)
    textSize(30)
    fill(0)
    text("PLAY", 405, 505)

def doSecondScreen():
    img = loadImage(path + '/data/screen2.jpeg')
    image(img, 0, 0, width, height)
    strokeWeight(2)
    noFill()
    rect(144, 409, 110, 40)
    rect(433, 409, 110, 40) 
    
def doEndScreen():
    background(33, 89, 78)
    global gameWin
    if gameWin == True:
        back = loadImage(path + '/data/underwater1.jpeg')
        fish = loadImage(path + '/data/fishWin.png')  
        image(back, 0, 0, width, height)
        image(fish, 50, height/6)
        fill(0)
        text("YOU WIN!", 655, 140)
        fill(28, 98, 215)
        rect(640, 180, 160, 50, 10)
        fill(255)
        textSize(30)
        text("play again", 647, 213)
        
    elif gameWin == False:
        lose = loadImage(path + '/data/loseScreen.png')
        image(lose, 0, 0, width, height)
        fill(0)
        text("YOU LOSE!", 640, 140) 
        fill(7, 7, 89)
        rect(640, 180, 160, 50, 10)
        fill(255)
        textSize(30)
        text("play again", 647, 213)
                           
            
class Creature:
    def __init__(self, x, y, r, img, w, h, num_slices):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.r = r
        self.img = loadImage(path + "/data/" + img)
        self.img_w = w
        self.img_h = h
        self.num_slices = num_slices
        self.slice = 0
        self.dir = RIGHT

    def display(self):
        self.update()
        #ellipse(self.x, self.y, self.r*2, self.r*2)
        if self.dir == RIGHT:
            image(self.img, self.x - self.img_w//2 - game.x_shift, self.y - self.img_h//2, self.img_w, self.img_h, self.slice * self.img_w, 0, (self.slice + 1) * self.img_w, self.img_h)
        elif self.dir == LEFT:
            image(self.img, self.x - self.img_w//2 - game.x_shift, self.y - self.img_h//2, self.img_w, self.img_h, (self.slice + 1) * self.img_w, 0, self.slice * self.img_w, self.img_h)
    
    def update(self):
        self.x = self.x + self.vx
    
  
class Shark(Creature):
    def __init__(self, x, y, r, img, w, h, num_slices):
        Creature.__init__(self, x, y, r, img, w, h, num_slices) 
        self.key_handler = {LEFT:False, RIGHT:False, UP:False, DOWN: False}
        self.lives = 3
        self.score = 0
        self.fishsound = player.loadFile(path + "/sounds/fish.mp3")
        self.jellysound = player.loadFile(path + "/sounds/jellyfish.mp3")
        
    def update(self):
        #movement of shark in 4 directions                    
        if self.key_handler[RIGHT] == True:
            self.vx = 3
            self.dir = RIGHT
        elif self.key_handler[LEFT] == True:
            self.vx = -3
            self.dir = LEFT
        else:
            self.vx = 0
        
        if self.key_handler[UP] == True and self.y - self.r >= 0:
            self.vy = -5
            
        if self.key_handler[DOWN] == True and self.y + self.r <= height:
            self.vy = +5
            
        self.y = self.y + self.vy  
        self.x = self.x + self.vx
        
        if self.x - self.r < 0:   # cheching the edges 
            self.x = self.r
        if self.y - self.r< 0:
            self.y = self.r
        if self.y + self.r > height:
            self.y = height-self.r
                    
        if frameCount%10 == 0 and self.vx != 0 and self.vy == 0:
            self.slice = (self.slice + 1) % self.num_slices
        elif self.vx == 0:
            self.slice = 0
        
        #displaying hearts for lives
        lives_img = loadImage(path + '/data/heart.png') #displaying 3 lives on the right upper corner
        x_pos = 700
        for i in range(self.lives):
            image(lives_img, x_pos,20,40,40)
            x_pos += 50
        
        if self.x >= game.w//2:
            game.x_shift = game.x_shift + self.vx
        
        for fish in game.fishes:                         #collision detection shark/fishes
            if self.distance(fish) <= self.r + fish.r:
                game.fishes.remove(fish)
                self.fishsound.rewind()
                self.fishsound.play()                    #as soon as shark eats fish it is removed from the list and new one appended
                self.score = self.score +1
                game.fishes.append(Fishes(game.w+30+game.x_shift, random.randrange(0, game.h, 15), 30, random.randrange(1,7), "fish_sprite.png", 100, 90, 12))
              
        global fishes              #win check
        if self.score == fishes:
            global gameWin
            gameWin = True
            global currentscreen
            currentscreen = 4 
        
        fill(255)            
        textSize(20)            
        text("Score:" , 40, 40)
        text(self.score, 200, 40) 
                
        
        for jellyfish in game.jellyfish:    # collision detection shark/jellyfishes
                if self.distance(jellyfish) <= self.r + jellyfish.r: 
                    self.lives -=1
                    self.jellysound.rewind()                    
                    self.jellysound.play()
                    jellyfish.y = height
                    jellyfish.x = random.randint(60+game.x_shift, game.x_shift + width-60)
                    
                    if self.lives <= 0:     #lose check
                        gameWin = False
                        global currentscreen
                        currentscreen = 4  
                            
    def distance(self, seacreature): #distance for collision detection
        return ((self.x - seacreature.x)**2 + (self.y - seacreature.y) ** 2) ** 0.5

#fishes
class Fishes(Creature):
    def __init__(self, x, y, r, v, img, w, h, num_slices):
        Creature.__init__(self, x, y, r, img, w, h, num_slices) 
        self.x = x     
        self.y = y
        self.r = r
        self.v = v
        
    def display(self):
        fill(144, 30, 45)
        #circle(self.x, self.y, self.r)
        image(self.img, self.x - self.img_w//2 - game.x_shift, self.y - self.img_h//2, self.img_w, self.img_h, self.slice * self.img_w, 0, (self.slice + 1) * self.img_w, self.img_h)
        self.update()
        
    def update(self):
        self.x = self.x - self.v
        if self.x <= game.x_shift:                                                                                       
            self.x = game.w + game.x_shift  #move x position of fish appearing coordinate based on the shift of the frame
            #variable how much the shark moved based on arrow keys
            self.y = random.randrange(0, game.h, 15)

        if frameCount%4 == 0:
            self.slice = (self.slice + 1) % self.num_slices
                        
#JELLYFISHES                                                            
class Jellyfish(Creature):
    def __init__(self, x, y, r, v, img, w, h, num_slices):
        Creature.__init__(self,x,y,r, img, w, h, num_slices)
        self.x = x    
        self.y = y
        self.r = r
        self.v = v
       
    def display(self):
        fill(0, 30, 0)
        #circle(self.x, self.y, self.r)
        image(self.img, self.x - self.img_w//2 - game.x_shift, self.y - self.img_h//2, self.img_w, self.img_h, self.slice * self.img_w, 0, (self.slice + 1) * self.img_w, self.img_h)
        self.update()
       
    def update(self):
        self.y = self.y - self.v
        #changing x coordinate of jellyfish after it disappears from the screen  
        if self.y <= 0:
            self.x = random.randrange(60+game.x_shift, game.w -60 + game.x_shift, 80)   #check if the jelleyfish leaved the screen
            self.y =  height
            
        if frameCount%10 == 0: 
            self.slice = (self.slice + 1) % self.num_slices            
                          
#game class     
class Game:
    def __init__(self, w, h, num_jelly):
        self.w = w
        self.h = h
        self.num_jelly = num_jelly  
        self.fishes = []
        self.x_shift = 0
        self.shark = Shark(25, 50, 10, "shark_sprite.png", 196, 156, 6)
        self.jellyfish = []
        self.backgroundmusic = player.loadFile(path + "/sounds/bg_music.mp3")
    
        for fishes in range(0, 13):        
            self.fishes.append(Fishes(self.w +30, random.randrange(0, self.h, 15), 30, random.randrange(1,10), "fish_sprite.png", 100, 90, 12 ))
        
        for jellyfish in range(0,self.num_jelly): 
            self.jellyfish.append(Jellyfish(random.randrange(60, self.w-60, 80),self.h, 60, random.randrange(1,8),"jelly_sprite.png" , 120, 100, 10 )) 
            
        self.bg = loadImage(path + "/data/water.jpeg")
                
    def displayGame(self):  #parallax effect
        x_offset = 0
        x_offset = self.x_shift//2
        width_right = x_offset % self.w
        width_left = self.w - width_right

        image(self.bg, 0, 0, width_left, self.h, width_right, 0, self.w, self.h)
        image(self.bg, width_left, 0, width_right, self.h, 0, 0, width_right, self.h)
 
        for fishes in self.fishes:
            fishes.display()
        for jellyfish in self.jellyfish:
            jellyfish.display()  
            
        self.shark.display()
           

def setup():
    size(WIDTH, HEIGHT)

def draw():
    if currentscreen == 1:
        doFirstScreen()
    elif currentscreen == 2:
        doSecondScreen() 
    elif currentscreen == 3:
        game.displayGame()  
    elif currentscreen == 4:
        doEndScreen()

def keyPressed():
    if keyCode == LEFT:
        game.shark.key_handler[LEFT] = True
    elif keyCode == RIGHT:
        game.shark.key_handler[RIGHT] = True
    elif keyCode == UP:
        game.shark.key_handler[UP] = True
    elif keyCode == DOWN:
        game.shark.key_handler[DOWN] = True

def keyReleased():
    if keyCode == LEFT:
        game.shark.key_handler[LEFT] = False
    elif keyCode == RIGHT:
        game.shark.key_handler[RIGHT] = False 
    elif keyCode == UP:
        game.shark.key_handler[UP] = False 
        game.shark.vy = 0
    elif keyCode == DOWN:
        game.shark.key_handler[DOWN] = False
        game.shark.vy = 0
                
def mousePressed():                                             #controls all the buttons in the game
    global currentscreen
    if currentscreen == 1:                                      #play
        if 340<=mouseX<=540 and 470<=mouseY<=520:
            currentscreen = 2
    if currentscreen == 2:
        if 144<=mouseX<=254 and 409<=mouseY<=449:                #choosing modes
            num_jelly = 5 #changing jelly fish for different modes
            global game
            game = Game(880, 550, num_jelly)
            game.backgroundmusic.loop()
            global fishes
            fishes = 10
            currentscreen = 3
        if 433<=mouseX<=543 and 409<=mouseY<=449:              
            num_jelly = 7
            global game
            game = Game(WIDTH, HEIGHT, num_jelly)
            game.backgroundmusic.loop()
            global fishes
            fishes = 20
            currentscreen = 3
            
    if currentscreen == 4:                                        #play again
        if 640<=mouseX<=800 and 180<=mouseY<=230:
             currentscreen = 2       
               
            
