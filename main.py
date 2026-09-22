from util import *
from time import sleep
import importlib

from getch import getch
from MancalaBoard import *
from console_screen import ConsoleScreen
import screen_templates

ai_speed = 1

board = MancalaBoard()
screen = ConsoleScreen()


def draw_main_board(screen):
    global board
    screen.clear_board()
    screen.draw_header()
    screen.draw_template(screen.board_offset_y + 3, screen.board_offset_x, board.get_string_list())


def draw_ai_selection(screen, player_files, player_num=1):

    players = printable_players(player_files)
    options = [f"Select an A.I. to play Player {player_num} ?"]

    for i, name in enumerate(players):
        options.append(f'({i}) {name}')

    screen.draw_menu(options)


def get_ai_selection(screen, player_files, player_num=1):
    draw_ai_selection(screen, player_files, player_num)

    index = 'not set'
    while ((not index.isnumeric()) or (int(index) < 0 or int(index) > len(player_files))):
        index = getch(list(map(str, list(range(len(player_files))))))

    return player_files[int(index)]


def play_many_games(screen, num_games, players):
    wins = [0, 0, 0]
    screen.print_message(f'{get_printable_name(players[0])} vs {get_printable_name(players[1])} with {board.starting_stones} stones', -6)

    for i in range(num_games):
        screen.print_message(f'Playing Game {i + 1} of {num_games}   ', -4)
        screen.print_status_bar(i, num_games, 8)

        winner = play_game(screen, players, False)
        if winner <= 0:
            wins[0] += 1
        else:
            wins[winner] += 1
    return wins


def play_game(screen, players, print_board_during_play=True):
    global board
    row = screen.board_offset_y
    col = screen.board_offset_x

    if len(players) < 2:
        raise Exception("Two players required to play the game!")

    # Initialize the board
    board.reset()
    board.set_player_names(get_printable_name(players[0]), get_printable_name(players[1]))
    player_objects = []

    turn = 1
    move_num = -1

    # Load the AI modules, when necessary
    for i in range(2):
        if players[i] == 'Human':
            player_objects.append(None)
        else:
            module_name = importlib.import_module('players.' + players[i])
            class_name = get_class_name(players[i])
            ai_class = getattr(module_name, class_name)
            ai_instance = ai_class(i+1)
            player_objects.append(ai_instance)

    # Begin game loop
    while not board.is_game_over():
        if print_board_during_play:
            draw_main_board(screen)
        turn = board.player_num
        turn_idx = turn - 1
        move_num = -1
        # i = getch(['q'])
        valid_moves = board.get_valid_moves()

        try:
            if players[turn_idx] == 'Human':
                # If player turn is human, get the move
                my_move = '-1'
                while not my_move.isnumeric() or int(my_move) not in valid_moves:
                    screen.print_message("Enter your move by index: ")
                    my_move = getch(['1', '2', '3', '4', '5', '6', 'p'])
                    if my_move == 'p':
                        return 0

                move_num = int(my_move)
            else:
                # If player is AI, get the move from the AI
                board_copy = board.clone()
                move_num = (player_objects[turn_idx]).get_move(board_copy)
                if print_board_during_play and ai_speed > 0:
                    screen.print_message(f'Player {turn} selected {move_num}.')
                    sleep(ai_speed)
        except InvalidMoveException as e:
            if print_board_during_play:
                screen.print_message(f'{str(e)}. Press <Q> to quit')
                _ = getch(['q'])
            # The other player wins
            return (turn + 1) % 2

        board.make_move(move_num)

    if print_board_during_play:
        draw_main_board(screen)
    board.collect()
    if print_board_during_play:
        draw_main_board(screen)
    return board.get_winner()


