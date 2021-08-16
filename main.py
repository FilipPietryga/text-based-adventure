import msvcrt
import os

class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Entity:
    def __init__(self, coord, symbol):
        self.coord = coord
        self.symbol = symbol
    
    def getX(self):
        return self.coord.x

    def getY(self):
        return self.coord.y

    def getSymbol(self):
        return self.symbol

class LivingEntity(Entity):
    def __init__(self, coord, symbol):
        super().__init__(coord, symbol)

    def move(self, newCoords):
        self.coord.x += newCoords.x
        self.coord.y += newCoords.y

    def loop(self, coord, width, height):
        if coord.x > 0:
            self.coord.x = 0
        if coord.x < 0:
            self.coord.x = width - 1
        if coord.y > 0:
            self.coord.y = 0
        if coord.y < 0:
            self.coord.y = height - 1

class Player(LivingEntity):
    def __init__(self, coord, symbol):
        super().__init__(coord, symbol)

class Room:
    def __init__(self, dimensions):
        self.entities = []
        self.content = []
        self.dimensions = dimensions
        for y in range(self.dimensions.y):
            self.content.append([])
            for x in range(self.dimensions.x):
                self.content[y].append('.')

    def append(self, entity):
        self.entities.append(entity)
        self.content[entity.getY()][entity.getX()] = entity.symbol

    def log(self):
        for y in range(self.dimensions.y):
            for x in range(self.dimensions.x):
                print(self.content[y][x], end='')
            print()

    def checkCollision(self, coord):
        for entity in self.entities:
            if isinstance(entity, Player):
                if self.content[entity.getY() + coord.y][entity.getX() + coord.x] != '.':
                    print("napotkaned")
                    symbol = self.content[entity.getY() + coord.y][entity.getX() + coord.x]
                    if symbol != entity.symbol:
                        if coord.x > 0:
                            self.content[entity.getY() + coord.y][entity.getX() + coord.x + 1] = symbol
                        if coord.x < 0:
                            self.content[entity.getY() + coord.y][entity.getX() + coord.x - 1] = symbol
                        if coord.y > 0:
                            self.content[entity.getY() + coord.y + 1][entity.getX() + coord.x] = symbol
                        if coord.y < 0:
                            self.content[entity.getY() + coord.y - 1][entity.getX() + coord.x] = symbol
    
    def movePlayer(self, coord):
        for entity in self.entities:
            if isinstance(entity, Player):
                if(entity.coord.x + coord.x < 0 or entity.coord.x + coord.x >= self.dimensions.x or 
                    entity.coord.y + coord.y < 0 or entity.coord.y + coord.y >= self.dimensions.y):
                    self.content[entity.coord.y][entity.coord.x] = '.'
                    entity.loop(coord, self.dimensions.x, self.dimensions.y)
                    self.content[entity.coord.y][entity.coord.x] = entity.symbol
                else:
                    self.checkCollision(coord)
                    self.content[entity.coord.y + coord.y][entity.coord.x + coord.x] = entity.symbol
                    self.content[entity.coord.y][entity.coord.x] = '.'
                    entity.move(coord)

class World:
    def __init__(self):
        self.rooms = []

    def appendRoom(self, room):
        self.rooms.append(room)

playerCoord = Coord(2, 2)
player = Player(playerCoord, '$')
worldDimensions = Coord(10, 5)
room1 = Room(worldDimensions)
entity1 = Entity(Coord(7,3), 'A')
entity2 = Entity(Coord(2,3), 'S')
entity3 = Entity(Coord(4,2), 'A')
entity4 = Entity(Coord(8,2), 'P')
room1.append(player)
room1.append(entity1)
room1.append(entity2)
room1.append(entity3)
room1.append(entity4)

def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

while True:
    clear()
    room1.log()
    input_char = msvcrt.getch()
    switcher = {
        b'D': Coord(1,0),
        b'S': Coord(0,1),
        b'A': Coord(-1,0),
        b'W': Coord(0,-1)   
    }
    coord = switcher.get(input_char.upper(), Coord(0,0))
    room1.movePlayer(coord)