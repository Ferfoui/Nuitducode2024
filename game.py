import pyxel

### CONSTANTS ###

SCREEN_SIZE = 128
GAME_NAME = "Nuit du code 2024"

RIGHT_DIRECTION = 1
LEFT_DIRECTION = -1

### IN GAME CLASSES ###

class Hitbox:
    def __init__(self, x_position, y_position, width, height):
        self.x = x_position
        self.y = y_position
        self.width = width
        self.height = height
        
    def check_collides(self, other_hitbox):
        x_collide_range = (self.x, self.x + self.width)
        y_collide_range = (self.y, self.y + self.height)
        x_overlap_right_corner = (x_collide_range[0] < other_hitbox.x) and (other_hitbox.x < x_collide_range[1])
        y_overlap_right_corner = (y_collide_range[0] < other_hitbox.y) and (other_hitbox.y < y_collide_range[1])
        
        x_left_corner = other_hitbox.x + other_hitbox.width
        y_left_corner = other_hitbox.y + other_hitbox.height
        x_overlap_left_corner = (x_collide_range[0] < x_left_corner) and (x_left_corner < x_collide_range[1])
        y_overlap_left_corner = (y_collide_range[0] < y_left_corner) and (y_left_corner < y_collide_range[1])
        
        return (x_overlap_right_corner or x_overlap_left_corner) and (y_overlap_left_corner or y_overlap_right_corner)

class Player(Hitbox):
    def __init__(self, x, y):
        super().__init__(x, y, width= 16, height= 16)
        
        self.is_alive = True
        self.health = 100
        
        self.horizontal_speed = 0
        self.acceleration = 2
        self.max_speed = 10
        self.image = 48, 8
    
    def set_dead(self):
        self.acceleration = 0
        self.image = 48, 24

    def update(self):
        self.apply_movement()
        
        if self.health <= 0:
            self.health = 0
            self.set_dead()
        
    def apply_movement(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.calcul_speed(LEFT_DIRECTION)
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.calcul_speed(RIGHT_DIRECTION)
            
        self.adjust_speed()
        
        self.move()

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.image[0], self.image[1], self.width, self.height, colkey=5)

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
    
    def check_obstacle_collides(self, player):
        for obstacle in self.obstacle_list:
            if obstacle.check_collides(player):
                return True
        
        return False
        
    def spawn_random_obstacles(self):
        obstacle_could_spawn = (pyxel.frame_count - self.last_spawn_time) > self.spawn_delay_frame_count
        
        if obstacle_could_spawn and (pyxel.rndf(0, 1) > 0.60):
            self.last_spawn_time = pyxel.frame_count
            obstacle = Obstacle(pyxel.rndi(0, SCREEN_SIZE - self.obstacle_width), 0)
            self.obstacle_list.append(obstacle)


    def update(self, speed, player):
        self.scroll_world(speed)
        self.spawn_random_obstacles()
        
        if self.check_obstacle_collides(player):
            player.health -= 10
    
    def draw(self):
        for obstacle in self.obstacle_list:
            obstacle.draw()
        for border in self.border_list:
            border.draw()

class Obstacle(Hitbox):
    def __init__(self, x, y):
        super().__init__(x, y, width= 9, height= 9)
        
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
        self.player = Player(SCREEN_SIZE / 2, SCREEN_SIZE / 2)
        pyxel.run(self.update, self.draw)
    
    def pyxel_init(self):
        pyxel.init(SCREEN_SIZE, SCREEN_SIZE, GAME_NAME, quit_key = pyxel.KEY_ESCAPE,fps=30)
        pyxel.load('1.pyxres')
    
    def update(self):
        self.world.update(speed= 5, player= self.player)
        self.player.update()

    
    def draw(self):
        pyxel.cls(3)
        self.world.draw()
        self.player.draw()
        
        

Game()