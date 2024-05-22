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
        pyxel.blt(self.x, self.y, 0, 0, 8, 8, 8 ,colkey=12)

    def move(self,direction):
        pass


### GAME CLASSE ###

class Game:
    def __init__(self):
        pyxel.init(SCREEN_SIZE, SCREEN_SIZE, GAME_NAME, quit_key = pyxel.KEY_ESCAPE)
        #pyxel.image[0].load(0,0,"1.pyxres")  ne marche pas
        self.player = Player(0,0)
        pyxel.run(self.update, self.draw)
    
    def update(self):
        self.player.update()
    
    def draw(self):
        pyxel.cls(12)
        self.player.draw()
        
        

Game()