class Room:
    def __init__(self, name, desc, north, south, west, east):
        self.name = name
        self.desc = desc
        self.north = north
        self.south = south
        self.east = east
        self.west = west

    def hasExit(self,direction):
        if(direction == "north") and (self.north != ""):
            return True

        if (direction == "south") and (self.south != ""):
            return True

        if (direction == "east") and (self.east != ""):
            return True

        if (direction == "west") and (self.west != ""):
            return True

        return False
