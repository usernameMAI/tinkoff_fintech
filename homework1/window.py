import curses


class Window:
    def __init__(self, screen, n: int, k: int):
        self.screen = screen
        self.n = n
        self.k = k

    def check_correct_terminal_size(self, need_height, need_width) -> bool:
        """
        Проверяет, можно ли разместить на экране screen надпись размером need_height и need_width.
        """
        screen_height, screen_width = self.screen.getmaxyx()
        if need_height > screen_height or need_width > screen_width:
            return False
        return True

    def check_correct_terminal_size_message(self) -> None:
        """
        Вывести на экран screen сообщение, что терминал слишком маленький.
        """
        self.screen.clear()
        self.screen.addstr("Make the terminal bigger")

    def draw_the_names_of_the_players(self, player1: str, player2: str) -> None:
        """
        Рисует прямоугольники, в которых располагаются имена игроков.
        """
        screen_height, screen_width = self.screen.getmaxyx()
        width_rectangle = 12
        height_rectangle = 3
        max_size_players_name = 10
        coord_y_first_player = (screen_height - height_rectangle) // 2
        coord_y_second_player = coord_y_first_player
        coord_x_first_player = 0
        coord_x_second_player = screen_width - width_rectangle - 1
        player1_win = curses.newwin(
            height_rectangle,
            width_rectangle + 1,
            coord_y_first_player,
            coord_x_first_player,
        )
        player2_win = curses.newwin(
            height_rectangle,
            width_rectangle + 1,
            coord_y_second_player,
            coord_x_second_player,
        )
        # Имя игроков располагается в прямоугольниках так, чтобы количество пробелов
        # слева и справа от имен было одинаково
        name_rectangle1 = (
            "~" * width_rectangle
            + "\n"
            + "~"
            + " " * ((max_size_players_name - len(player1)) // 2)
            + player1
            + " " * (max_size_players_name // 2 - len(player1) // 2)
            + "~\n"
            + "~" * width_rectangle
        )
        name_rectangle2 = (
            "~" * width_rectangle
            + "\n"
            + "~"
            + " " * ((max_size_players_name - len(player2)) // 2)
            + player2
            + " " * (max_size_players_name // 2 - len(player2) // 2)
            + "~\n"
            + "~" * width_rectangle
        )
        player1_win.addstr(name_rectangle1)
        player2_win.addstr(name_rectangle2)
        player1_win.refresh()
        player2_win.refresh()

    def draw_ships_left(self, field1, field2) -> None:
        """
        Рисует сколько осталось кораблей у игроков
        """
        str_player1_ships = "Remaining ships for the left player: ( "
        for i in range(4):
            str_player1_ships = str_player1_ships + str(field1.count_ships[i]) + " "
        str_player1_ships += ")"
        str_player2_ships = "Remaining ships for the right player: ( "
        for i in range(4):
            str_player2_ships = str_player2_ships + str(field2.count_ships[i]) + " "
        str_player2_ships += ")"
        self.screen.addstr(0, 35, str_player1_ships)
        self.screen.addstr(1, 35, str_player2_ships)

    def draw_saves(self):
        str_saves = "Press 1 or 2 to save the current game to the corresponding slot."
        x_save_on_screen = 35
        y_save_on_screen = 5
        self.screen.addstr(y_save_on_screen, x_save_on_screen, str_saves)
        self.screen.refresh()

    def draw_instructions(self, instructions: str) -> None:
        self.screen.addstr(instructions)
        self.screen.refresh()

    def draw_battlefields(self, battlefield_player1, battlefield_player2, y, x) -> None:
        """
        Рисует 2 поля для морского боя. Также рисует курсор, куда хочет выстрелить Player1.
        """
        screen_height, screen_width = self.screen.getmaxyx()
        left_x = 20
        left_y = screen_height // 2 - battlefield_player2.n // 2
        battlefield1_win = curses.newwin(
            battlefield_player2.n + 2, battlefield_player2.k + 2, left_y, left_x
        )
        for i in range(battlefield_player1.n):
            string = ""
            for el in battlefield_player1.battlefield[i]:
                if el == 0:
                    string += "."
                else:
                    string += str(el)
            battlefield1_win.addstr(string + "\n")
        battlefield1_win.refresh()

        left_x = screen_width // 2 + 10
        battlefield2_win = curses.newwin(
            battlefield_player2.n + 2, battlefield_player2.k + 2, left_y, left_x
        )
        for line in battlefield_player2.battlefield_hide:
            for i in line:
                battlefield2_win.addstr(i)
            battlefield2_win.addstr("\n")
        battlefield2_win.addstr(y, x, "#")
        battlefield2_win.refresh()
