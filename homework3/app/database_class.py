from logging import Logger

from app.todo_class import Todo


class Database:
    """
    Класс 'моя' база данных для 'Todo'.
    Реализована через словарь.
    Содержит счётчик 'cnt', который нужен
    для определения 'id' добавляемого элемента.
    """

    def __init__(self) -> None:
        self.db: dict[int, Todo] = {}
        self.cnt = 0


def save_title(title: str, my_db: Database, my_logger: Logger) -> bool:
    """
    Функция сохраняет заголовок в словарь.
    Если заголовок пустой или состоит из пустых символов,
    то сохранение не происходит, и функция возвращает False.
    Если сохранить получилось, то возвращается True.
    """
    cnt = my_db.cnt
    if title and not title.isspace():
        new_todo = Todo(title, False)
        cnt += 1
        my_db.cnt += 1
        my_db.db[cnt] = new_todo
        my_logger.debug(f"Added element {new_todo.title} with number {cnt}.")
        return True
    return False
