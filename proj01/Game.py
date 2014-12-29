__author__ = 'Itay'
import cards

class Game():
    """ BlackJack square solitaire implementation game
        each game player receive a 'square' Tableau consist of 9 possible blackjack hands and 4 trash cards.
        player need to maximize his score by placing the cards to fit the best BlackJack ands as possible.
    """

    def __init__(self):
        """ initialize all instance parameters"""
        self.cardPlace = {x: x for x in range(1, 21)}
        self.count__used_slots = 1
        self.my_deck = cards.Deck()
        self.my_deck.shuffle()

    def run_game(self):
        """main method, manage the game flow"""
        self.display()
        #as long as there are cards to draw:
        while self.count__used_slots <= 16:
            user_choice = raw_input(
                "Choose an option: d - draw a card, s - simple calculation, a - advanced calculation,"
                " q - quit: ").lower()
            if user_choice == "d":
                self.draw_card()
            elif user_choice == "s":
                self.simple_calc()
            elif user_choice == "a":
                self.advanced_calc()
            elif user_choice == "q":
                exit()
            else:
                print "Error: an invalid choice was made"
        #when all places are taken
        while True:
            user_choice = raw_input("Choose an option: s - simple calculation, a - advanced calculation, q - quit: ") \
                .lower()
            if user_choice == "s":
                self.simple_calc()
            elif user_choice == "a":
                self.advanced_calc()
            elif user_choice == "q":
                exit()
            else:
                print "Error: an invalid choice was made"

    def display(self):
        """ print the game table"""
        print "Tableau:"
        print "%4s %4s %4s %4s %4s" % (self.cardPlace[1], self.cardPlace[2], self.cardPlace[3], self.cardPlace[4],
                                       self.cardPlace[5])
        print "%4s %4s %4s %4s %4s" % (self.cardPlace[6], self.cardPlace[7], self.cardPlace[8], self.cardPlace[9],
                                       self.cardPlace[10])
        print "%9s %4s %4s" % (self.cardPlace[11], self.cardPlace[12], self.cardPlace[13])
        print "%9s %4s %4s" % (self.cardPlace[14], self.cardPlace[15], self.cardPlace[16])
        print
        print "Discards: %4s %4s %4s %4s" % (
            self.cardPlace[17], self.cardPlace[18], self.cardPlace[19], self.cardPlace[20])

    def draw_card(self):
        """ manage a single card dealt to the user"""
        current_card = self.my_deck.deal()
        print "Card dealt:   ", current_card
        good_place = False
        while not good_place:
            current_place = raw_input("Choose location (1 - 20) to place the new card:")
            if not (current_place.isdigit()):
                print "Error: input is not an integer"
                continue
            current_place = int(current_place)
            if current_place >= 21 or current_place <= 0:
                print "Error: input is out of range"
            elif not isinstance(self.cardPlace[current_place], int):  # if slot is already taken
                print "Error: a card was already placed in this spot"
            else:
                good_place = True
        self.update_tableau(current_card, int(current_place))
        print '\n'
        self.display()

    def update_tableau(self, card, place):
        """put the card in the given slot and update cards count if needed"""
        self.cardPlace[place] = card
        if place <= 16:
            self.count__used_slots += 1



    def make_hands_list(self):
        """ return a list of lists, each list contain a hand of blackjack hand"""
        num_dict = {x: self.cards_to_numbers(self.cardPlace[x]) for x in range(1, 21)}
        hands_list = [[num_dict[1], num_dict[2], num_dict[3], num_dict[4], num_dict[5]],
                      [num_dict[6], num_dict[7], num_dict[8], num_dict[9], num_dict[10]],
                      [num_dict[11], num_dict[12], num_dict[13]],
                      [num_dict[14], num_dict[15], num_dict[16]],
                      [num_dict[1], num_dict[6]],
                      [num_dict[2], num_dict[7], num_dict[11], num_dict[14]],
                      [num_dict[3], num_dict[8], num_dict[12], num_dict[15]],
                      [num_dict[4], num_dict[9], num_dict[13], num_dict[16]],
                      [num_dict[5], num_dict[10]]]
        return hands_list

    def simple_calc(self):
        """ calculate each hand (list of ints) separately and return the score of current hand"""
        point_count = 0
        hands_list = self.make_hands_list()
        for hand in hands_list:
            count = 0
            for card in hand:
                count += card
                if card == 1:
                    count += 10
            for card in hand:
                if (card == 1) and (count > 21):
                    count -= 10
            hand_count = self.calc_hand(count)
            if (hand_count == 7) and (len(hand) == 2):
                hand_count = 10
            point_count +=hand_count
        print "The total score (simple algorithm) is: ", point_count

    def advanced_calc(self):
        """ calculate all hands together, maximize score by controlling all aces together"""
        cards_as_nums = []
        for card in self.cardPlace:
            cards_as_nums.append(self.cards_to_numbers(self.cardPlace[card]))
        aces = cards_as_nums.count(1)
        print "The total score (advanced algorithm) is: ", self.recursive_get_best_score(aces, cards_as_nums, 0)

    def recursive_get_best_score(self, aces, card_list, current_index):
        """ maximize score by returning the higher score given for ace as 1 or 11"""
        if aces == 0:
            return self.count_hands(card_list)
        changed_index = card_list.index(1, current_index)
        score_one = self.recursive_get_best_score(aces - 1, card_list, changed_index + 1)
        card_list[changed_index] = 11
        score_two = self.recursive_get_best_score(aces - 1, card_list, changed_index + 1)
        card_list[changed_index] = 1
        return max(score_one, score_two)

    def count_hands(self, hands):
        """ count the sum score of all hands on deck"""
        hands_count = 0
        hands_count += self.calc_hand(hands[0] + hands[1] + hands[2] + hands[3] + hands[4])
        hands_count += self.calc_hand(hands[5] + hands[6] + hands[7] + hands[8] + hands[9])
        hands_count += self.calc_hand(hands[10] + hands[11] + hands[12])
        hands_count += self.calc_hand(hands[13] + hands[14] + hands[15])
        hands_count += self.calc_hand(hands[0] + hands[5])
        hands_count += self.calc_hand(hands[1] + hands[6] + hands[10] + hands[13])
        hands_count += self.calc_hand(hands[2] + hands[7] + hands[11] + hands[14])
        hands_count += self.calc_hand(hands[3] + hands[8] + hands[12] + hands[15])
        hands_count += self.calc_hand(hands[4] + hands[9])
        if hands[0]+hands[5] == 21:
            hands_count +=3
        if hands[4]+hands[9] == 21:
            hands_count +=3
        return hands_count

    def calc_hand(self, count):
        """ score hands by their value"""
        if count == 21:
            return 7
        if count == 20:
            return 5
        if count == 19:
            return 4
        if count == 18:
            return 3
        if count <= 17:
            if count == 17:
                return 2
            else:
                return 1
        else:
            return 0

    def cards_to_numbers(self, card):
        """ return cards value, if there is no card, return 0"""
        if isinstance(card, cards.Card):
            val = card.get_value()
            return val
        else:
            return 0
