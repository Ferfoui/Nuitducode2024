import pyxel

### CONSTANTS ###

SCREEN_SIZE = 128
GAME_NAME = "Nuit du code 2024"

RIGHT_DIRECTION = 1
LEFT_DIRECTION = -1

LEFT_BORDER = 8
RIGHT_BORDER = SCREEN_SIZE - 8

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
        self.max_speed = 7
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
        
        if self.x < LEFT_BORDER:
            self.x = LEFT_BORDER
            self.horizontal_speed = 0
        elif self.x > (RIGHT_BORDER - self.width):
            self.x = RIGHT_BORDER - self.width
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
        self.last_obstacle_1_spawn_time = 0
        self.last_obstacle_2_spawn_time = 0
        self.obstacle_width = 9
        self.coin_list=[]
        
        self.obstacle_spawn_delay_frame_count = 12
            
    def scroll_world(self, scroll_value):
        for index, obstacle in enumerate(self.obstacle_list):
            obstacle.go_down(scroll_value)
            
            if obstacle.y > SCREEN_SIZE:
                self.obstacle_list.pop(index)

        for index, coin in enumerate(self.coin_list):
            coin.go_down(scroll_value)
            
            if coin.y > SCREEN_SIZE:
                self.coin_list.pop(index)

        for border in self.border_list:# supprime les borders sorties et en cree des nouvelles en haut
            if border.y>=SCREEN_SIZE:
                border.y-=(SCREEN_SIZE+16)
            border.move_down(scroll_value)
    
    def check_obstacle_collides(self, player):
        obstacles = []
        
        for index, obstacle in enumerate(self.obstacle_list):
            if player.check_collides(obstacle):
                obstacles.append(obstacle)
                self.obstacle_list.pop(index)
        
        return obstacles
        
    def spawn_random_obstacles(self):
        obstacle_1_could_spawn = (pyxel.frame_count - self.last_obstacle_1_spawn_time) > self.obstacle_spawn_delay_frame_count
        obstacle_2_could_spawn = (pyxel.frame_count - self.last_obstacle_2_spawn_time) > self.obstacle_spawn_delay_frame_count
        
        if obstacle_1_could_spawn and (pyxel.rndf(0, 1) > 0.62):
            self.last_obstacle_1_spawn_time = pyxel.frame_count
            if pyxel.rndf(0, 1) > 0.80:
                obstacle = Coin(pyxel.rndi(LEFT_BORDER, RIGHT_BORDER - self.obstacle_width), 16)
            else:
                obstacle = Obstacle(pyxel.rndi(LEFT_BORDER, RIGHT_BORDER - self.obstacle_width), 16)
                
            self.obstacle_list.append(obstacle)
            
        if (pyxel.frame_count > 600) and obstacle_2_could_spawn and (pyxel.rndf(0, 1) > 0.8):
            self.last_obstacle_2_spawn_time = pyxel.frame_count
            obstacle = Obstacle(pyxel.rndi(LEFT_BORDER, RIGHT_BORDER - self.obstacle_width), 16)
            self.obstacle_list.append(obstacle)

    def update(self, speed, player):
        self.scroll_world(speed)
        self.spawn_random_obstacles()
        
        obstacles = self.check_obstacle_collides(player)
        
        for obstacle in obstacles:
            if obstacle.is_coin:
                player.score += round(2.71**(0.2*(pyxel.frame_count//60))) * 10
            else:
                player.health -= 10

                
    
    def draw(self):
        for obstacle in self.obstacle_list:
            obstacle.draw()
        for border in self.border_list:
            border.draw()
        for coin in self.coin_list:
            coin.draw_coin()

class Obstacle(Hitbox):
    def __init__(self, x, y):
        super().__init__(x, y, width= 9, height= 9)
        self.is_coin = False
        
    def go_down(self, pixel_number_to_move):
        self.y += pixel_number_to_move

    def draw(self):
        image = (20, 59)
        pyxel.blt(self.x, self.y, 0, image[0], image[1], self.width, self.height, colkey=5)


class Coin(Obstacle):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.is_coin = True
    
    def draw(self):
        self.image=(16,104)
        pyxel.blt(self.x, self.y, 0, self.image[0], self.image[1], self.width, self.height, colkey=5)


### GAME CLASS ###

class Game:
    def __init__(self):
        self.pyxel_init()
        self.world = World()
        self.player = Player(SCREEN_SIZE / 2, int(SCREEN_SIZE * 11/16))
        self.player.score=0
        pyxel.run(self.update, self.draw)
    
    def pyxel_init(self):
        pyxel.init(SCREEN_SIZE, SCREEN_SIZE, GAME_NAME, quit_key = pyxel.KEY_ESCAPE,fps=30)
        pyxel.load('1.pyxres')
        pyxel.play(0, 0, loop = True)
    
    def update(self):
        self.world.update(speed= 5, player= self.player)
        self.player.update()
        if pyxel.frame_count%30==0 and self.player.health>0:
            self.player.score+=round(2.71**(0.2*(pyxel.frame_count//60)))

    
    def draw(self):
        pyxel.cls(13)
        pyxel.rect(8, 0, SCREEN_SIZE-(8*2),2,5)
        pyxel.rect(8, 2, SCREEN_SIZE-(8*2),12,12)
        pyxel.rect(8, 14, SCREEN_SIZE-(8*2),2,5)
        self.world.draw()
        self.player.draw()
        pyxel.text(80, 6,"score: " + str(self.player.score),0)
        pyxel.text(20, 6,"vie: "+str(self.player.health),0)
        if not(self.player.is_alive) or self.player.health<=0:
            pyxel.text(50,60,"GAME OVER",9)
        
        

Game()