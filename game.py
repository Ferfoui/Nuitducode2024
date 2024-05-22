import pyxel, random

### CONSTANTS ###

SCREEN_SIZE = 128
GAME_NAME = "Nuit du code 2024"

RIGHT_DIRECTION = 1
LEFT_DIRECTION = -1

### IN GAME CLASSES ###

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 16
        self.height = 16
        
        self.horizontal_speed = 2

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT) and (self.x > 0):
            self.move(LEFT_DIRECTION)
        if pyxel.btn(pyxel.KEY_RIGHT) and (self.x + self.width < SCREEN_SIZE):
            self.move(RIGHT_DIRECTION)

    def draw(self):
        image = 48, 8
        pyxel.blt(self.x, self.y, 0, image[0], image[1], self.width, self.height, colkey=5)

    def move(self, direction):
        self.x += direction * self.horizontal_speed

## Border
class Border:
    def __init__(self, x, y, width, color:int):
        self.width = width
        self.y = y
        self.x = x
        self.color = color

    def move_down(self, scroll_speed):
        self.y += scroll_speed

    def draw(self):
        image=(self.color*8, 0)
        pyxel.blt(self.x, self.y, 0, image[0], image[1], 8, 8)



## World
class World:
    def __init__(self):
        self.obstacle_list = []
        self.border_list = [Border(j*(SCREEN_SIZE-8), (i-1)*8, 8, 8+i%2) for i in range((SCREEN_SIZE//8+2)) for j in range(2)]
        self.last_spawn_time = 0
        self.obstacle_width = 9
        
        self.spawn_delay_frame_count = 25
            
    def scroll_world(self, scroll_value):
        for index, obstacle in enumerate(self.obstacle_list):
            obstacle.go_down(scroll_value)
            
            if obstacle.y > SCREEN_SIZE:
                self.obstacle_list.pop(index)

        for border in self.border_list:# supprime les borders sorties et en cree des nouvelles en haut
            if border.y>=SCREEN_SIZE:
                border.y-=(SCREEN_SIZE+16)
            border.move_down(scroll_value)
            
    
    def spawn_random_obstacles(self):
        obstacle_could_spawn = (pyxel.frame_count - self.last_spawn_time) > self.spawn_delay_frame_count
        
        if obstacle_could_spawn and (random.random() > 0.60):
            self.last_spawn_time = pyxel.frame_count
            obstacle = Obstacle(random.randrange(0, SCREEN_SIZE - self.obstacle_width), 0)
            self.obstacle_list.append(obstacle)


    def update(self, speed):
        self.scroll_world(speed)
        self.spawn_random_obstacles()
    
    def draw(self):
        for obstacle in self.obstacle_list:
            obstacle.draw()
        for border in self.border_list:
            border.draw()

class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 9
        self.height = 9
        
    def go_down(self, pixel_number_to_move):
        self.y += pixel_number_to_move

    def draw(self):
        image = (20, 59)
        pyxel.blt(self.x, self.y, 0, image[0], image[1], self.width, self.height, colkey=5)


### GAME CLASSE ###

class Game:
    def __init__(self):
        self.pyxel_init()
        
        self.world = World()
        self.player = Player(0, SCREEN_SIZE / 2)
        pyxel.run(self.update, self.draw)
    
    def pyxel_init(self):
        pyxel.init(SCREEN_SIZE, SCREEN_SIZE, GAME_NAME, quit_key = pyxel.KEY_ESCAPE,fps=30)
        pyxel.load('1.pyxres')
    
    def update(self):
        self.world.update(5)
        self.player.update()

    
    def draw(self):
        pyxel.cls(3)
        self.world.draw()
        self.player.draw()
        
        

Game()