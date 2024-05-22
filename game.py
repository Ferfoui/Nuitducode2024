import pyxel

SCREEN_SIZE = 128
GAME_NAME = "Nuit du code 2024"

class Game:
    def __init__(self):
        pyxel.init(SCREEN_SIZE, SCREEN_SIZE, GAME_NAME, quit_key=pyxel.KEY_ESCAPE)
        pyxel.run(self.update,self.draw)
    
    def update(self):
        pass
    
    def draw(self):
        pass
        

Game()