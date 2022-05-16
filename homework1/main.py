import typer
import window
import battlefield
import pickle
from curses import wrapper

PLAYER_NAME_1 = "Player 1"
PLAYER_NAME_2 = "Player 2"


def get_player_name(player_num: int) -> str:
    """
    Возвращает введённое имя пользователя с номером player_num.
    Максимальный размер имени -- 10 символов.
    Если ничего не вводится (пустая строка), то имя будет 'Player [player_num]'.
    """
    input_message = f"Please enter a name for player {player_num}: "
    name = input(input_message)
    max_name_len = 10
    while len(name) > max_name_len:
        name = input("Please enter a name with 15 or less characters:  ")
    return name


def get_instructions_for_main_menu(game_started) -> str:
    """
    :return: строка, которая является инструкцией для пользователя в главном меню.
    """
    welcome_str = (
        "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
        "~                                   ~\n"
        "~      WELCOME TO BATTLESHIP        ~\n"
        "~                                   ~\n"
        "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
    )
    if not game_started:
        new_game_str = "Press p to play a new game.\n"
    else:
        new_game_str = "Press p to continue the game.\n"
    load_save_str = "Press s to load save.\n"
    quit_the_game_str = "Press q to quit."
    return welcome_str + new_game_str + load_save_str + quit_the_game_str


def get_instructions_for_battleship() -> str:
    game_str = "This is battleship...\n\n"
    shot_str = "Press p to shot.\n"
    save_str = "Press l to save.\n"
    quit_str = "Press q to exit the main menu.\n"
    move_str = "Press WASD to navigate."
    return game_str + shot_str + save_str + quit_str + move_str


def go_to_correct_size_menu(screen) -> None:
    """
    Выводит на экран информацию о том, что введённый размер полей для морского боя некорректен.
    """
    instructions = "Please enter a valid field size"
    screen_height, screen_width = screen.getmaxyx()
    y_instructions = screen_height // 2
    x_instructions = screen_width // 2 - len(instructions) // 2
    screen.clear()
    screen.addstr(y_instructions, x_instructions, instructions)
    screen.getch()


def go_to_save_menu(
    screen,
) -> (battlefield.Battlefield, battlefield.Battlefield, str, str):
    """
    Перейти в меню сохранений. Можно выбрать 1 или 2 сохранение.
    Если сохранений нет, то можно вернуться в главное меню и начать новую игру.
    Если сохранение выбрано, то при запуске следующей игры оно будет запущено.
    """
    save_menu = window.Window(screen, 0, 0)
    screen.clear()
    instructions = "Select save 1 or 2, or press q to exit: "
    screen.addstr(instructions)
    while True:
        if not save_menu.check_correct_terminal_size(1, len(instructions) + 1):
            save_menu.check_correct_terminal_size_message()
            key = screen.getch()
            if key == ord("q"):
                break
        else:
            key = screen.getch()
            if key == ord("1"):
                file_name = "save1"
            elif key == ord("2"):
                file_name = "save2"
            elif key == ord("q"):
                break
            else:
                continue
            try:
                with open(file_name, mode="rb") as file_handler:
                    load = pickle.load(file_handler)
                    return load
            except FileNotFoundError:
                screen.addstr(2, 0, f"{file_name} does not exist")
                continue


def go_to_win_menu(screen, player_name) -> None:
    """
    Выводит на экран информацию о том, что игрок с именем player_name победил.
    """
    screen.clear()
    screen_height, screen_width = screen.getmaxyx()
    # расстояние, на которое надпись победы будет смещена влево от середины экрана
    some_x = 5
    win_str = f"{player_name} win! "
    win_menu_coord_y = screen_height // 2
    win_menu_coord_x = screen_width // 2 - some_x
    screen.addstr(win_menu_coord_y, win_menu_coord_x, win_str)
    screen.getch()


def pressed_1_or_2_file(key: int) -> (bool, str):
    """
    Функция проверяет, выбрал ли пользователь файл для загрузки сохранения.
    Если да, то возвращает имя файла, которое он выбрал, а также значение типа bool,
    означающее, что название файла получено.
    """
    flag = False
    file_name = None
    if key == ord("1"):
        file_name = "save1"
        flag = True
    elif key == ord("2"):
        file_name = "save2"
        flag = True
    return flag, file_name


def move_cursor(current_y: int, current_x: int, key: int, n: int, k: int) -> (int, int):
    """
    Функция изменяет координаты курсора.
    """
    if key == ord("d"):
        current_x = min(k - 1, current_x + 1)
    elif key == ord("a"):
        current_x = max(0, current_x - 1)
    elif key == ord("s"):
        current_y = min(n - 1, current_y + 1)
    elif key == ord("w"):
        current_y = max(0, current_y - 1)
    return current_y, current_x


def load_save(file_name: str, battlefield_player1, battlefield_player2) -> None:
    """
    Сохраняет два боевых поля с кораблями и имена игроков в файл.
    """
    with open(file_name, mode="wb") as file_handler:
        pickle.dump(
            (
                battlefield_player1,
                battlefield_player2,
                PLAYER_NAME_1,
                PLAYER_NAME_2,
            ),
            file_handler,
        )


