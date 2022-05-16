class Todo:
    """
    Класс задача "app".
    Содержит поля заголовка и завершенности задачи.
    """

    def __init__(self, title: str, complete: bool) -> None:
        self.title = title
        self.complete = complete
