import Game
import sys


def main(self):
    """ first project in python workshop,
    build a BlackJack square solitaire game,
    implementation itself in Game file.
    """
    game = Game.Game()
    game.run_game()



if __name__ == "__main__":
    main(sys.argv)