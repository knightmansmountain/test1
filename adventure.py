import random

class Game(object):
    """
    holds all information for a game. Later it may be
    possible to run several game instances at once
    """
    number = 0

    def __init__(self):
        self.number = Game.number
        Game.number += 1
        self.rooms = {} # dictionary of rooms, key is room number
        self.items = {} # dictionary of items, key is item number
        self.monsters = {} # dictionary of monsters, key is m. number
        self.effects = {}


class Player(object):
    number = 0
    def __init__(self, game, where=0, name="hero"):
        """need game object, like the room class"""
        self.number = Player.number
        Player.number += 1
        self.name = name
        self.inventory = [] # list of itemnumbers (player carry items)
        self.maxcarry = 100 # kg
        self.carry = 0 # kg
        self.where = where # start room number



class Item(object):
    number = 0

    def __init__(self, game, description="", mass=0):
        self.number = Item.number
        Item.number += 1
        self.effect = None
        if mass == 0.0:
            mass = round(random.randint(1,50))
        self.mass = mass
        self.description=description
        if self.description == "":
            self.description = random.choice(("helmet","chestplate","pants",
                    "shoes","potion of instant healing","potion of strenght",
                    "potion of speed","potion of regeneration","gold","sword",
                    "bow","arrows","shield","teleport pill"))
        if self.description == "teleport pill":
            self.effect = "teleport"
        game.items[self.number] = self # add item into game dict

    def info(self):
        txt =  "Item Number {}: ".format(self.number)
        txt += self.description + "\n"
        return txt

class Monster(object):
    number = 0

    def __init__(self, game, adjective="", description="", boss=False):
        self.number = Monster.number
        Monster.number += 1
        game.monsters[self.number] = self # add monster into game dict
        self.adjective = adjective
        self.description = description
        self.hitpoints = random.randint(5,15)
        if description == "":
            if boss:
                self.adjective = random.choice((" deadly"," dangerous",
                        " creepy"," ugly"," killer"))
                self.description = random.choice(("Unicorn","Cat",
                        "Teddy Bear","Hamster","Rabbit"))
                self.hitpoints *= 5
            else:
                self.description = random.choice(("goblin","ork","troll",
                    "mice","rat","dwarf","cave drake"))


    def info(self):
        txt = "Monster number {}: {} {} with {} hitpoints\n".format(
            self.number, self.adjective, self.description, self.hitpoints)
        return txt


class Effect(object):
    def __init__(self, g, effectname, description="", roomnumber=-1, 
                 affectplayer = True, summonalies = 0, summonenemy = 0, 
                 teleport = -1, summonitem = -1, destroyitem = 0, 
                 highweight = 0, lowweight = 0, healplayer = 0, 
                 damageplayer = 0, killenemy = 0):
        self.effectname = effectname
        self.roomnumber = roomnumber
        self.description = description
        self.affectplayer = affectplayer
        self.summonalies = summonalies
        self.sommonenemy = summonenemy
        self.teleport = teleport
        self.summonitem = summonitem
        self.destroyitem = destroyitem
        self.highweight = highweight
        self.lowweight = lowweight
        self.healplayer = healplayer
        self.damageplayer = damageplayer
        self.killenemy = killenemy
        g.effects[self.effectname] = self
        
    def action(self, g, p):
        """g = Game   p = Player"""
        print("The effect does his job")
        if self.teleport != -1:
            while True:
                target = random.choice(g.rooms)
                if target == 4:
                    continue
                else:
                    break
            p.where=target

