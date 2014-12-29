__author__ = 'Itay'


#Tile class represent a tile in a domino game
class Tile:

    #initialize a tile instance
    def __init__(self, num1, num2):
        self.first = min(num1, num2)
        self.second = max(num1, num2)

    # def print_tile(self):
    #     print self.__str__()

    #strin representation for tile
    def __str__(self):
        return'['+str(self.first)+':'+str(self.second)+']'

    def __repr__(self):
        return self.__str__()

    #get left end of tile
    def get_left(self):
        return self.first

    #get right eng of tile
    def get_right(self):
        return self.second

    #change tile's left and right ends
    def rotate_tile(self):
        second = self.first
        self.first = self.second
        self.second = second
        return

    # return the value of the tile
    def get_sum(self):
        if self.first == self.second:
            return self.first+self.second+10
        else:
            return self.first+self.second

