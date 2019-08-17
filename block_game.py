import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Player:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.xvel = 0
        self.yvel = 0
        self.touching_object = False
        self.is_jumping = False
        self.can_move = True
        self.max_xvel = 1
        self.max_yvel = 1
        self.jump_height = 4
    def draw(self, target):
        pygame.draw.rect(target, GREEN, [self.x, self.y, self.size, self.size], 2) 

    def step(self, obstacles):
        isFalling = True
        
        for block in obstacles:
            if block.y > self.y + self.size and self.x + self.size >= block.x and self.x  <= block.x + block.x2:        # if not touching obstacle
                isFalling = True
            elif block.y > self.y and self.x + self.size >= block.x and self.x  <= block.x + block.x2:                  # touching obstacle
                isFalling = False
                if self.y + self.size > block.y:    #bump player up if lower than the block height
                    self.y = block.y - self.size



        if isFalling:
            self.yvel = self.yvel + .1
            if self.xvel > 0:       # check right side for walls
                for block in obstacles:
                    if self.y + (self.size / 2) > block.y and block.y + block.y2 > self.y:
                        if block.x - 1.5 < self.x +self.size:
                            if block.x - 1.5 > self.x:
                                self.can_move = False
                                self.xvel = 0
            if self.xvel < 0:       # check left side for walls
                for block in obstacles:
                    if self.y + (self.size / 2) > block.y and block.y + block.y2 > self.y:
                        if block.x + block.x2 + 1.5 > self.x:
                            if block.x + block.x2 + 1.5 < self.x + self.size:
                                self.can_move = False
                                self.xvel = 0
            if self.can_move:       # if no walls   
                for block in obstacles:
                    block.x = block.x - self.xvel
            self.touching_object = False
            
        else:
            if self.is_jumping == False:            # not jumping
                self.yvel = 0
                self.touching_object = True
            else:                                   # is jumping
                self.is_jumping = False
        
        self.y = self.y + self.yvel

        if self.xvel > 0:
            if self.touching_object:
                self.xvel = self.xvel -0.025
        if self.xvel < 0:
            if self.touching_object:
                self.xvel = self.xvel +0.025
        for block in obstacles:
            block.x = block.x - self.xvel
        
            
    def jump(self, obstacles):        
        jump = True

        if self.touching_object == False:
            jump = False

        if jump:
            self.is_jumping = True
            self.yvel = - self.jump_height 


            
    def move(self, direction, obstacles):
        self.can_move = True
        pressed = pygame.key.get_pressed()
        # Right
        if direction == "right":
            for block in obstacles:
                if self.y + (self.size / 2) > block.y and block.y + block.y2 > self.y:
                    if block.x - 1.5 < self.x + self.size:
                        if block.x - 1.5 > self.x:
                            self.can_move = False
            if self.can_move:
                if self.touching_object:
                    self.xvel = self.xvel + 0.075
                    for block in obstacles:
                        block.x = block.x - self.xvel
                else:
                    self.xvel = self.xvel + 0.0125
                
            else:               
                if pressed[pygame.K_SPACE]:
                    self.is_jumping = True
                    self.yvel = - self.jump_height
                    self.xvel = 0 - self.max_xvel
                else:
                    self.xvel = 0
                    
            if self.xvel > self.max_xvel:
                self.xvel = self.max_xvel

        # Left
        if direction == "left":

            for block in obstacles:
                if self.y + (self.size / 2) > block.y and block.y + block.y2 > self.y:
                    if block.x + block.x2 + 1.5 > self.x:
                        if block.x + block.x2 + 1.5 < self.x + self.size:
                            self.can_move = False
            if self.can_move:              
                if self.touching_object:              
                    self.xvel = self.xvel - 0.075
                    for block in obstacles:
                         block.x = block.x - self.xvel
                else:
                    self.xvel = self.xvel - 0.0125
            else:
                if pressed[pygame.K_SPACE]:
                    self.is_jumping = True
                    self.yvel = - self.jump_height
                    self.xvel = self.max_xvel
                else:
                    self.xvel = 0
            if self.xvel < -self.max_xvel:
                self.xvel = 0 - self.max_xvel
                
    def goto(self, x, y):
        self.x = x
        self.y = y

        
    def reset(self):
        self.xvel = 0
        self.yvel = 0
        
        
class Block:
    def __init__(self, x, x2, y, y2):
        self.x = x
        self.y = y
        self.x2 = x2
        self.y2 = y2
        self.initial_x = x
        self.initial_y = y
        self.initial_x2 = x2
        self.initial_y2 = y2
        self.size = size
        
    def draw(self, target):
        pygame.draw.rect(target, RED, [self.x, self.y, self.x2, self.y2])
        
    def goto_origin(self):
        self.x = self.initial_x
        self.y = self.initial_y
        self.x2 = self.initial_x2
        self.y2 = self.initial_y2
        
#main


 
pygame.init()
 
size = (700, 500)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("My Game")

guy = Player(200, 200, 20)

Block_List = []

Block_List.append(Block(50, 350, 300, 350))
Block_List.append(Block(500, 50, 400, 50))
Block_List.append(Block(650, 100, 370, 200))

Block_List.append(Block(820, 50, 323, 10))
Block_List.append(Block(950, 50, 323, 10))

done = False
 

clock = pygame.time.Clock()
 

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True


    screen.fill(WHITE)




    guy.step(Block_List)
    pressed = pygame.key.get_pressed()
    
    if pressed[pygame.K_SPACE]:
        guy.jump(Block_List)

    if pressed[pygame.K_RIGHT]:
        guy.move("right", Block_List)

    if pressed[pygame.K_LEFT]:
        guy.move("left", Block_List)
        
    guy.draw(screen)
    for block in Block_List:
        block.draw(screen)
    if(guy.y > 500):
        guy.goto(200, 200)
        guy.reset()
        for block in Block_List:
            block.goto_origin()
    
    pygame.display.flip()
 

    clock.tick(120)

pygame.quit()