def draw_many_games_results(screen, players, p1_results, p2_results):
    screen.clear()
    screen.draw_header()

    row = screen.board_offset_y + 4
    col = screen.board_offset_x

    screen.draw_template(row, col, screen_templates.multi_game_results_2)
    player_names = printable_players(players)

    screen.addstr(row + 1, col + 2, player_names[0])
    screen.addstr(row + 1, col + 55, player_names[1])

    col += 5
    row += 7
    screen.addstr(row, col, f'{p1_results[0][1]:>4}')
    screen.addstr(row+1, col, f'{p1_results[0][2]:>4}')
    screen.addstr(row+2, col, f'{p1_results[0][0]:>4}')

    col += 7
    screen.addstr(row, col, f'{p1_results[2][1]:>4}')
    screen.addstr(row+1, col, f'{p1_results[2][2]:>4}')
    screen.addstr(row+2, col, f'{p1_results[2][0]:>4}')

    col += 7
    screen.addstr(row, col, f'{p1_results[4][1]:>4}')
    screen.addstr(row+1, col, f'{p1_results[4][2]:>4}')
    screen.addstr(row+2, col, f'{p1_results[4][0]:>4}')

    col += 10
    screen.addstr(row, col, f'{p1_results[1][2]:>4}')
    screen.addstr(row+1, col, f'{p1_results[1][1]:>4}')
    screen.addstr(row+2, col, f'{p1_results[1][0]:>4}')

    col += 7
    screen.addstr(row, col, f'{p1_results[3][2]:>4}')
    screen.addstr(row+1, col, f'{p1_results[3][1]:>4}')
    screen.addstr(row+2, col, f'{p1_results[3][0]:>4}')

    col += 7
    screen.addstr(row, col, f'{p1_results[5][2]:>4}')
    screen.addstr(row+1, col, f'{p1_results[5][1]:>4}')
    screen.addstr(row+2, col, f'{p1_results[5][0]:>4}')

    # Print Player 2 results
    col += 15
    screen.addstr(row, col, f'{p2_results[0][1]:>4}')
    screen.addstr(row+1, col, f'{p2_results[0][2]:>4}')
    screen.addstr(row+2, col, f'{p2_results[0][0]:>4}')

    col += 7
    screen.addstr(row, col, f'{p2_results[2][1]:>4}')
    screen.addstr(row+1, col, f'{p2_results[2][2]:>4}')
    screen.addstr(row+2, col, f'{p2_results[2][0]:>4}')

    col += 7
    screen.addstr(row, col, f'{p2_results[4][1]:>4}')
    screen.addstr(row+1, col, f'{p2_results[4][2]:>4}')
    screen.addstr(row+2, col, f'{p2_results[4][0]:>4}')

    col += 10
    screen.addstr(row, col, f'{p2_results[1][2]:>4}')
    screen.addstr(row+1, col, f'{p2_results[1][1]:>4}')
    screen.addstr(row+2, col, f'{p2_results[1][0]:>4}')

    col += 7
    screen.addstr(row, col, f'{p2_results[3][2]:>4}')
    screen.addstr(row+1, col, f'{p2_results[3][1]:>4}')
    screen.addstr(row+2, col, f'{p2_results[3][0]:>4}')

    col += 7
    screen.addstr(row, col, f'{p2_results[5][2]:>4}')
    screen.addstr(row+1, col, f'{p2_results[5][1]:>4}')
    screen.addstr(row+2, col, f'{p2_results[5][0]:>4}')

    col = col = screen.board_offset_x + 11
    row += 4
    screen.addstr(row, col, f'{sum([p1_results[0][1], p1_results[1][2], p1_results[2][1], p1_results[3][2], p1_results[4][1], p1_results[5][2]]):>4}')
    screen.addstr(row+1, col, f'{sum([p1_results[0][2], p1_results[1][1], p1_results[2][2], p1_results[3][1], p1_results[4][2], p1_results[5][1]]):>4}')
    screen.addstr(row+2, col, f'{sum([p1_results[0][0], p1_results[1][0], p1_results[2][0], p1_results[3][0], p1_results[4][0], p1_results[5][0]]):>4}')

    col += 54
    screen.addstr(row, col, f'{sum([p2_results[0][1], p2_results[1][2], p2_results[2][1], p2_results[3][2], p2_results[4][1], p2_results[5][2]]):>4}')
    screen.addstr(row+1, col, f'{sum([p2_results[0][2], p2_results[1][1], p2_results[2][2], p2_results[3][1], p2_results[4][2], p2_results[5][1]]):>4}')
    screen.addstr(row+2, col, f'{sum([p2_results[0][0], p2_results[1][0], p2_results[2][0], p2_results[3][0], p2_results[4][0], p2_results[5][0]]):>4}')


