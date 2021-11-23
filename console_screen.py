import curses

class ConsoleScreen:
   def __init__(self, global_stdscr, board_offset_x = 1, board_offset_y = 1):
      self.stdscr = global_stdscr
      self.board_offset_x = board_offset_x
      self.board_offset_y = board_offset_y
      self.header_display = []
      curses.start_color()
      curses.use_default_colors()
      curses.noecho()
      curses.curs_set(False)
      for i in range(0, curses.COLORS):
         curses.init_pair(i + 1, i, -1)
      
   def set_header(self, header_display):
      self.header_display = header_display

   def clear_board(self):
      self.stdscr.clear()
      self.stdscr.refresh()

   def refresh(self):
      self.stdscr.refresh()

   def draw_template(self, row, col, template_rows, strip=False):
      for line in template_rows:
         if strip:
            line = line.strip()
         self.stdscr.addstr(row, col, line)
         row += 1
      self.stdscr.refresh()

   def draw_header(self):
      self.draw_template(self.board_offset_y, self.board_offset_x, self.header_display)

   def draw_menu(self, options):
      self.stdscr.clear()
      self.stdscr.refresh()
      self.stdscr.erase()
      self.draw_header()
      row = self.board_offset_y + 4
      col = self.board_offset_x + 3
      self.draw_template(row, col, options)
      self.stdscr.refresh()

   def print_message(self, message, row_offset = 0):
      row = self.board_offset_y + 11 + row_offset
      col = self.board_offset_x

      self.stdscr.move(row, col)
      self.stdscr.clrtoeol()
      self.stdscr.addstr(row, col, message)

      self.stdscr.refresh()
   
   def clear_message(self, row_offset = 0):
      self.print_message('', row_offset)

   def addstr(self, row, col, strng, refresh = True):
      self.stdscr.addstr(row, col, strng)
      if refresh:
         self.stdscr.refresh()
   
   def print_status_bar(self, val, total_val):
      row = self.board_offset_y + 16
      col = self.board_offset_x
      
      self.stdscr.move(row, col)
      self.stdscr.clrtoeol()

      number_of_boxes = 50
      val_boxes = int((val / total_val) * number_of_boxes)
      remainder = max(0, (number_of_boxes - val_boxes))
      val_box_str = ''
      if val_boxes > 1:
         val_box_str = '█' * val_boxes
      remainder_str = ''
      if remainder > 1:
         remainder_str = '░' * remainder
      self.stdscr.addstr(row, col, val_box_str + remainder_str)
      self.stdscr.refresh()