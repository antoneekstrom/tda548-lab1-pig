# /*
#  * The Pig game
#  * See http://en.wikipedia.org/wiki/Pig_%28dice_game%29
#  *
#  */


def run():
    win_points = 20  # Points to win (decrease if testing)
    aborted = False
    # Hard coded players, replace *last* of all with ... (see below)
    players = [Player(name='Olle'), Player(name='Fia')]
    # players = getPlayers()    # ... this (method to read in all players)

    welcome_msg(win_points)
    status_msg(players)
    current = players[0]  # TODO Set random player to start

    # TODO Game logic, using small step, functional decomposition

    game_over_msg(current, aborted)


class Player:

    def __init__(self, name=''):
        self.name = name  # default ''
        self.totalPts = 0  # Total points for all rounds
        self.roundPts = 0  # Points for a single round


# ---- Game logic methods --------------
# TODO
#


# ---- IO Methods --------------
def welcome_msg(win_pts):
    print("Welcome to PIG!")
    print("First player to get " + str(win_pts) + " points will win!")
    print("Commands are: r = roll , n = next, q = quit")


def status_msg(the_players):
    print("Points: ")
    for player in the_players:
        print("\t" + player.name + " = " + str(player.totalPts) + " ")


def round_msg(result, current_player):
    if result > 1:
        print("Got " + result + " running total are " + current_player.roundPts)
    else:
        print("Got 1 lost it all!")


def game_over_msg(player, is_aborted):
    if is_aborted:
        print("Aborted")
    else:
        print("Game over! Winner is player " + player.name + " with "
              + str(player.totalPts + player.roundPts) + " points")


def get_player_choice(player):
    input("Player is " + player.name + " > ")


def get_players():
    # TODO
    pass


# ----- Testing -----------------
# Here you run your tests i.e. call your game logic methods
# to see that they really work (IO methods not tested here)
def test():
    # This is hard coded test data
    # An array of (no name) Players (probably don't need any name to test)
    test_players = [Player(), Player(), Player()]
    # TODO Use for testing of logical methods (i.e. non-IO methods)


if __name__ == "__main__":
    run()
