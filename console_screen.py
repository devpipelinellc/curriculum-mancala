import ansi_lib


class ConsoleScreen:
    def __init__(self, board_offset_x=1, board_offset_y=1):

        self.board_offset_x = board_offset_x
        self.board_offset_y = board_offset_y
        self.header_display = []
        ansi_lib.reset()

    def set_header(self, header_display):
        self.header_display = header_display

    def clear_board(self):
        ansi_lib.clear()

    def hide_cursor(self):
        ansi_lib.hide_cursor()

    def show_cursor(self):
        ansi_lib.show_cursor()

    def reset(self):
        ansi_lib.reset()

    def clear(self):
        ansi_lib.clear()
        ansi_lib.reset()
        ansi_lib.goto(self.board_offset_y, self.board_offset_x)

#    def refresh(self):

    def draw_template(self, row, col, template_rows, variables=[], strip=False):
        var_idx = 0
        for line in template_rows:
            if strip:
                line = line.strip()
            if '%%' in line:
                line = line.replace('%%', str(variables[var_idx]))
                var_idx += 1
            ansi_lib.addstr(row, col, line)
            row += 1
        # ansi_lib.refresh()

    def draw_header(self):
        self.draw_template(self.board_offset_y, self.board_offset_x, self.header_display)

    def draw_menu(self, template_rows, variables=[]):
        ansi_lib.clear()
        ansi_lib.reset()
        self.draw_header()
        row = self.board_offset_y + 4
        col = self.board_offset_x + 3
        self.draw_template(row, col, template_rows, variables)

    def print_message(self, message, row_offset=0):
        row = self.board_offset_y + 11 + row_offset
        col = self.board_offset_x

        ansi_lib.goto(row, col)
        ansi_lib.addstr(row, col, message)

    def clear_message(self, row_offset=0):
        self.print_message('', row_offset)

    def addstr(self, row, col, strng, refresh=True):
        ansi_lib.addstr(row, col, strng)
        # if refresh:
        #     self.stdscr.refresh()

    def print_status_bar(self, val, total_val, row_offset=16):
        row = self.board_offset_y + row_offset
        col = self.board_offset_x

        ansi_lib.goto(row, col)
      #   self.stdscr.clrtoeol()

        number_of_boxes = 50
        val_boxes = int((val / total_val) * number_of_boxes)
        remainder = max(0, (number_of_boxes - val_boxes))
        val_box_str = ''
        if val_boxes > 1:
            val_box_str = '█' * val_boxes
        remainder_str = ''
        if remainder > 1:
            remainder_str = '░' * remainder
        ansi_lib.addstr(row, col, val_box_str + remainder_str)
        # self.stdscr.refresh()
