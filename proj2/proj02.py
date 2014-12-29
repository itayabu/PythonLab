__author__ = 'Itay'
import Tile
import re
import Player


#DobleSix class, if not all tiles are in hands of players, the DoubleSix has the tile that are left
#if DoubleSix is not empty, players can draw a tile from it in their turn
class DoubleSix:

    #initialize the DoubleSix instance
    def __init__(self):
        self.isEmpty = True
        self.list_of_tiles = list()

    # add a tile to the DoubleSix
    def add_tiles(self, tile_hand):
        self.isEmpty = False
        for tile in tile_hand:
            self.list_of_tiles.append(tile[1])

    #draw a tile from the DoubleSix
    def draw_tile(self):
        tile = self.list_of_tiles.pop(0)
        if len(self.list_of_tiles) == 0:
            self.isEmpty = True
        return tile

    # return false iff there are tiles left in DoubleSix
    def is_empty(self):
        return self.isEmpty


#list of play class, represent the list of already played tiles.
#player can add tiles to the list only if his tile suits one of the edges of the list of play
class LOP:

    #initialize the list of play instance
    def __init__(self):
        self.right_end = None
        self.left_end = None
        self.list_of_play = list()

    # return the left end of the list
    def get_left_hand(self):
        return self.left_end

    #return the right end of the list
    def get_right_hand(self):
        return self.right_end

    #add a tile to the lop, receive a tile and one of the ends and put the new tile at this end.
    def add_to_lop(self, tile, place):
        if place == 'e':
            self.right_end = tile.get_right()
            self.list_of_play.append(tile)
        else:
            self.left_end = tile.get_left()
            self.list_of_play.insert(0, tile)

    # receive a number as parameter and return the number of tiles contain this number
    def get_num_of_instance(self, num):
        sums = 0
        for tile in self.list_of_play:
            if tile.get_left() == num or tile.get_right() == num:
                sums += 1
        return sums

    # return the number of tiles in the list
    def count_tiles(self):
        return len(self.list_of_play)

    #return a string of represented tiles in the line
    def lop_to_print(self):
        hand = ''
        for tile in self.list_of_play:
            if hand != '':
                hand += ' ' + tile.__str__()
            else:
                hand += tile.__str__()
        return hand

    #special case for the first tile added to the line- need to update both right and left ends.
    def add_first_tile(self, tile):
        self.right_end = tile.get_right()
        self.left_end = tile.get_left()
        self.list_of_play.append(tile)

    #check if a given tile can continue the right end of the line
    def check_tile_end(self, tile):
        if tile.first == self.right_end:
            return True
        return False

    #check if a given tile can continue the left end of the line
    def check_tile_start(self, tile):
        if tile.second == self.left_end:
            return True
        return False


#game flow class, control the players and their turns.
class Game:
    
    #initialize game instance
    def __init__(self):
        self.player_list = list()
        self.pack = DoubleSix()
        self.lop = LOP()
        self.current_turn = None
        self.no_play_turn = 0           # count turns tha no one played in a row
        self.is_finished = False

    # parse a given file to hands and tiles so each player (or the DoubleSix) can get a hand of tiles
    def file_parser(self, file_path):
        tile_file = open(file_path)
        tile_string = tile_file.read()

        #remove all comments from file
        tile_string = re.sub(re.compile("/\*.*?\*/", re.DOTALL), "",
                        tile_string)
        tile_string = re.sub(re.compile("\"\"\".*?\"\"\"", re.DOTALL), "",
                        tile_string)
        tile_string = re.sub(re.compile("//.*?\n"), "\n",
                        tile_string)
        tile_string = re.sub(re.compile("#.*?\n"), "",
                        tile_string)
        tile_string = re.sub(re.compile("\n+"), "|",
                        tile_string)
        tile_string = re.sub(re.compile("\s"), "",
                        tile_string)

        #split the file to lists of hands containing lists of tiles still as strings
        if tile_string[0] == "|":
            tile_string = tile_string[1:]
        if tile_string[len(tile_string) - 1] == "|":
            tile_string = tile_string[:len(tile_string) - 1]
        hands_list = [row.split('-') for row in tile_string.split('|')]

        #make the tiles from strings
        splitted_hands = []
        for hand in hands_list:
            splitted_hand = []
            for word in hand:
                word = word.strip(' \t\n\r').split(',')
                temp_tile = Tile.Tile(int(word[1]), int(word[2]))
                word = [int(word[0]), temp_tile]
                splitted_hand.append(word)
            splitted_hands.append(splitted_hand)
        return splitted_hands



    #decide witch player will play firs
    def choose_first_player(self):
        max_sum = 0
        max_player = None
        for player in self.player_list:
            for tile in player.tiles:
                current_sum = tile.get_sum()
                if current_sum > max_sum:
                    max_sum = current_sum
                    max_player = player
        self.current_turn = max_player.id

    #add a new player to the game
    def add_player(self, player_id, name, is_human, skill, tiles):
        self.player_list.append(Player.Player(player_id, name, is_human, skill, tiles))

    #play the first turn in the game
    def first_turn(self):
        print_step(self.player_list[self.current_turn-1], self.lop)
        self.player_list[self.current_turn-1].first_turn(self.lop)
        self.current_turn += 1
        if self.current_turn > len(self.player_list):
            self.current_turn = 1

    #play a turn in the game
    def next_turn(self):
        if self.player_list[self.current_turn-1].is_playable(self.lop) or not self.pack.isEmpty:   #if player can play
            print_step(self.player_list[self.current_turn-1], self.lop)
            self.no_play_turn = 0
            self.player_list[self.current_turn-1].move(self.pack, self.lop)
            temp = self.player_list[self.current_turn-1].has_finished()
            if temp:
                print_win(self.current_turn, self.player_list[self.current_turn-1].name)
                self.is_finished = True
                return
        else:                       #if no legal move can be played by this player
            self.no_play_turn += 1
            if self.no_play_turn >= len(self.player_list):  #if no player played for a whole round
                print_draw()
                self.is_finished = True
        self.current_turn += 1
        if self.current_turn > len(self.player_list):
            self.current_turn = 1


#print function
def print_choose_tile(tiles_num):
    print "Choose tile (1-" + tiles_num + "), and place (Start - s, End - e): "


#print function
def print_win(player_id, player_name):
    print "Player " + str(player_id) + ", " + player_name + " wins!"


#print function
def print_draw():
    print "It's a draw!"


#print function
def print_step(player, lop):
    print "\nTurn of " + player.name + " to play, player " + str(player.id) + ":"
    print "Hand :: " + player.hand_to_str()
    print "LOP  :: " + lop.lop_to_print()


#start the game- read thi input file and set up players and game round
def game_set_up(game):
    print "Welcome to Domino!"
    file_path = raw_input("'tile' file path: ")
    tiles = game.file_parser(file_path)
    num_of_players = raw_input("number of players (1-4): ")
    for i in xrange(1, int(num_of_players)+1):
        player_name, is_human = raw_input("player " + str(i) + "name: "), raw_input("Human player (y/n): ")
        game.add_player(i, player_name, is_human,
                        raw_input("Computer skill: Easy (e), Medium (m): ") if is_human == 'n' else "", tiles[i-1])
    for i in xrange(int(num_of_players)+1, 5):
        game.pack.add_tiles(tiles[i-1])


#main function, set up game, run the turns and close the game.
def main():
    game = Game()
    game_set_up(game)
    game.choose_first_player()
    game.first_turn()
    while not game.is_finished:
        game.next_turn()
    return

if __name__ == "__main__":
    main()
