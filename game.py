import pyxel

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
        
        self.horizontal_speed = 0
        self.acceleration = 2
        self.max_speed = 10

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.calcul_speed(LEFT_DIRECTION)
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.calcul_speed(RIGHT_DIRECTION)
            
        self.adjust_speed()
        
        self.move()

    def draw(self):
        image = 48, 8
        pyxel.blt(self.x, self.y, 0, image[0], image[1], self.width, self.height, colkey=5)

    def calcul_speed(self, direction):
        self.horizontal_speed += direction * self.acceleration
        
        if self.horizontal_speed > self.max_speed:
            self.horizontal_speed = self.max_speed
    
    def adjust_speed(self):
        if self.horizontal_speed != 0:
            self.horizontal_speed -= self.horizontal_speed / 5

    def move(self):
        self.x += self.horizontal_speed
        
        if self.x < 0:
            self.x = 0
            self.horizontal_speed = 0
        elif self.x > SCREEN_SIZE - self.width:
            self.x = SCREEN_SIZE - self.width
            self.horizontal_speed = 0

class Border:
    def __init__(self, width):
        self.width = width

    def update(self):
        pass

    def draw(self):
        pyxel.blt()

## World
class World:
    def __init__(self):
        self.obstacle_list = []
        self.last_spawn_time = 0
        self.obstacle_width = 9
        
        self.spawn_delay_frame_count = 25
            
    def scroll_world(self, scroll_value):
        for index, obstacle in enumerate(self.obstacle_list):
            obstacle.go_down(scroll_value)
            
            if obstacle.y > SCREEN_SIZE:
                self.obstacle_list.pop(index)
    
    def spawn_random_obstacles(self):
        obstacle_could_spawn = (pyxel.frame_count - self.last_spawn_time) > self.spawn_delay_frame_count
        
        if obstacle_could_spawn and (pyxel.rndf(0, 1) > 0.60):
            self.last_spawn_time = pyxel.frame_count
            obstacle = Obstacle(pyxel.rndi(0, SCREEN_SIZE - self.obstacle_width), 0)
            self.obstacle_list.append(obstacle)

    
    def update(self, speed):
        self.scroll_world(speed)
        self.spawn_random_obstacles()
    
    def draw(self):
        for obstacle in self.obstacle_list:
            obstacle.draw()

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
        pyxel.init(SCREEN_SIZE, SCREEN_SIZE, GAME_NAME, quit_key = pyxel.KEY_ESCAPE)
        pyxel.load('1.pyxres')
    
    def update(self):
        self.world.update(5)
        self.player.update()
    
    def draw(self):
        pyxel.cls(3)
        self.world.draw()
        self.player.draw()
        
        

Game()