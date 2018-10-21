import tdl

#Set window size and fps
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20
REALTIME = False
#Set map size
MAP_WIDTH = 80
MAP_HEIGHT = 45

#Set colors
color_dark_wall = (0, 0, 100)
color_dark_ground = (50, 50, 150)

class GameObject:
    #Generic object
    def __init__(self, x, y, char, color):
        self.x = x 
        self.y = y
        self.char = char
        self.color = color
        
    #Move by the given amount
    def move(self, dx, dy):
        #If tile not blocked
        if not my_map[self.x+dx][self.y+dy].blocked:
            self.x += dx
            self.y += dy
    
    #Draw the caracter char at position x,y
    def draw(self):
        con.draw_char(self.x, self.y, self.char, self.color)
    
    #Remove character from game
    def clear(self):
        con.draw_char(self.x, self.y, ' ', self.color, bg=None)

class Tile:
    
    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked
        
        #by default, if a tile is blocked, it also blocks sight
        if block_sight is None: 
            block_sight = blocked
        
        self.block_sight = block_sight
        
def make_map():
    global my_map
    #fill map with unblocked tiles 
    my_map = [[ Tile(False)
        for y in range(MAP_HEIGHT)]
            for x in range(MAP_WIDTH)]
            
    my_map[30][22].blocked = True
    my_map[30][22].block_sight = True
    my_map[50][22].blocked = True
    my_map[50][22].block_sight = True

def handle_keys(realtime):
    global playerx, playery
    
    if realtime:
        keypress = False
        for event in tdl.event.get():
            if event.type == 'KEYDOWN':
                user_input = event
                keypress = True
            if not keypress:
                return
    
    else: 
        if user_input.key == 'ENTER' and user_input.alt:
            #Alt+Enter: toggle fullscreen
            tdl.set_fullscreen(not tdl.get_fullscreen())
        
        elif user_input.key == 'ESCAPE':
            return True
        elif user_input.key == 'UP' or user_input.key == 'W':
            player.move(0, -1)    
        elif user_input.key == 'DOWN' or user_input.key == 's':
            player.move(0, 1) 
        elif user_input.key == 'LEFT' or user_input.key == 'A':
            player.move(-1, 0) 
        elif user_input.key == 'RIGHT' or user_input.key == 'D':
            player.move(1, 0) 
        
def render_all():
    for obj in objects:
        obj.draw()
        
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            wall = my_map[x][y].block_sight
            if wall:
                con.draw_char(x, y, None, fg=None, bg=color_dark_wall)
            else:
                con.draw_char(x, y, None, fg=None, bg=color_dark_ground)
    
    #Blit the contents of 'con' to the root console and present it
    root.blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0)
    

#####################################
#Initialization & Main Loop         #
#####################################
tdl.set_font('arial10x10.png', greyscale=True, altLayout=True)
root = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="RogueLike", fullscreen=False)
tdl.setFPS(LIMIT_FPS)
con = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT)

#Create Player
player = GameObject(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, '@', (255,255,255))
#Create NPC
npc = GameObject(SCREEN_WIDTH//2-5, SCREEN_HEIGHT//2, '@', (255,255,0))
#List of objects
objects = [npc, player]
            
make_map()
#Keeps the game running until window closes
while not tdl.event.is_window_closed():
    
    render_all()
    
    tdl.flush()
    
    for obj in objects:
        obj.clear()
        
    exit_game = handle_keys(REALTIME)
    if exit_game:
        break


