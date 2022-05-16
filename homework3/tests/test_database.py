from mock import MagicMock

from app.database_class import Database, save_title


def test_database():
    my_db = Database()
    assert my_db.cnt == 0
    assert len(my_db.db) == 0


def test_save_title_good():
    my_title = "Hello, world!"
    db = Database()
    logger = MagicMock()
    logger.debug.return_value = None
    assert save_title(my_title, db, logger) is True
    assert db.cnt == 1


def test_save_title_bad():
    my_title = ""
    db = Database()
    logger = MagicMock()
    logger.debug.return_value = None
    assert save_title(my_title, db, logger) is False
    assert db.cnt == 0
