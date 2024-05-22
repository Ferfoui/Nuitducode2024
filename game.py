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

## Border
class Border:
    def __init__(self, x, y, width, color:int):
        self.width = width
        self.y = y
        self.x = x
        self.color = color

    def move_down(self, scroll_speed):
        self.y -= scroll_speed

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.color*8, 8, 8, 0)



## World
class World:
    def __init__(self):
        self.obstacle_list = []
        self.border_list = [Border(0,i*8,8,8+i%2) for i in range((SCREEN_SIZE//8)-1)]
            
    def scroll_world(self, scroll_value):
        for obstacle in self.obstacle_list:
            obstacle.go_down(scroll_value)

 #       for border in self.border_list:
  #          border.move_down(scroll_value)
   #         if border.y>SCREEN_SIZE:# supprime les border si elles sortent
    #            self.border_list.remove(border)
    
    def update():
        pass
    
    def draw(self):
        for border in self.border_list:
            border.draw()

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
        self.world = World()
        self.player = Player(0,0)
        pyxel.run(self.update, self.draw)
    
    def pyxel_init(self):
        pyxel.init(SCREEN_SIZE, SCREEN_SIZE, GAME_NAME, quit_key = pyxel.KEY_ESCAPE)
        pyxel.load('1.pyxres')
    
    def update(self):
        self.world.scroll_world(2)
        self.player.update()

    
    def draw(self):
        pyxel.cls(3)
        self.world.draw()
        self.player.draw()
        
        

Game()