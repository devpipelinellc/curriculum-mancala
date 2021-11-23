from util import *
from time import sleep
import importlib

import curses

from console_screen import ConsoleScreen
from getch import getch
from screens import *
from MancalaBoard import *

ai_speed = 2

board = MancalaBoard()

def draw_main_board(screen):
   global board
   screen.clear_board()
   screen.draw_header()
   # screen.draw_template(row + 4, col, board_display)
   screen.draw_template(screen.board_offset_y + 3, screen.board_offset_x, board.get_string_list())
   
   # screen.draw_board_display()
   # Write Player names
   # player_2_name = 'Player 2: ' + get_printable_name(players[1])
   # screen.addstr(row + 10, col + 10, f'{get_printable_name(players[0])}')
   # screen.addstr(row + 20, col, f'{player_2_name:>53}')

   # draw_moves_list(screen)
   
   screen.refresh()

def draw_ai_selection(screen, player_files, player_num = 1):
   
   players = printable_players(player_files)
   options = [f"Select an A.I. to play Player {player_num} ?"]

   for i, name in enumerate(players):
      options.append(f'({i}) {name}')
   
   screen.draw_menu(options)

def get_ai_selection(screen, player_files, player_num = 1):
   # opp_num = 1 if player_num == '2' else '2'
   draw_ai_selection(screen, player_files, player_num)
   
   index = 'not set'
   while ((not index.isnumeric()) or (int(index) < 0 or int(index) > len(player_files))):
      index = getch(list(map(str, list(range(len(player_files))))))
   
   return player_files[int(index)]

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
   winner = ''
   turn = 1
   move_num = -1
   message = ''
   
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
      
      screen.print_message(f'Player {turn} selected {move_num}.')
      board.make_move(move_num)
      
   if print_board_during_play:
      draw_main_board(screen)
   board.collect()
   if print_board_during_play:
      draw_main_board(screen)
   return board.get_winner()

def main(stdscr):
   global board
   screen = ConsoleScreen(stdscr)
   screen.set_header(header_display)
   player_files = load_player_files()     
   
   # Main Loop
   print("Calling main menu")
   screen.draw_menu(main_menu_options)
   
   selection = 'noop'

   while selection and selection.lower() != 'q':
      players = []
      selection = getch(['1', '2', 'q'])

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
      #    elif sub_selection == '2':
      #       if len(player_files) < 1:
      #          print_message("There are no AI's in the 'players' folder to play against")
      #          continue
      #       num_games = 5000
      #       wins = [0, 0, 0]
            
      #       # Play two custom AI's against each other
      #       players.append(get_ai_selection(player_files, 'X'))
      #       # print_message(f"{get_printable_name(players[0])} will be 'X'")
      #       players.append(get_ai_selection(player_files, 'O'))
               
      #       play_many_games(num_games, players, wins)

      #       players2 = players[::-1]
      #       wins2 = [0, 0, 0]
            
      #       play_many_games(num_games, players2, wins2)
            
      #       draw_many_game_results()
      #       print_many_games_scores(players, wins, wins2)
      #       print_message("Press <Q> to return to the main menu", 4)
      #       pause = getch(['q'])
      #    elif sub_selection == '3' or sub_selection == '4':
      #       ai_speed = 0
      #       if len(player_files) < 1:
      #          print_message("There are no AI's in the 'players' folder to play against")
      #          continue
      #       num_games = 10000
            
      #       # Play two custom AI's against each other
      #       first_player = get_ai_selection(player_files, 'X')
      #       print_message(f"X: {get_printable_name(first_player)}")
      #       players.append(first_player)

      #       players.append(get_ai_selection(player_files, 'O'))

      #       play_until_letter_wins = 'X'
      #       if sub_selection == '4':
      #          play_until_letter_wins = 'O'
            
      #       while num_games > 0:
      #          winner = play_game(players)
      #          if winner >= 0 and symbols[winner] == play_until_letter_wins:
      #             print_message(f"{get_printable_name(players[winner])} as {symbols[winner]}, is the Winner!")
      #             break
      #          num_games -= 1
               
      #       if num_games == 0:
      #          print_message(f"{play_until_letter_wins} did not win any games!", 1)
            
      #       print_message("Press <Q> to return to the main menu", 4)
      #       pause = getch(['q'])
      #       ai_speed = .3

      elif selection == 'q':
         break
   
      screen.draw_menu(main_menu_options)

curses.wrapper(main)
