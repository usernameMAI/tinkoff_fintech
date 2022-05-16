from random import randint

HORIZONTAL = 1
VERTICAL = 2


def count_the_number_of_ships(n: int, k: int) -> list:
    """
    Считает количество кораблей размером 1, 2, 3, 4 исходя от размера поля.
    Стандартные размеры поля 10 x 10, его площадь 100 и количество кораблей -- (1×4 + 2×3 + 3×2 + 4×1).
    Исходя из пропорций, для поля n x k, площадью square, количество кораблей:
        4 -- square // 100
        3 -- square * 2 // 100
        2 -- square * 3 // 100
        1 -- square * 4 // 100
    """
    count_ships = [0, 0, 0, 0]
    square = n * k
    for i in range(4):
        count_ships[3 - i] = square * (i + 1) // 100
    return count_ships


def nothing_around(field, y, x) -> bool:
    """
    Функция проверяет, можно ли установить на клетке поля field[y][x] корабль.
    Возвращает True, если рядом по горизонтали и вертикали не заняты клетки.
    """
    if x > 0 and field[y][x - 1] != 0:
        return False
    if y > 0 and field[y - 1][x] != 0:
        return False
    if x < len(field[0]) - 1 and field[y][x + 1] != 0:
        return False
    if y < len(field) - 1 and field[y + 1][x] != 0:
        return False
    return True


def find_position(size: int, direction: int, field, n, k) -> (int, int, bool):
    """
    Ищет куда можно поставить корабль размера size на поле field. Возвращает координаты найденной точки.
    """
    min_x = 0
    min_y = 0
    max_x = k - 1
    max_y = n - 1
    attempts = 0
    # Случайное большое число, за которое уже должна было быть найдена координата.
    max_attempts = 10e5
    if direction == VERTICAL:
        max_y -= size
    if direction == HORIZONTAL:
        max_x -= size
    while True:
        attempts += 1
        x = randint(min_x, max_x)
        y = randint(min_y, max_y)
        flag = True
        # Если в (y, x) уже стоит корабль, то нужно сгенерировать новую точку (y, x) и проверить её
        if field[y][x] != 0:
            continue
        # Проверяется, можно ли поставить корабль в вертикальном или горизонтальном направление
        if direction == VERTICAL:
            for free_space in range(y, y + size + 1):
                if field[free_space][x] != 0 or not nothing_around(
                    field, free_space, x
                ):
                    flag = False
        if direction == HORIZONTAL:
            for free_space in range(x, x + size + 1):
                if field[y][free_space] != 0 or not nothing_around(
                    field, y, free_space
                ):
                    flag = False
        if flag:
            return x, y, True
        # Если не получается найти позицию, то стоит попытаться сменить ориентацию корабля
        if attempts > max_attempts:
            return 0, 0, False


def generate_a_field(n: int, k: int, ships: list) -> list:
    """
    Генерирует расстановку кораблей на поле n x k.
    :param n: Высота поля.
    :param k: Ширина поля.
    :param ships: Список с количеством кораблей.
    """
    field = [[0] * k for _ in range(n)]
    for i in range(4):
        for ship in range(ships[i]):
            oriented = randint(HORIZONTAL, VERTICAL)
            while True:
                x, y, find = find_position(i, oriented, field, n, k)
                if find:
                    break
                else:
                    # Меняем ориентацию корабля на противоположную. Используется 3, так как
                    # 3 - HORIZONTAL = VERTICAL, 3 - VERTICAL = HORIZONTAL
                    oriented = 3 - oriented
            for j in range(i + 1):
                if oriented == HORIZONTAL:
                    field[y][x + j] = i + 1
                elif oriented == VERTICAL:
                    field[y + j][x] = i + 1
    return field


