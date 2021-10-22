# escape the castle

from abc import abstractclassmethod
from random import randint, choice
import math
import recursiveBacktracking


ADJACENTTILES = ((1,0), (-1,0), (0, 1), (0,-1))
WEAPONLIST = ('fork', 'spade', 'sword', 'broadsword') #wieghts: 6, 4, 3, 1
FOODLIST = ('potato', 'health potion', 'good soup', 'mouldy bread') #weights 17, 5, 1, 10
ITEMLIST = ('old book', 'key') #weights: 5, 1

f = open('names.txt', 'r')
NAMES = f.readlines()
for i, name in enumerate(NAMES):
    NAMES[i] = name[:-1]


class obstructionInTargetPosition(Exception): pass
class itemNotInInventory(Exception): pass

class Items:
    def __init__(self) -> None:
        maxX = castle.room.maxX; maxY = castle.room.maxY
        self.itemPostions = {}
        self.availableItems = [['weapon',randint(0,maxX+maxY)],
                        ['item',randint(2*len(castle.team.playerList)-1,(maxX*maxY//2)-maxX+maxY)],
                        ['food',randint(3*len(castle.team.playerList)-1, (maxX*maxY//2)-len(castle.team.playerList))]]
    
    def setItemPositions(self):
        # selecting what items to include and where to put them
        grid = castle.room.grid
        for space in grid:
            if self.availableItems:
                ifItem = randint(0,5)
                if ifItem == 0:
                    whichItem = randint(0, len(self.availableItems)-1)
                    if self.availableItems[whichItem][1]:
                        self.availableItems[whichItem][1] -= 1
                        if self.availableItems[whichItem][0] == 'weapon':
                            W = self.createWeaponObj()
                            self.itemPostions[space] = W
                        elif self.availableItems[whichItem][0] == 'item':
                            I = self.createItemObj()
                            self.itemPostions[space] = I
                        elif self.availableItems[whichItem][0] == 'food':
                            F = self.createFoodObj()
                            self.itemPostions[space] = F
            else:
                break
        return self.itemPostions
        #for position in self.__itemPostions:
         #   print(f'there is a {self.__itemPostions[position]} at {position}')
        
    def __getattribute__(self, name):
        return super().__getattribute__(name)
    
    def createWeaponObj(self):
        weight = randint(1,14)
        if weight == 14:
            weaponType = 'broadsword'
            attack = -75
        elif weight >= 11:
            weaponType = 'sword'
            attack = -50
        elif weight >= 7:
            weaponType = 'spade'
            attack = -20
        else:
            weaponType = 'fork'
            attack = -10
        
        return Weapon(weaponType, attack)
    
    def createFoodObj(self):
        weight = randint(1,33)
        if weight == 33:
            foodType = 'good soup'
            healthWhenEaten = randint(8,12)
        elif weight >= 28:
            foodType = 'health potion'
            healthWhenEaten = randint(45,55)
        elif weight >= 18:
            foodType = 'mouldy bread'
            healthWhenEaten = randint(-6, -3)
        else:
            foodType = 'potato'
            healthWhenEaten = randint(4, 8)
            
        return Food(foodType, healthWhenEaten)
    
    def createItemObj(self):
        weight = randint(1,6)
        if weight == 6:
            itemType = 'key'
        else:
            itemType = 'old book'
        
        return Item(itemType)
    
    def use(self, player):
        player.inventory.contents[self.type][0]-=1
        if player.inventory.contents[self.type][0] == 0:
            player.inventory.contents.pop(self.type)
            
    def drop(self, player):
        print(f'you dropped {self.type}')
        castle.room.itemPositions[player.position] = self
        self.use(player)
    
class Weapon(Items):
    def __init__(self, weaponType, attack) -> None:
        self.type = weaponType
        self.attack = attack
        
class Item(Items):
    def __init__(self, itemType) -> None:
        self.type = itemType
        
    def use(self, player):
        super().use(player)
        print(f'you used {self.type}')
        if self.type == 'old book':
            print('you gained ancient knowledge! or smth idk')
        elif self.type == 'key':
            print('something happened... don\'t ask me what tho') # do stuff with probably

class Food(Items):
    def __init__(self, foodType, healthWhenEaten) -> None:
        self.type = foodType
        self.healthWhenEaten = healthWhenEaten
    
    def use(self, player):
        super().use(player)
        player.health += self.healthWhenEaten
        print(f'you ate {self.type}')
        print(f'you gained {self.healthWhenEaten} health')

class Inventory:
    def __init__(self, Id) -> None:
        self.playerId = Id
        self.contents = {}
        self.maxSize = 5
    
    def showInventory(self):
        showInv = ' | '
        if self.contents:
            for item in self.contents:
                showInv += f'{item} [{self.contents[item][0]}] | '
        else:
            showInv += ' | '
        return showInv
    
    def addItemToInv(self, item):
        playerPos = castle.team.playerList[self.playerId].position
        itemType = item.type
        if len(self.contents) == self.maxSize:
            if itemType not in self.contents:
                print(f'your inventory already has {self.maxSize} items inside, you can\'t pick this up')
        if len(self.contents) != self.maxSize or itemType in self.contents:
            checkPickUp = input(f'would you like to pick up {itemType}? (y/n)\n> ')
            if checkPickUp == 'y':
                castle.room.removeItem(playerPos)
                if itemType in self.contents:
                    self.contents[itemType].append(item)
                    self.contents[itemType][0] += 1
                else:
                    self.contents[itemType] = [1, item]
                print('inventory:', self.showInventory())
            else:
                pass
        
        
class Team:
    def __init__(self) -> None:
        self.playerList = []
        while True:
            chooseNo = int(input('How many players are there? (max is 3)\n>'))
            try:
                if chooseNo < 1 or chooseNo > 3:
                    raise ValueError
                break
            except ValueError:
                print(f'{chooseNo} is not in the range of 1 -> 3')
        for player in range(0, chooseNo):
            P = Player(player)
            self.playerList.append(P)
            #P.name = 'Player ' + str(player+1)
        self.totalHealth = chooseNo*100
        
    def __getattribute__(self, name):
        return super().__getattribute__(name)
    
    def updateTotalHealth(self):
        self.totalHealth = 0
        for player in self.playerList:
            self.totalHealth += player.health
        

class Player:
    def __init__(self, Id) -> None:
        self.health = 100
        self.id = Id
        self.name = 'player ' + str(self.id+1)
        self.position = (1,1)
        self.inventory = Inventory(self.id)
        self.currentRoom = (0,0)
    
    def __getattribute__(self, name):
        return super().__getattribute__(name)
    
    def __setattr__(self, name, value):
        self.__dict__[name] = value
            
    def describePlayer(self):
        showInv = self.inventory.showInventory()
        print(f'   -- {self.name} --   \nHealth: {self.health}\nPosition: {self.position}\nInventory: {showInv}')
    
    def movePlayer(self):
        while True:
            try:
                moveX = int(input('horizontal movement\n> '))
                moveY = int(input('vertical movement\n> '))
                newPos = (self.position[0] + moveX, self.position[1] + moveY)
                grid = castle.room.grid
                if newPos in grid:
                    for enemy in castle.room.enemyTeam.enemyList: 
                        enemyPos = enemy.position
                        if enemyPos == newPos:
                            raise obstructionInTargetPosition
                    self.position = newPos
                    print(f'New position: {self.position}')
                    break
                else:
                    raise ValueError
            except obstructionInTargetPosition:
                print('You cannot move there, something is in the way lol. definately no bugs here :)')
            except ValueError:
                print('target position out of room. no cheating allowed')
                
    '''
    PUT THESE MORE INTO THE ITEM CLASSES!!!
    '''
                        
    def attackEnemy(self):
        adjEnemies = []
        for index, enemy in enumerate(castle.room.enemyTeam.enemyList):
            enemyPos = enemy.position
            for coord in ADJACENTTILES:
                if self.position[0] + coord[0] == enemyPos[0] and self.position[1] + coord[1] == enemyPos[1]:
                    adjEnemies.append([enemy, enemyPos]); castle.room.enemyTeam.enemyList.pop(index)
        if adjEnemies:
            for index, enemy in enumerate(adjEnemies):
                attack = input(f'there is an enemy at {enemy[1]} with {enemy[0].health} health. would you like to attack? (y/n)\n> ')
                if attack == 'y':
                    
                    # this could probably be in other objs
                    for item in self.inventory.contents:
                        if item in WEAPONLIST:
                            damageDone = self.inventory.contents[item][1].attack
                            print(f'you attacked {enemy[0].name} with {item}. It lost {damageDone} health.')
                    else:
                        damageDone = 5
                        print(f'you attacked {enemy[0].name} with fist. It lost {damageDone} health.')
                    if enemy[0].health - damageDone < 0:
                        enemy[0].health = 0
                        adjEnemies.pop(index)
                        print(f'{enemy[0].name} died. hopefully')
                    else:
                        enemy[0].health -= damageDone
                        castle.room.enemyTeam.enemyList.append(enemy[0]); adjEnemies.pop(index)
                    
        else:
            print('there are no enemies within reach, can you not read the map???')
            
    def eatFood(self):
        chooseFood = self.checkInput(action='eat', checkList=FOODLIST)
        if chooseFood:
            foodToEat = self.inventory.contents[chooseFood].pop(1)
            foodToEat.use(self)

    def useItem(self):
        chooseItem = self.checkInput(action='use', checkList=ITEMLIST)
        if chooseItem:
            itemToUse = self.inventory.contents[chooseItem].pop(1)
            itemToUse.use(self)
            
    def dropItem(self):
        chooseItem = self.checkInput(action='drop',checkList=ITEMLIST+WEAPONLIST+FOODLIST)
        if chooseItem:
            droppedItem = self.inventory.contents[chooseItem].pop(1)
            droppedItem.drop(self)


    def checkInput(self, action, checkList):
        while True:
            try:
                chooseItem = input(f'what item would you like to {action}\n> ')
                if chooseItem == 'none':
                    return False
                elif chooseItem not in checkList:
                    raise ValueError
                elif chooseItem not in self.inventory.contents:
                    raise itemNotInInventory
                return chooseItem
            except ValueError:
                print('That is not a valid entry, you cant just make stuff up')
            except itemNotInInventory:
                print(f'you don\'t have any {chooseItem} in your inventory, go find one first')
                
class EnemyTeam:
    def __init__(self) -> None:
        self.enemyList = []
        maxX = castle.room.maxX; maxY = castle.room.maxY
        areaAve = (maxX+maxY)//2
        noEs = randint(0,areaAve)
        for enemy in range(noEs):
            if enemy == 0:
                E = Boss(enemy)
            else:
                E = Monster(enemy)
            self.enemyList.append(E)
                            
class Enemy:
    def __init__(self) -> None:
        maxX = castle.room.maxX; maxY = castle.room.maxY
        self.position = (randint(1, maxX),randint(1, maxY))
        if self.position == (1,1):
            shiftPos = randint(1,3)
            if shiftPos == 1:
                self.position = (2,2)
            elif shiftPos == 2:
                self.position = (1,2)
            elif shiftPos == 3:
                self.position = (2,1)
        #print('enemy at', self._position)
    
    def __getattribute__(self, name):
        return super().__getattribute__(name)
    
    def __setattr__(self, name, value):
        self.__dict__[name] = value
    
    def attackPlayer(self, player):
        playerPos = player.position
        for tile in ADJACENTTILES:
            if self.position[0] + tile[0] == playerPos[0] and self.position[1] + tile[1] == playerPos[1]:
                damageDone = self.weapon.attack
                print(f'You were attacked by {self.name} using {self.weapon.type}. You lost {damageDone} health.')
                playerHealth = player.health
                newHealth = playerHealth + damageDone
                if newHealth < 0:
                    newHealth = 0
                player.health = newHealth
                castle.team.updateTotalHealth()
                print(f'Health: {newHealth}')
    
    def move(self):
        # print(self.__position, player.position)
        getDistance = []
        for P in castle.team.playerList:
            playerPos = P.position
            getDistance.append({'player': P, 'distance': self.distance_to(P)})
        getDistance = sorted(getDistance, key=lambda k: k['distance'])
        player = getDistance[0]['player']
        
        playerPos = player.position
        
        for i in range(0, self.speed):
            difference = (playerPos[0]-self.position[0], playerPos[1]-self.position[1])
            xDirection = yDirection = 1
            if difference[0] < 0: xDirection = -1
            if difference[1] < 0: yDirection = -1
            moveBy =(xDirection, yDirection)
            newPos = [self.position[0]+moveBy[0], self.position[1]+moveBy[1]]
            
            
            obstacles = []
            for player in castle.team.playerList:
                obstacles.append(player.position)
            for enemy in castle.room.enemyTeam.enemyList:
                if enemy.id != self.id:
                    obstacles.append(enemy.position)
            for coord in obstacles:
                newPos = self.checkMove(coord, newPos)
                    
        self.position = (newPos[0], newPos[1])
        #print(self.id, self.position)

                    
            # print(moveX, moveY)
           # self._position = (self._position[0] + moveX, self._position[1]+ moveY)
        # print(self.__position, player.position)
    
    def distance_to(self, other):
        otherPos = other.position
        return math.sqrt((self.position[0] - otherPos[0]) ** 2 + (self.position[1] - otherPos[1]) ** 2)
    
    def checkMove(self, otherPos, newPos):
            checkPos = (newPos[0], newPos[1])
            if otherPos != checkPos:
                return newPos
            elif otherPos == checkPos:
                return self.position
            

class Boss(Enemy):
    def __init__(self, Id) -> None:
        super().__init__()
        self.health = 100
        self.name = choice(NAMES)
        self.weapon = Weapon(weaponType='broadsword', attack=-75)
        self.speed = 2
        self.type = 'boss'
        self.id = Id
        
class Monster(Enemy):
    def __init__(self, Id) -> None:
        super().__init__()
        self.health = 10
        self.name = choice(NAMES)
        self.weapon = Weapon(weaponType='spade', attack=-20)
        self.speed = 1
        self.type = 'normal'
        self.id = Id
        
class Castle:
    def __init__(self) -> None:
        self.turn = 1
        self.maxX = 3
        self.maxY = 3
        self.spanningTree = recursiveBacktracking.generateTree(self.maxX, self.maxY)
        self.roomsGrid = {}
        
    def __getattribute__(self, name):
        return super().__getattribute__(name)
    
    def __setattr__(self, name, value):
        self.__dict__[name] = value

    def setUpObjects(self):
        self.roomsGrid[(1,1)] = Room(position=(1,1))
        for item in self.spanningTree:
            self.roomsGrid[item[0]] = Room(position=item[0])

        self.room = Room(position=(0,0))
        self.team = Team()
        self.items = Items()
        self.room.createEnemyTeam()
        self.room.setItemPos()
        
    def displayCastle(self):
        allRooms = []
        for y in range(1, self.maxY+1):
            line = ''
            for x in range(1, self.maxX+1):
                indicator = '['
                thisRoom = self.roomsGrid[(x,y)]
                for player in self.team.playerList:
                    if player.currentRoom == (x,y):
                        indicator += 'p' + player.Id
                        break
                line += indicator + ' '
            allRooms.append(line)
        
        for line in allRooms:
            print(line)

        pass
        
    def gameLoop(self):
        
        while True:
            for player in self.team.playerList:
                chance = randint(1,50)
                if chance == 1:
                    print('you got smote lol')
                    self.team.totalHealth = 0
                if self.team.totalHealth == 0:
                    print('\n -- GAME OVER -- ')
                    exit()
                if player.health == 0 and len(self.team.playerList) > 1:
                    print('you have no health left, your turn is skipped')
                else:
                    self.gameTurn(player, self.turn)
                self.turn += 1
        
    def gameTurn(self, player, turn):
        print(f'\n ----  PLAYER: {player.name} | TURN: {turn}  ---- \n')
        self.room.loadRoom(player)
        player.describePlayer()
        player.movePlayer()
        for enemy in self.room.enemyTeam.enemyList:
            enemy.move()
        self.room.loadRoom(player)
        playerPos = player.position
        itemPos = self.room.itemPositions
        if playerPos in itemPos:
            itemType = itemPos[playerPos].type
            print(f'there is a {itemType} in this space')
            playerId = player.id
            player.inventory.addItemToInv(itemPos[playerPos])
        
        # player.useItem()
        
        while True:
            action = input('\n -- what action would you like to take? -- \na -> attack nearby enemies\ne -> eat food\nu -> use an item\nd -> drop an item\nn -> none\n>')
            if action == 'a':
                player.attackEnemy(); break
            elif action == 'e':
                player.eatFood(); break
            elif action == 'u':
                player.useItem(); break
            elif action == 'd':
                player.dropItem(); break
            elif action == 'key':
                key = Item(itemType='key')
                self.room.itemPositions[player.position] = key
                player.inventory.addItemToInv(key)
                player.useItem()
                break
            elif action == 'n':
                break
            print('that\'s not a valid action')
            
        for enemy in self.room.enemyTeam.enemyList:
            enemy.attackPlayer(player)

    
class Room:
    def __init__(self, position) -> None:
        self.maxX = randint(4,10); self.maxY = randint(4,10)
        self.grid = []
        self.position = position
        for x in range(1, self.maxX+1):
            for y in range(1, self.maxY+1):
                self.grid.append((x,y))
        #print(f'{self.__maxX} across | {self.__maxY} down')
        self.adjacentRooms = []
    
        for item in castle.spanningTree:
            if item[1] == self.position:
                self.adjacentRooms.append(item[0])
            
    
    def setItemPos(self):
        self.itemPositions = castle.items.setItemPositions()
        
    def createEnemyTeam(self):
        self.enemyTeam = EnemyTeam()
    
    def __getattribute__(self, name):
        return super().__getattribute__(name)
        
    def removeItem(self, pos):
        self.itemPositions.pop(pos)
            
    def loadRoom(self, player):
        visGrid = []
        for y in range(1, self.maxY+1):
            line = '  '
            for x in range(1, self.maxX+1):
                for i,  player in  enumerate(castle.team.playerList):
                    playerPos = player.position
                    if playerPos == (x,y):
                        line += 'P' + str(i+1) + '  '; break
                else:
                    for enemy in castle.room.enemyTeam.enemyList:
                        enemyPos = enemy.position
                        enemyType = enemy.type
                        if enemyPos == (x,y):
                            if enemyType == 'boss':
                                line+= 'B   '; break
                            elif enemyType == 'normal':
                                line += 'E   '; break
                    else:
                        for key in self.itemPositions:
                            if key == (x,y):
                                line += 'I   '; break
                        else:
                            line += '.   '
            visGrid.append(line)   
        for line in visGrid:
            print(line)


castle = Castle()
castle.setUpObjects()
castle.displayCastle()
castle.gameLoop()
    
    



        

