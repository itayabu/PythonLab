import Tile
__author__ = 'Itay'


#player class manage players both human and computers
class Player:

    #initialize a player instance
    def __init__(self, player_id, name, is_human, skill, tiles):
        self.id = player_id
        self.name = name
        if is_human == 'n':
            self.is_human = False
            self.skill = skill
        else:
            self.is_human = True
        self.tiles = list()
        for tile in tiles:
            self.tiles.insert(int(tile[0]), tile[1])

    # movement of player each turn
    def move(self, deck, lop):
        if self.is_human:
            self.human_move(deck, lop)
        elif self.skill == 'e':
            self.easy_comp_move(deck, lop)
        else:
            self.smart_comp_move(deck, lop)

    #human move: choosing if draw a tile or put a tile in row
    def human_move(self, deck, lop):
        legal_input = False
        while not legal_input:
            choice = raw_input("Choose action: Tile (t) or Draw (d): ")
            if choice.lower() == 'd': #if draw is chosen
                if not deck.is_empty():
                    self.tiles.append(deck.draw_tile())
                    legal_input = True
                    break
            else:           #if put tile is chosen
                choice = raw_input("Choose tile (1-" + str(len(self.tiles)) + "), and place (Start - s, End - e): ")
                tile_id = int(choice[0])
                place = choice[2].lower()
                tile = self.tiles.pop(tile_id-1)
                if self.check_attached_tile(tile, lop, place):
                    lop.add_to_lop(tile, place)
                    legal_input = True
                    break
                else:
                    tile.rotate_tile()
                if self.check_attached_tile(tile, lop, place):
                    lop.add_to_lop(tile, place)
                    legal_input = True
                    break
                tile.rotate_tile()
                self.tiles.insert(tile_id-1, tile)
            print "Error: Illegal move"

    #check if player can play on the row at all
    def is_playable(self, lop):
        for tile in self.tiles:
            if lop.check_tile_end(tile) or lop.check_tile_start(tile):
                return True
            tile.rotate_tile()
            if lop.check_tile_end(tile) or lop.check_tile_start(tile):
                tile.rotate_tile()
                return True
            tile.rotate_tile()
        return False

    #play the easy computer player
    def easy_comp_move(self, deck, lop):
        for i in range(len(self.tiles)):
            tile = self.tiles.pop(i)
            if self.check_attached_tile(tile, lop, 'e'):
                lop.add_to_lop(tile, 'e')
                return
            tile.rotate_tile()
            if self.check_attached_tile(tile, lop, 's'):
                lop.add_to_lop(tile, 's')
                return
            if self.check_attached_tile(tile, lop, 'e'):
                lop.add_to_lop(tile, 'e')
                return
            tile.rotate_tile()
            if self.check_attached_tile(tile, lop, 's'):
                lop.add_to_lop(tile, 's')
                return
            self.tiles.insert(i, tile)
        if not deck.is_empty():
            self.tiles.append(deck.draw_tile())


    def smart_comp_move(self, deck, lop):
        apperance_list = [0, 0, 0, 0, 0, 0, 0]
        for i in range(0, 7):
            apperance_list[i] = (7 - lop.get_num_of_instance(i))
            apperance_list[i] -= self.get_num_of_instance(i)
        all_tiles = float(28 - lop.count_tiles() - len(self.tiles))
        mintile = (float(2), 0, '', '')
        start = lop.get_left_hand()
        end = lop.get_right_hand()
        for tile in self.tiles: #check all combinations for all tile and keep the best match
            place = self.tiles.index(tile)
            if (tile.get_left() == end) and (float(apperance_list[tile.get_right()])/all_tiles < mintile[0]):
                mintile = (float(apperance_list[tile.get_right()])/all_tiles, place, 'e', '')
            if (tile.get_left() == start) and (float(apperance_list[tile.get_right()])/all_tiles < mintile[0]):
                mintile = (float(apperance_list[tile.get_right()])/all_tiles, place, 's', 'r')
            if (tile.get_right() == end) and (float(apperance_list[tile.get_left()])/all_tiles < mintile[0]):
                mintile = (float(apperance_list[tile.get_left()])/all_tiles, place, 'e', 'r')
            if (tile.get_right() == start) and (float(apperance_list[tile.get_left()])/all_tiles < mintile[0]):
                mintile = (float(apperance_list[tile.get_left()])/all_tiles, place, 's', '')

        #put the best match in the lop or draw a card
        if mintile[3] == 'r':
            self.tiles[mintile[1]].rotate_tile()
        if mintile[0] > 1:
            self.tiles.append(deck.draw_tile())
            return
        tile = self.tiles.pop(mintile[1])
        if mintile[2] == 's':
            if lop.check_tile_start(tile):
                lop.add_to_lop(tile, 's')
                return
            tile.rotate_tile()
            lop.add_to_lop(tile, 's')
            return
        if mintile[2] == 'e':
            if lop.check_tile_end(tile):
                lop.add_to_lop(tile, 'e')
                return
            tile.rotate_tile()
            lop.add_to_lop(tile, 'e')
        return

    # receive a number as parameter and return the number of tiles contain this number in player's hand
    def get_num_of_instance(self, num):
        sums = 0
        for tile in self.tiles:
            if tile.get_left() == num or tile.get_right() == num:
                sums += 1
        return sums

    #play the first turn in a game (player do not choose his play
    def first_turn(self, lop):
        lop.add_first_tile(self.tiles.pop(0))

    # check if a given tile is suited for a given end of the row
    def check_attached_tile(self, tile, lop, place):
        if place == 's':
            return lop.check_tile_start(tile)
        else:
            return lop.check_tile_end(tile)

    #translate the tiles in player's hand to a string
    def hand_to_str(self):
        hand = ''
        for tile in self.tiles:
            if hand != '':
                hand += ' ' + str(tile)
            else:
                hand += str(tile)
        return hand

    #return true iff player finished his tiles in hand
    def has_finished(self):
        if len(self.tiles) == 0:
            return True
        return False