class Battlefield:
    MIN_HEIGHT = 5
    MAX_HEIGHT = 30
    MIN_WIDTH = 5
    MAX_WIDTH = 30

    def __init__(self, n: int, k: int):
        """
        :param n: Высота поля.
        :param k: Ширина поля.
        """
        self.n = n
        self.k = k
        self.battlefield_hide = [["."] * k for _ in range(n)]
        self.count_ships = count_the_number_of_ships(n, k)
        self.battlefield = generate_a_field(n, k, self.count_ships)

    def check_the_size_of_the_field(self) -> bool:
        """
        Проверить, является ли поле допустимого размера.
        """
        if (
            self.n > self.MAX_HEIGHT
            or self.n < self.MIN_HEIGHT
            or self.k > self.MAX_WIDTH
            or self.k < self.MIN_HEIGHT
        ):
            return False
        return True

    def check_defeat(self):
        """
        Проверить, закончились ли корабли у морского поля.
        """
        for count in self.count_ships:
            if count != 0:
                return False
        return True

    @staticmethod
    def check_current_position(
        battlefield, check_y_up, check_y_down, check_x_right, check_x_left, x, y
    ):
        go_up = go_down = go_right = go_left = True
        if battlefield[check_y_up][x] in ["*", 0] or check_y_up == y:
            go_up = False
        if battlefield[check_y_down][x] in ["*", 0] or check_y_down == y:
            go_down = False
        if battlefield[y][check_x_right] in ["*", 0] or check_x_right == x:
            go_right = False
        if battlefield[y][check_x_left] in ["*", 0] or check_x_left == x:
            go_left = False
        return go_up, go_down, go_right, go_left

    def check_destroy(self, y, x):
        """
        Проверить, уничтожен ли корабль на поле с координатой (y, x)
        """
        destroy = True
        size_of_ship = 1
        numbers_ships = [1, 2, 3, 4]
        # вниз, вверх, влево, вправо
        need_to_go = [True, True, True, True]
        for i in range(3):
            check_y1 = min(y + 1 + i, self.n - 1)
            check_y2 = max(y - 1 - i, 0)
            check_x1 = max(x - 1 - i, 0)
            check_x2 = min(x + 1 + i, self.k - 1)
            coordinates = [(x, check_y1), (x, check_y2), (check_x1, y), (check_x2, y)]
            for j, (check_x, check_y) in enumerate(coordinates):
                if need_to_go[j]:
                    if (
                        self.battlefield[check_y][check_x] in ["*", 0]
                        or (j < 2 and check_y == y)
                        or (j >= 2 and check_x == x)
                    ):
                        need_to_go[j] = False
                        continue
                    if self.battlefield[check_y][check_x] in ["X", "d"]:
                        size_of_ship += 1
                    if self.battlefield[check_y][check_x] in numbers_ships:
                        destroy = False
                    if j == 0 and check_y == self.n - 1:
                        need_to_go[j] = False
                    if j == 1 and check_y == 0:
                        need_to_go[j] = False
                    if j == 2 and check_x == 0:
                        need_to_go[j] = False
                    if j == 3 and check_x == self.k - 1:
                        need_to_go[j] = False
        return destroy, size_of_ship

    @staticmethod
    def signify_destruction(y, x, field) -> None:
        """
        Функция помечает, что корабль уничтожен в координате (y, x).
        """
        # вниз, вверх, влево, вправо
        need_to_go = [True, True, True, True]
        for i in range(0, 4):
            check_y1 = max(0, y - i)
            check_y2 = min(y + i, field.n - 1)
            check_x1 = max(0, x - i)
            check_x2 = min(x + i, field.k - 1)
            coordinates = [(check_x1, y), (x, check_y1), (check_x2, y), (x, check_y2)]
            for j, (check_x, check_y) in enumerate(coordinates):
                if need_to_go[j]:
                    if field.battlefield[check_y][check_x] == "d":
                        continue
                    if field.battlefield[check_y][check_x] == "X":
                        field.battlefield[check_y][check_x] = field.battlefield_hide[
                            check_y
                        ][check_x] = "d"
                        # Закрашиваем вокруг корабля
                        x_left = min(check_x + 1, field.k - 1)
                        x_right = max(check_x - 1, 0)
                        y_up = min(check_y + 1, field.n - 1)
                        y_down = max(check_y - 1, 0)
                        check_positions_to_paint = [
                            (y_up, check_x),
                            (y_down, check_x),
                            (check_y, x_left),
                            (check_y, x_right),
                        ]
                        for (
                            paint_coordinate_y,
                            paint_coordinate_x,
                        ) in check_positions_to_paint:
                            if field.battlefield[paint_coordinate_y][
                                paint_coordinate_x
                            ] not in ["X", "d"]:
                                field.battlefield[paint_coordinate_y][
                                    paint_coordinate_x
                                ] = field.battlefield_hide[paint_coordinate_y][
                                    paint_coordinate_x
                                ] = "*"
                    else:
                        need_to_go[j] = False

    def make_a_shot(self, y, x, field) -> bool:
        """
        Сделать выстрел в точку (y, x).
        Возвращает True, если удалось сделать выстрел.
        """
        if field.battlefield[y][x] in ["X", "*", "d"]:
            return False
        if field.battlefield[y][x] == 0:
            field.battlefield_hide[y][x] = "*"
            field.battlefield[y][x] = "*"
            return True
        elif field.battlefield[y][x] in [1, 2, 3, 4]:
            field.battlefield[y][x] = "X"
            field.battlefield_hide[y][x] = "X"
        destroy, size_destroy = field.check_destroy(y, x)
        if destroy:
            self.signify_destruction(y, x, field)
            field.count_ships[size_destroy - 1] -= 1
        return True

    def make_a_bot_shot(self, field) -> None:
        """
        Выстрел бота (Player 2).
        Выстрел происходил в случайную точку на поле, в которую ещё не стреляли.
        """
        while True:
            x = randint(0, field.k - 1)
            y = randint(0, field.n - 1)
            if field.battlefield[y][x] in [0, 1, 2, 3, 4]:
                self.make_a_shot(y, x, field)
                break
