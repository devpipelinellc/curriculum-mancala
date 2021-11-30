from util import *
from time import sleep
import importlib

import curses

from console_screen import ConsoleScreen
from getch import getch
from screens import *
from MancalaBoard import *

ai_speed = 1

board = MancalaBoard()

def draw_main_board(screen):
   global board
   screen.clear_board()
   screen.draw_header()
   screen.draw_template(screen.board_offset_y + 3, screen.board_offset_x, board.get_string_list())
   screen.refresh()

def draw_ai_selection(screen, player_files, player_num = 1):
   
   players = printable_players(player_files)
   options = [f"Select an A.I. to play Player {player_num} ?"]

   for i, name in enumerate(players):
      options.append(f'({i}) {name}')
   
   screen.draw_menu(options)

def get_ai_selection(screen, player_files, player_num = 1):
   draw_ai_selection(screen, player_files, player_num)
   
   index = 'not set'
   while ((not index.isnumeric()) or (int(index) < 0 or int(index) > len(player_files))):
      index = getch(list(map(str, list(range(len(player_files))))))
   
   return player_files[int(index)]

def play_many_games(screen, num_games, players):
   wins = [0,0,0]
   for i in range(num_games):
      screen.print_message('game: ' + str(i))
      screen.print_status_bar(i, num_games, 10)
      
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
   board = MancalaBoard()
   board.set_player_names(get_printable_name(players[0]), get_printable_name(players[1]))
   player_objects = []
   # winner = ''
   turn = 1
   move_num = -1
   # message = ''
   
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
               my_move = getch(['1','2','3','4','5','6','p'])
               if my_move == 'p':
                  return 0
               
            move_num = int(my_move)
         else:
            # If player is AI, get the move from the AI
            move_num = (player_objects[turn_idx]).get_move(board)
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

def draw_many_games_results(screen, players, wins, wins2):
   screen.clear_board()
   screen.draw_header()
   
   row = screen.board_offset_y + 4
   col = screen.board_offset_x

   screen.draw_template(row, col, multi_game_results)
   
   player_names = printable_players(players)

   screen.addstr(row + 1, col + 2, player_names[0])
   screen.addstr(row + 1, col + 27, player_names[1])

   col += 5
   row += 5
   screen.addstr(row, col, f'{wins[1]:>4}')
   screen.addstr(row+1, col, f'{wins[2]:>4}')
   screen.addstr(row+2, col, f'{wins[0]:>4}')
   col += 10
   screen.addstr(row, col, f'{wins2[2]:>4}')
   screen.addstr(row+1, col, f'{wins2[1]:>4}')
   screen.addstr(row+2, col, f'{wins2[0]:>4}')
   
   col += 15
   screen.addstr(row, col, f'{wins2[1]:>4}')
   screen.addstr(row+1, col, f'{wins2[2]:>4}')
   screen.addstr(row+2, col, f'{wins2[0]:>4}')
   col += 10
   screen.addstr(row, col, f'{wins[2]:>4}')
   screen.addstr(row+1, col, f'{wins[1]:>4}')
   screen.addstr(row+2, col, f'{wins[0]:>4}')

   col = screen.board_offset_x + 10
   row += 4
   screen.addstr(row, col, f'{(wins[1] + wins2[2]):>4}')
   screen.addstr(row + 1, col, f'{(wins[2] + wins2[1]):>4}')
   screen.addstr(row + 2, col, f'{(wins[0] + wins2[0]):>4}')
   
   col += 25
   screen.addstr(row, col, f'{(wins[2] + wins2[1]):>4}')
   screen.addstr(row + 1, col, f'{(wins[1] + wins2[2]):>4}')
   screen.addstr(row + 2, col, f'{(wins[0] + wins2[0]):>4}')


def main(stdscr):
   global board
   global ai_speed
   screen = ConsoleScreen(stdscr)
   screen.set_header(header_display)
   player_files = load_player_files()     
   
   # Main Loop
   print("Calling main menu")
   screen.draw_menu(main_menu_options)
   
   selection = 'noop'

   while selection and selection.lower() != 'q':
      players = []
      selection = getch(['1', '2', '3', 'q'])

      if selection == '1':
         if len(player_files) < 1:
            screen.print_message("There are no AI's in the 'players' folder to play against. Press 'C' to continue.")
            _ = getch(['c'])
            screen.clear_message()
            continue
         
         screen.draw_menu(player_select_options)

         player_num = getch(['1','2', 'q'])
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
         if len(player_files) < 1:
            screen.print_message("There are no AI's in the 'players' folder to play against")
            continue
         
         screen.draw_menu(num_games_options)
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
                  screen.print_message("Cat's Game! No winner.")
               else:
                  screen.print_message(f"{get_printable_name(players[winner - 1])} as Player {winner}, is the Winner!", 13)
               screen.print_message("Press <R> for a rematch", 14)
               screen.print_message("Press <Q> to return to main menu", 15)
               pause = getch(['q', 'r'])
         elif sub_selection == '2':
            if len(player_files) < 1:
               screen.print_message("There are no AI's in the 'players' folder to play against")
               continue
            num_games = 500
            wins = [0, 0, 0]
            
            # Play two custom AI's against each other
            players.append(get_ai_selection(screen, player_files, 1))
            players.append(get_ai_selection(screen, player_files, 2))
            
            wins = play_many_games(screen, num_games, players)

            players2 = players[::-1]
            wins2 = [0, 0, 0]
            wins2 = play_many_games(screen, num_games, players2)
                        
            draw_many_games_results(screen, players, wins, wins2)
            screen.print_message("Press <Q> to return to the main menu", 7)
            pause = getch(['q'])
         elif sub_selection == '3' or sub_selection == '4':
            original_ai_speed = ai_speed
            ai_speed = 0
            if len(player_files) < 1:
               screen.print_message("There are no AI's in the 'players' folder to play against")
               continue
            num_games = 1000
            
            # Play two custom AI's against each other
            first_player = get_ai_selection(screen, player_files, 1)
            screen.print_message(f"Player 1: {get_printable_name(first_player)}")
            players.append(first_player)

            players.append(get_ai_selection(screen, player_files, 2))

            play_until_player_num_wins = 1
            if sub_selection == '4':
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

      if selection == '3': # Two Human Players
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

      elif selection == 'q':
         break
   
      screen.draw_menu(main_menu_options)

curses.wrapper(main)