class Room(object):
    number = 0

    def __init__(self, game, description="", connections=[],
                 itemchances=[0.5,0.25,0.1],
                 monsterchances=[0.3,0.2,0.1,0.05],
                 bosschances=[0.0], explored=False):
        """need game instance"""
        self.number = Room.number
        game.rooms[self.number] = self # add room into game dict
        Room.number += 1
        self.explored = explored # True or False
        self.description = description
        self.connections = connections
        self.itemchances = itemchances
        self.monsterchances = monsterchances
        self.bosschances = bosschances
        self.effect = random.randint(1,100)
        # create items
        self.itemnumbers = []  # list of indexes of items in this room
        #self.game = game
        for chance in self.itemchances:
            if random.random()< chance:
                newItem = Item(game)
                self.itemnumbers.append(newItem.number) # add reference
        self.monsternumbers = [] # list of indexes of monsters in this room
        for chance in self.monsterchances:
            if random.random() < chance:
                newMonster = Monster(game)
                self.monsternumbers.append(newMonster.number) # add reference
        for chance in self.bosschances:
            if random.random() < chance:
                newMonster = Monster(game,boss=True)
                self.monsternumbers.append(newMonster.number) # add reference


    def info(self, game):
        """return string with all information about this room"""
        txt = "Room number {}: ".format(self.number)
        txt += self.description + "\n"
        # itmes ?
        if len(self.itemnumbers) > 0:
            txt += "You see {} itmes here: \n".format(len(self.itemnumbers))
            for i in self.itemnumbers:
                txt += game.items[i].info()
        else:
            txt += "This room has no items\n"
        # monsters ?
        if len(self.monsternumbers) > 0:
            txt +="You see {} monster(s) here:\n".format(len(self.monsternumbers))
            for m in self.monsternumbers:
                txt += game.monsters[m].info()
        else:
            txt += "No monsters in this room, fortunately.\n"
        # doors
        txt += "You see {} door(s).\n".format(len(self.connections))
        txt += "\n"
        return txt

# this function use print, replace later with gui commands
def output(txt):
    """can be later replaced by gui or graphical output"""
    print(txt)

def select_number(list_of_numbers):
        """The player select *one* number of a list of numbers"""
        answer = ""
        while ((not answer.isdecimal()) or int(answer) not in list_of_numbers):
                answer=input("Please type selected number and press ENTER: ")
        return int(answer)

def show_inventory(game, player):
    output("\n\n")
    output("==== Your inventory ====")
    output("")
    output("number, description, mass (kg)")
    output("-------------------------")
    output("")
    tmpmass = 0.0
    for i in player.inventory:
        output("{}...{}...{}".format(i, game.items[i].description,
                                             game.items[i].mass))
        tmpmass += game.items[i].mass
    output("")
    output("You're currently carrying {} kg, that is {:.2f}% of your capacity".format(
        tmpmass, (tmpmass / player.maxcarry)*100))


def drop_item(game, player):
    for i in player.inventory:
        output("")
        print(i,"...........",game.items[i].description)
        output("")
    output("Please type selected number and press ENTER")
    try:
        selection=int(input(">>> "))
    except:
        output("")
        output("Wrong input")
        return
    if len(player.inventory) > 0:
        # drop chosen item in inventory
        player.inventory.remove(selection)
        game.rooms[player.where].itemnumbers.append(selection)

def pickup_item(game, player):
    for i in game.rooms[player.where].itemnumbers:
        output("")
        print(i,"...........",game.items[i].description)
        output("")
    output("Please type selected number and press ENTER")

    try:
        selection=int(input(">>> "))
    except:
        output("")
        output("Wrong input")
        return
    # can player carry this item
    tmpmass=0
    for j in player.inventory:
        tmpmass += game.items[j].mass
    if tmpmass + game.items[selection].mass < player.maxcarry:
        if len(game.rooms[player.where].itemnumbers) > 0:
            # pick up chosen item in this room
            player.inventory.append(selection)
            game.rooms[player.where].itemnumbers.remove(selection)
    else:
         output("")
         output("You're carrying too much!")
         output("You have to drop something to carry more stuff!")
         
