from Room import Room


class Dungeon:
    def __init__(self):
        self.currentRoom = 0
        self.roomMap ={}

    def Init(self):
        print("init")

        self.roomMap["room 0"] = Room("room 0", "You are standing in the entrance hall\nAll adventures start here", "room 1", "", "", "")
        self.roomMap["room 1"] = Room("room 1", "You are in room 1","", "room 0", "room 3", "room 2")
        self.roomMap["room 2"] = Room("room 2", "You are in room 2", "room 4", "", "", "")
        self.roomMap["room 3"] = Room("room 3", "You are in room 3", "", "", "", "room 1")
        self.roomMap["room 4"] = Room("room 4", "You are in room 4", "", "room 2", "room 5", "")
        self.roomMap["room 5"] = Room("room 5", "You are in room 5", "", "room 1", "", "room 4")

        self.currentRoom = "room 0"

    def DisplayCurrentRoom(self):
        print(self.roomMap[self.currentRoom].desc)

        print("Exits")
        exits = ["NORTH", "SOUTH","EAST","WEST"]
        exitStr = ""

        for i in exits:
            if self.roomMap[self.currentRoom].hasExit(i.lower()):
                exitStr += i + " "
        print(exitStr)

    def isValidMove(self, direction):
        return self.roomMap[self.currentRoom].hasExit(direction)

    def MovePlayer(self,direction):
        if self.isValidMove(direction):
            if direction == "north":
                self.currentRoom = self.roomMap[self.currentRoom].north
                return

            if direction == "south":
                self.currentRoom = self.roomMap[self.currentRoom].south
                return

            if direction == "east":
                self.currentRoom = self.roomMap[self.currentRoom].east
                return

            if direction == "west":
                self.currentRoom = self.roomMap[self.currentRoom].west
                return