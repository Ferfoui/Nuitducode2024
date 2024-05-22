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
        if pyxel.btn(pyxel.KEY_LEFT) and self.x>0:
            self.move(-1,2)
        if pyxel.btn(pyxel.KEY_RIGHT) and self.x<SCREEN_SIZE:
            self.move(1,2)


    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 8, 8, 8 ,colkey=12)

    def move(self, direction, speed):
        self.x +=direction*speed


### GAME CLASSE ###

class Game:
    def __init__(self):
        pyxel.init(SCREEN_SIZE, SCREEN_SIZE, GAME_NAME, quit_key = pyxel.KEY_ESCAPE)
        self.player = Player(0,0)
        pyxel.run(self.update, self.draw)
    
    def update(self):
        self.player.update()
    
    def draw(self):
        pyxel.cls(12)
        self.player.draw()
        
        

Game()