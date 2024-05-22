import pyxel

### CONSTANTS ###

SCREEN_SIZE = 128
GAME_NAME = "Nuit du code 2024"

### IN GAME CLASSES ###

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y  

    def update(self):
        pass

    def draw(self):
        pass


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



### GAME CLASSE ###

class Game:
    def __init__(self):
        pyxel.init(SCREEN_SIZE, SCREEN_SIZE, GAME_NAME, quit_key=pyxel.KEY_ESCAPE)
        self.player = Player(0,0)
        pyxel.run(self.update, self.draw)
    
    def update(self):
        self.player.update()
    
    def draw(self):
        pyxel.cls(0)
        self.player.draw()
        
        

Game()