def try_to_shot(
    screen, battlefield_player1, battlefield_player2, current_y: int, current_x: int
) -> bool:
    """
    Функция пытается сделать выстрел первым игроком в точку (current_y, current_x).
    Если это получилось, то выстрел делает и второй игрок.
    Возвращает True, если один из игроков закончил игру.
    """
    shot = battlefield_player1.make_a_shot(current_y, current_x, battlefield_player2)
    if shot:
        if battlefield_player2.check_defeat():
            go_to_win_menu(screen, PLAYER_NAME_1)
            return True
        battlefield_player2.make_a_bot_shot(battlefield_player1)
        if battlefield_player1.check_defeat():
            go_to_win_menu(screen, PLAYER_NAME_2)
            return True
    return False


def go_to_play_battleship(
    screen, n, k, load, battlefield_player1, battlefield_player2
) -> bool:
    """
    Симуляция игры в морской бой.
    Чтобы выйти, нужно нажать q.
    Возвращает True, если все корабли одного из игроков полностью уничтожены.
    """
    # Если есть сохранение
    if load:
        n = load[0].n
        k = load[0].k
    instructions = get_instructions_for_battleship()
    # Размеры инструкций для игрового меню
    instructions_height = 8
    instructions_width = 90
    play_field = window.Window(screen, n, k)
    if load:
        battlefield_player1 = load[0]
        battlefield_player2 = load[1]
    # current_x и current_y отвечают за то, где Player1 находится на поле другого игрока.
    current_x = 0
    current_y = 0
    saves = False
    key = None
    while True:
        if not play_field.check_correct_terminal_size(
            instructions_height * 2 + n, instructions_width
        ):
            play_field.check_correct_terminal_size_message()
            key = screen.getch()
            # Если игрок не может или не хочет расширить терминал, то он может выйти с помощью кнопки 'q'.
            if key == ord("q"):
                return False
        else:
            screen.clear()
            screen.refresh()
            play_field.draw_battlefields(
                battlefield_player1, battlefield_player2, current_y, current_x
            )
            # Если загружено сохранение, то загружаем имена игроков из сохранения
            if load:
                play_field.draw_the_names_of_the_players(load[2], load[3])
            else:
                play_field.draw_the_names_of_the_players(PLAYER_NAME_1, PLAYER_NAME_2)
            play_field.draw_instructions(instructions)
            play_field.draw_ships_left(battlefield_player1, battlefield_player2)
            if not saves:
                key = screen.getch()
            if saves:
                play_field.draw_saves()
                key = screen.getch()
                # Флаг отвечает за то, нажал ли пользователь кнопку 1 или 2
                flag, file_name = pressed_1_or_2_file(key)
                if flag:
                    load_save(file_name, battlefield_player1, battlefield_player2)
            if key == ord("q"):
                return False
            # Возможность сохраниться
            elif key == ord("l"):
                # Убрать меню сохранений с экрана или наоборот -- добавить
                saves = not saves
            elif key in [ord("w"), ord("a"), ord("s"), ord("d")]:
                current_y, current_x = move_cursor(current_y, current_x, key, n, k)
            elif key == ord("p"):
                shot = try_to_shot(
                    screen,
                    battlefield_player1,
                    battlefield_player2,
                    current_y,
                    current_x,
                )
                if shot:
                    return True


def go_to_player_menu(screen, n: int, k: int) -> None:
    """Меню игры, из которого можно загрузить сохранение или начать новую игру."""
    battlefield_player1 = battlefield.Battlefield(n, k)
    battlefield_player2 = battlefield.Battlefield(n, k)
    game_started = False
    main_menu = window.Window(screen, n, k)
    load = None
    # Размеры инструкций для главного меню
    instructions_height = 8
    instructions_width = 38
    while True:
        if not main_menu.check_correct_terminal_size(
            instructions_height, instructions_width
        ):
            main_menu.check_correct_terminal_size_message()
            key = screen.getch()
            # Если игрок не может или не хочет расширить терминал, то он может выйти с помощью кнопки 'q'.
            if key == ord("q"):
                break
        else:
            screen.clear()
            instructions = get_instructions_for_main_menu(game_started)
            main_menu.draw_instructions(instructions)
            key = screen.getch()
            if key == ord("p"):
                # Начать новую игру
                game_started = True
                if battlefield_player1.check_the_size_of_the_field():
                    end = go_to_play_battleship(
                        screen, n, k, load, battlefield_player1, battlefield_player2
                    )
                    if end:
                        break
                else:
                    go_to_correct_size_menu(screen)
            elif key == ord("s"):
                # Загрузить сохранение
                load = go_to_save_menu(screen)
                # Если вышел из меню сохранений, но не загрузил сохранение
                if load is None:
                    continue
                else:
                    battlefield_player1 = load[0]
                    battlefield_player2 = load[1]
                    n = battlefield_player1.n
                    k = battlefield_player1.k
            elif key == ord("q"):
                # Выйти из игры
                break


def main(n: int, k: int) -> None:
    print("Let's play battleship...")
    # Ask for user to input names
    global PLAYER_NAME_1
    PLAYER_NAME_1 = get_player_name(1) or "Player1"
    global PLAYER_NAME_2
    PLAYER_NAME_2 = get_player_name(2) or "Player2"
    wrapper(go_to_player_menu, n, k)


if __name__ == "__main__":
    typer.run(main)
