import tdl
from random import randint

#Set window size and fps
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20
REALTIME = False
#Set map size
MAP_WIDTH = 80
MAP_HEIGHT = 45
#Set room size
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30

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

class Rect:
    #Initialize map variables
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
    
    def center(self):
        center_x = (self.x1 + self.x2)//2
        center_y = (self.y2 + self.y2)//2
        return (center_x, center_y)
    
    def intersect(self, other):
        #Returns True if this rectangle intersects with another one
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and 
                self.y1 <= other.y2 and self.y2 >= other.y1)
            
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
        #Turn based
        user_input = tdl.event.key_wait()
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

def make_map():
    global my_map
    
    #fill map with unblocked tiles 
    my_map = [[ Tile(True) 
        for y in range(MAP_HEIGHT)]
            for x in range(MAP_WIDTH)]
    
    rooms = []
    num_rooms = 0
    
    for r in range(MAX_ROOMS):
        #Random width and height 
        w = randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        h = randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        #Random position without going out of the boundaries of the map
        x = randint(0, MAP_WIDTH-w-1)
        y = randint(0, MAP_HEIGHT-h-1)
        
        #Rect() makes rectangles easier to work with
        new_room = Rect(x, y, w, h)
        
        #Run through the other rooms and see if they intersect with this one
        failed = False
        for other_room in rooms:
            if new_room.intersect(other_room):
                failed = True
                break
        
        if not failed:
            #This means there are no intersections, so this room is valid
            
            #"paint" it to the map's tiles
            create_room(new_room)
            #Center coordinates of new room
            (new_x, new_y) = new_room.center()
            if num_rooms == 0:
                #This is the first room, where the player starts
                player.x = new_x
                player.y = new_y
            
            else:
                #Not the first room
                #Connect to the previous room with a tunnel
                
                #Center coordinates of previous rooms
                (prev_x, prev_y) = rooms[num_rooms-1].center()
                
                #Flip a coin
                if randint(0, 1) == 1:
                    #First move vertically, then horizontally
                    create_h_tunnel(prev_x, new_x, prev_y)
                    create_v_tunnel(prev_y, new_y, new_x)
                else:
                    #First move horizontally, then vertically
                    create_v_tunnel(prev_y, new_y, prev_x)
                    create_h_tunnel(prev_x, new_x, new_y)
            
            #Append the new room to list
            rooms.append(new_room)
            num_rooms += 1

def create_room(room):
    global my_map
    
    for x in range(room.x1+1, room.x2):
        for y in range(room.y1+1, room.y2):
            my_map[x][y].blocked = False
            my_map[x][y].block_sight = False

def create_h_tunnel(x1, x2, y):
    global my_map
    #Create horizontal tunnel 
    for x in range(min(x1, x2), max(x1, x2)+1):
        my_map[x][y].blocked = False
        my_map[x][y].block_sight = False

def create_v_tunnel(y1, y2, x):
    global my_map
    #Create vertical tunnel
    for y in range(min(y1, y2), max(y1, y2)+1):
        my_map[x][y].blocked = False
        my_map[x][y].block_sight = False


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


