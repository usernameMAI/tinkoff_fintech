from app.todo_class import Todo


def test_class():
    title = "Hello, world"
    complete = False
    todo = Todo(title, complete)
    assert todo.title == title
    assert todo.complete == complete
