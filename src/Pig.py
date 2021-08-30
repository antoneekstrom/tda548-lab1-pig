# /*
#  * The Pig game
#  * See http://en.wikipedia.org/wiki/Pig_%28dice_game%29
#  *
#  */
import random


def run():
    win_points = 20  # Points to win (decrease if testing)
    aborted = False
    # Hard coded players, replace *last* of all with ... (see below)
    # players = [Player(name='Olle'), Player(name='Fia')]
    players = get_players()    # ... this (method to read in all players)

    # prints name of players in the game
    show_players_msg(players)

    welcome_msg(win_points)
    status_msg(players)

    # get a random player to start
    current_player = get_random_player(players)

    # repeat the game loop until a player has won (or a player quits)
    while not game_has_ended(players, win_points) and not aborted:
        # player can choose to roll or hold (or quit the game)
        player_choice = get_player_choice(current_player)

        # handle player choice
        # quit
        if player_choice == "q":
            aborted = True
        # next / hold
        elif player_choice == "n":
            # if the player chooses to hold, update points and select the next player
            hold_pts(current_player)
            current_player = get_next_player(players, current_player)
            status_msg(players)
        # roll
        elif player_choice == "r":
            roll = roll_die()

            # update player points
            next_points = get_next_round_pts(current_player.roundPts, roll)
            current_player.roundPts = next_points

            round_msg(roll, current_player)

            # if the player rolls a 1, select the next player
            if next_points == 0:
                current_player = get_next_player(players, current_player)
                status_msg(players)
        # incorrect choice
        else:
            show_choices_msg()
            pass

    game_over_msg(get_winning_player(players), aborted)


class Player:
    def __init__(self, name=''):
        self.name = name  # default ''
        self.totalPts = 0  # Total points for all rounds
        self.roundPts = 0  # Points for a single round


# ---- Game logic methods --------------
def roll_die():
    return random.randint(1, 6)


def get_next_round_pts(round_total, roll):
    if roll == 1:
        return 0
    else:
        return round_total + roll


def hold_pts(player):
    player.totalPts += player.roundPts
    player.roundPts = 0


def game_has_ended(players, win_points):
    for player in players:
        if player.totalPts >= win_points:
            return True
    return False


def get_next_player(players, current_player):
    current_index = players.index(current_player)
    return players[(current_index + 1) % len(players)]


def get_player_total(player):
    return player.totalPts


def get_winning_player(players):
    return sorted(players, key=get_player_total).pop()


# ---- IO Methods --------------
def welcome_msg(win_pts):
    print("Welcome to PIG!")
    print("First player to get " + str(win_pts) + " points will win!")
    show_choices_msg()


def status_msg(the_players):
    print("Points: ")
    for player in the_players:
        print("\t" + player.name + " = " + str(player.totalPts) + " ")


def round_msg(result, current_player):
    if result > 1:
        print("Got " + str(result) + " running total are " + str(current_player.roundPts))
    else:
        print("Got 1 lost it all!")


def game_over_msg(player, is_aborted):
    if is_aborted:
        print("Aborted")
    else:
        print("Game over! Winner is player " + player.name + " with "
              + str(player.totalPts + player.roundPts) + " points")


def show_choices_msg():
    print("Commands are: r = roll , n = next, q = quit")


def show_players_msg(players):
    print(f"Players are {[player.name for player in players]}")


def get_player_choice(player):
    return input("Player is " + player.name + " > ")


def get_players():
    players = []
    while True:
        response = input("Add a player? (y/n) > ")
        if response.startswith("y"):
            player_name = input("Enter name of the player > ")
            players.append(Player(player_name))
            pass
        else:
            break
    return players


def get_random_player(players):
    return random.choice(players)


# ----- Testing -----------------
# Here you run your tests i.e. call your game logic methods
# to see that they really work (IO methods not tested here)
def test():
    # This is hard coded test data
    # An array of (no name) Players (probably don't need any name to test)
    test_players = [Player(), Player(), Player()]
    sample_rolls = [roll_die() for _ in range(1000)]
    win_pts = 20

    # everything should print True

    # only rolls numbers [1-6]
    print(set(range(1, 7)).issubset(sample_rolls) and set(sample_rolls).issubset(range(1, 7)))

    print(get_next_round_pts(7, 1) == 0)
    print(get_next_round_pts(7, 2) == 9)
    print(get_next_round_pts(0, 1) == 0)
    print(get_next_round_pts(0, 2) == 2)

    p = test_players[0]
    p.roundPts = 6
    p.totalPts = 7
    hold_pts(p)
    print(p.roundPts == 0)
    print(p.totalPts == 6+7)
    p.totalPts = 0

    print(not game_has_ended(test_players, win_pts))
    p.totalPts = 19
    print(not game_has_ended(test_players, win_pts))
    p.totalPts = 20
    print(game_has_ended(test_players, win_pts))

    print(get_next_player(test_players, test_players[0]) == test_players[1])
    print(get_next_player(test_players, test_players[2]) == test_players[0])

    test_players[0].totalPts = 1
    print(get_winning_player(test_players) == test_players[0])
    test_players[1].totalPts = 2
    print(get_winning_player(test_players) == test_players[1])

    exit(0)


if __name__ == "__main__":
    run()