def main(screen):
    global board
    global ai_speed

    try:
        screen.hide_cursor()
        screen.clear()

        # Main Loop
        screen.set_header(screen_templates.header_display)
        screen.draw_menu(screen_templates.main_menu_options)

        selection = 'noop'

        while selection and selection.lower() != 'q':
            players = []
            selection = getch(['1', '2', '3', 'o', 'q'])

            if selection == '3':  # Two Human Players
                players.append('Human')
                players.append('Human')

                char = 'r'
                while char == 'r':
                    winner = play_game(screen, players)
                    # Print winner
                    screen.print_message("Game Over!")
                    if winner == -1:
                        screen.print_message("Tie Game! No winner.", 13)
                    else:
                        screen.print_message(f"{get_printable_name(players[winner - 1])} as Player {winner}, is the Winner!", 13)
                    screen.print_message("Press <R> for a rematch", 14)
                    screen.print_message("Press <Q> to return to main menu", 15)
                    char = getch(['q', 'r'])

            else:
                player_files = load_player_files()
                if len(player_files) < 1:
                    screen.print_message("There are no AI's in the 'players' folder to play against. Press 'C' to continue.")
                    _ = getch(['c'])
                    screen.clear_message()
                    continue

                if selection == '1':
                    screen.draw_menu(screen_templates.player_select_options)

                    player_num = getch(['1', '2', 'q'])
                    if player_num == 'q':
                        continue

                    player_num = int(player_num)
                    ai_num = 1 if player_num == 2 else 2

                    players.append('Human')

                    # Play against a single custom AI
                    ai_player = get_ai_selection(screen, player_files, ai_num)

                    # Make sure to place the '1' first in the list
                    if player_num == 1:
                        players.append(ai_player)
                    else:
                        players.insert(0, ai_player)

                    pause = 'r'
                    while pause == 'r':
                        winner = play_game(screen, players)
                        # Print winner
                        screen.print_message("Game Over!")
                        if winner == -1:
                            screen.print_message("Tie Game! No winner.", 13)
                        else:
                            screen.print_message(f"{get_printable_name(players[winner - 1])} as Player {winner}, is the Winner!", 13)
                        screen.print_message("Press <R> for a rematch", 14)
                        screen.print_message("Press <Q> to return to main menu", 15)
                        pause = getch(['q', 'r'])

                elif selection == '2':
                    screen.draw_menu(screen_templates.num_games_options)
                    sub_selection = getch(['1', '2', '3', '4'])

                    if sub_selection == '1':
                        pause = 'r'

                        # Play two custom AI's against each other
                        first_player = get_ai_selection(screen, player_files, 1)
                        screen.print_message(f"Player 1: {get_printable_name(first_player)}")
                        players.append(first_player)

                        players.append(get_ai_selection(screen, player_files, 2))

                        while pause == 'r':
                            winner = play_game(screen, players)
                            if winner == -1:
                                screen.print_message("Tie! No winner.")
                            else:
                                screen.print_message(f"{get_printable_name(players[winner - 1])} as Player {winner}, is the Winner!", 13)
                            screen.print_message("Press <R> for a rematch", 14)
                            screen.print_message("Press <Q> to return to main menu", 15)
                            pause = getch(['q', 'r'])
                    elif sub_selection == '2' or sub_selection == '3':  # Play two custom AI's against each other for 500 games (per side per starting_stone size) and display the results

                        num_games = 500 if sub_selection == '2' else 100

                        # Results will be stored in these lists, which will be used to display the results
                        # The format will be [[[wins, losses, ties], [wins,losses, ties]], [[wins, losses, ties], [wins,losses, ties]], [[wins, losses, ties], [wins,losses, ties]]]
                        #                               /\                   /\                      /\                   /\                      /\                   /\
                        #                         3 Starting Stones    3 Starting Stones       4 Starting Stones    4 Starting Stones       5 Starting Stones    5 Starting Stones
                        #                        as starting player    as second player        as starting player   as second player        as starting player   as second player
                        player_1_results = []
                        player_2_results = []
                        original_starting_stones = board.starting_stones

                        players = []
                        players.append(get_ai_selection(screen, player_files, 1))
                        players.append(get_ai_selection(screen, player_files, 2))

                        players2 = players[::-1]
                        screen.clear()
                        screen.draw_header()

                        for starting_stones in range(3, 6):
                            board.set_starting_stones(starting_stones)
                            wins = play_many_games(screen, num_games, players)
                            # wins = [ties, player1_wins, player2_wins]
                            wins2 = play_many_games(screen, num_games, players2)
                            # wins = [ties, player2_wins, player1_wins]
                            player_1_results.append(wins)
                            player_1_results.append(wins2)
                            player_2_results.append(wins2)
                            player_2_results.append(wins)

                        draw_many_games_results(screen, players, player_1_results, player_2_results)

                        board.set_starting_stones(original_starting_stones)
                        screen.print_message("Press <Q> to return to the main menu", 9)
                        pause = getch(['q'])

                    elif sub_selection == '4' or sub_selection == '5':
                        original_ai_speed = ai_speed
                        ai_speed = 0

                        num_games = 1000

                        # Play two custom AI's against each other
                        first_player = get_ai_selection(screen, player_files, 1)
                        screen.print_message(f"Player 1: {get_printable_name(first_player)}")
                        players.append(first_player)

                        players.append(get_ai_selection(screen, player_files, 2))

                        play_until_player_num_wins = 1
                        if sub_selection == '5':
                            play_until_player_num_wins = 2

                        while num_games > 0:
                            winner = play_game(screen, players)
                            if winner > 0 and winner == play_until_player_num_wins:
                                screen.print_message(f"{get_printable_name(players[winner - 1])} as Player {winner}, is the Winner!")
                                break
                            num_games -= 1

                        if num_games == 0:
                            screen.print_message(f"Player {play_until_player_num_wins} did not win any games!", 1)

                        screen.print_message("Press <Q> to return to the main menu", 14)
                        ai_speed = original_ai_speed
                        pause = getch(['q'])

                elif selection == 'o':
                    screen.draw_menu(screen_templates.options_menu, [board.starting_stones])
                    sub_selection = getch(['1', 'q'])
                    if sub_selection == '1':
                        screen.draw_menu(screen_templates.change_starting_stones)
                        new_stone_count = getch(['2', '3', '4', '5'])
                        board.set_starting_stones(int(new_stone_count))
                        screen.print_message(f"Starting stones changed to {new_stone_count}. Press <Q> to return to main menu", 14)
                        _ = getch(['q'])
                elif selection == 'q':
                    break
            screen.clear()
            screen.draw_menu(screen_templates.main_menu_options)
    finally:
        screen.show_cursor()
        screen.reset()
        screen.clear()


if __name__ == "__main__":
    try:
        main(screen)
    except KeyboardInterrupt:
        screen.show_cursor()
        screen.reset()
        screen.clear()
        print("\nGame ended by user (Ctrl+C pressed)\n")
