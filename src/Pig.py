# /*
#  * The Pig game
#  * See http://en.wikipedia.org/wiki/Pig_%28dice_game%29
#  *
#  */
import random


def run():
    # initialize game state
    win_points = 20
    aborted = False
    players = get_players()
    current_player = get_random_player(players)

    # show startup messages
    players_msg(players)
    welcome_msg(win_points)
    status_msg(players)

    # repeat the game loop until a player has won (or a player quits)
    while not game_should_end(players, win_points, aborted):
        player_choice = get_player_choice(current_player)
        current_player, aborted = handle_player_choice(players, current_player, player_choice)

    game_over_msg(get_winning_player(players), aborted)


class Player:
    def __init__(self, name=''):
        self.name = name  # default
        self.total_points = 0  # Total points for all rounds
        self.round_points = 0  # Points for a single round

    def hold_points(self):
        self.total_points += self.round_points
        self.round_points = 0

    def update_round_points_with_roll(self, roll):
        if roll == 1:
            self.round_points = 0
        else:
            self.round_points += roll


# ---- Game logic methods --------------
def handle_player_choice(players, current_player, player_choice):
    aborted = False
    next_player = current_player

    if player_choice == "q":  # quit
        aborted = True
    elif player_choice == "n":  # next / hold
        next_player = player_choice_next(players, current_player)
    elif player_choice == "r":  # roll
        next_player = player_choice_roll(players, current_player)
    else:  # incorrect choice
        choices_msg()

    return next_player, aborted


def player_choice_roll(players, current_player):
    roll = get_die_roll()
    current_player.update_round_points_with_roll(roll)
    round_msg(roll, current_player)
    return determine_next_player_after_roll(players, current_player)


def player_choice_next(players, current_player):
    current_player.hold_points()
    status_msg(players)
    return get_next_player(players, current_player)


def determine_next_player_after_roll(players, current_player):
    if current_player.round_points == 0:
        status_msg(players)
        return get_next_player(players, current_player)
    else:
        return current_player


def game_should_end(players, win_points, aborted):
    return someone_has_won(players, win_points) or aborted


def get_die_roll():
    return random.randint(1, 6)


def someone_has_won(players, win_points):
    for player in players:
        if player.total_points >= win_points:
            return True
    return False


def get_next_player(players, current_player):
    current_index = players.index(current_player)
    return players[(current_index + 1) % len(players)]


def get_player_total(player):
    return player.total_points


def get_winning_player(players):
    return sorted(players, key=get_player_total).pop()


# ---- IO Methods --------------
def welcome_msg(win_pts):
    print("Welcome to PIG!")
    print("First player to get " + str(win_pts) + " points will win!")
    choices_msg()


def status_msg(the_players):
    print("Points: ")
    for player in the_players:
        print("\t" + player.name + " = " + str(player.total_points) + " ")


def round_msg(result, current_player):
    if result > 1:
        print("Got " + str(result) + " running total are " + str(current_player.round_points))
    else:
        print("Got 1 lost it all!")


def game_over_msg(player, is_aborted):
    if is_aborted:
        print("Aborted")
    else:
        print("Game over! Winner is player " + player.name + " with "
              + str(player.total_points + player.round_points) + " points")


def choices_msg():
    print("Commands are: r = roll , n = next, q = quit")


def players_msg(players):
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
    sample_rolls = [get_die_roll() for _ in range(1000)]

    # only rolls numbers [1-6]
    print(set(range(1, 7)).issubset(sample_rolls) and set(sample_rolls).issubset(range(1, 7)))

    # should return the next player
    print(get_next_player(test_players, test_players[0]) == test_players[1])
    print(get_next_player(test_players, test_players[2]) == test_players[0])

    # should return the player with the most points
    test_players[0].total_points = 1
    print(get_winning_player(test_players) == test_players[0])
    test_players[1].total_points = 2
    print(get_winning_player(test_players) == test_players[1])

    exit(0)


if __name__ == "__main__":
    run()
