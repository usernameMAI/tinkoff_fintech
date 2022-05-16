import logging
from http import HTTPStatus

import werkzeug.wrappers.response
from flask import Flask, Response, redirect, render_template, request, url_for

from app.database_class import Database, save_title

logging.basicConfig(level=logging.DEBUG, filename="logs.log", filemode="w")
my_logger = logging.getLogger(__name__)


def create_app() -> Flask:
    """
    Функция создаёт и возвращает объект Flask.
    """
    return Flask(__name__)


app = create_app()
my_db = Database()


@app.route("/")
def to_do() -> str:
    """
    Стартовая страница. Возвращает html код,
    указанный в шаблоне app.html.
    """
    return render_template(
        "todo.html", todo_list=my_db, show_finished=True, show_not_finished=True
    )


@app.route("/add", methods=["POST"])
def add() -> werkzeug.wrappers.response.Response:
    """
    Функция вызывается, когда клиент нажал
    на кнопку add. Сохраняет заголовок в словарь.
    Перенаправляет на стартовую страницу.
    """
    title = request.form.get("title")
    save_title(str(title), my_db, my_logger)
    return redirect(url_for("to_do"))


@app.route("/update/<int:todo_id>", methods=["POST"])
def update(todo_id: int) -> werkzeug.wrappers.response.Response:
    """
    Функция вызывается, когда клиент нажал
    на кнопку update. Изменяет статус завершенности
    у задачи с номером "todo_id".
    Перенаправляет на стартовую страницу.
    """
    # если задача с номером 'todo_id' существует
    cnt = my_db.cnt
    if cnt >= todo_id >= 1:
        my_db.db[todo_id].complete = not my_db.db[todo_id].complete
        my_logger.debug(
            "The relevance of the case %d has been changed" " to %r.",
            todo_id,
            my_db.db[todo_id].complete,
        )
        return redirect(url_for("to_do"))
    return Response(status=HTTPStatus.NOT_FOUND)


@app.route("/completed")
def completed() -> str:
    """
    Страница с завершенными задачами. Возвращает html код,
    указанный в шаблоне app.html.
    """
    return render_template(
        "todo.html", todo_list=my_db, show_finished=True, show_not_finished=False
    )


@app.route("/active")
def active() -> str:
    """
    Страница с активными задачами. Возвращает html код,
    указанный в шаблоне app.html.
    """
    return render_template(
        "todo.html", todo_list=my_db, show_finished=False, show_not_finished=True
    )