def use_item(game, player):
    for i in player.inventory:
        output("")
        print(i,"...........",game.items[i].description)
        output("")
    output("Please type selected number and press ENTER")
    try:
        selection=int(input(">>> "))
    except:
        output("")
        output("Wrong input")
        return
    if len(player.inventory) > 0:
        # use chosen item in inventory
        player.inventory.remove(selection)
        #game.rooms[player.where].itemnumbers.append(selection)

# this funciton use input, replace later with gui command
def nextAction(game, player):
    """ask the user to select only one of many options"""
    output("What do you want to do today ?")
    connections = game.rooms[player.where].connections
    names = [] # temp list of room names
    for c in connections:
        if game.rooms[c].explored:
            names.append(game.rooms[c].description)
        else:
            names.append("unknown room")
    output("0.........other actions")
    for d in enumerate(names, 1): # make list of tuples, start with 1
        output("{}.........{}".format(d[0], d[1]))
    #answer = ""
    #while ((not answer.isdecimal()) or (int(answer) < 0) or
    #       (int(answer) > len(connections))):
    #    answer = input("please type number and press ENTER:>")
    answer = select_number(range(len(names)+1))
    if answer != 0:
       return connections[int(answer)-1] # return new room number
    # other menu options, player remain in same room
    output("")
    output("What do you want to do today?")
    actions = {"d":"drop item",
               "i":"inspect inventory",
               "p":"pick up item",
               "u":"use item",
               "c":"cancel"}
    for a in actions:
        output("{}....{}".format(a, actions[a]))
    answer = ""
    while answer not in actions:
        answer = input("please type selected letter and press ENTER: ")
    if answer == "i":
        show_inventory(game, player)
    elif answer == "d":
        drop_item(game, player)
    elif answer == "p":
        pickup_item(game, player)
    elif answer == "u":
        use_item(game, player)
    return player.where # return the same room number



# create a game instance
g = Game()

# add rooms with  description and connections.
# Each room will have a unique number and add himself to game
# room number 0
Room(g,"starting lobby", [1, 4], explored = True)
# room number 1
Room(g,"first room", [0,2,6])
# room number 2
Room(g,"storage room", [1,5,7])
# room number 3
# the boss room has 1 to 6 minions and 1 to 3 bosses
Room(g,"boss chamber", [6], monsterchances=[1.0,0.9,0.8,0.5,0.5,0.5],
     bosschances = [1.0,0.15,0.05])
# room number 4
Room(g,"end of the world (game over)", [], explored=True)
# room number 5
Room(g,"npc room", [2,9,10])
# room number 6
Room(g,"gear room", [1,3,10])
# room number 7
Room(g,"trader", [2,5,8])
# room number 8
Room(g,"enemy room", [3,7], monsterchances=[1.0,1.0,1.0,0.9,0.7,0.5,0.2])
# room number 9
Room(g,"empty room", [5,12], itemchances=[])
# room number 10
Room(g,"mini boss",  [5,6], monsterchances=[1.0,0.5,0.5,0.5], bosschances = [0.5])
# room number 11
Room(g,"random room", [10,12])
#room number 12
Room(g,"random room", [11,9])
# items
i=Item(g,"potion of instant healing",mass=0.25)
g.rooms[6].itemnumbers.append(i.number) # puts item i in room 6
# you can use another item for i
i=Item(g,"wheel of cheese",mass=0.50)
g.rooms[2].itemnumbers.append(i.number)
# add effects
e = Effect(g,"teleport",teleport=1)
e.description = "You wake up in a strange room"

# start player in lobby (room 0)
# where = 0 # the actual room number
p = Player(g, where=0) # create player in room 0

# main loop
while len(g.rooms[p.where].connections) > 0:
    if not g.rooms[p.where].explored:
        output("You explore a new room!")
        g.rooms[p.where].explored = True # explore this room
    output("\n\nYou are now here:\n\n{}".format(g.rooms[p.where].info(g)))
    p.where = nextAction(g, p)
    output("\n"*1)
output("\n"*1)
output("Thank you for playing. Have a nice real life")
