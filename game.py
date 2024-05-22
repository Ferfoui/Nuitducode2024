import pyxel

### CONSTANTS ###

SCREEN_SIZE = 128
GAME_NAME = "Nuit du code 2024"

### IN GAME CLASSES ###

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width=16
        self.height=16  

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT) and (self.x > 0):
            self.move(-1,2)
        if pyxel.btn(pyxel.KEY_RIGHT) and (self.x + self.width < SCREEN_SIZE):
            self.move(1,2)

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 48, 8, self.width, self.height, colkey=5)

    def move(self, direction, speed):
        self.x += direction * speed


## World
class World:
    def __init__(self):
        self.obstacle_list = []
            
    def scroll_world(self, scroll_value):
        for obstacle in self.obstacle_list:
            obstacle.go_down(scroll_value)
    
    def update():
        pass
    
    def draw():
        pass

class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = None
        
    def go_down(self, pixel_number_to_move):
        self.y += pixel_number_to_move

    def draw(self):
        pass


### GAME CLASSE ###

class Game:
    def __init__(self):
        self.pyxel_init()
        
        self.player = Player(0,0)
        pyxel.run(self.update, self.draw)
    
    def pyxel_init(self):
        pyxel.init(SCREEN_SIZE, SCREEN_SIZE, GAME_NAME, quit_key = pyxel.KEY_ESCAPE)
        pyxel.load('1.pyxres')
    
    def update(self):
        self.player.update()
    
    def draw(self):
        pyxel.cls(3)
        self.player.draw()
        
        

Game()