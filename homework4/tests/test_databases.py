from app.databases import Cryptocurrency, OperationsHistory, PortfolioItem, User


def test_user():
    user = User(id=1, name="Hello, world", money=1234)
    assert user.id == 1
    assert user.name == "Hello, world"
    assert user.money == 1234


def test_storage():
    storage = PortfolioItem(id=1, name_user="USER", name_crypto="CRYPTO", count=10000)
    assert storage.id == 1
    assert storage.name_user == "USER"
    assert storage.name_crypto == "CRYPTO"
    assert storage.count == 10000


def test_cryptocurrency():
    cryptocurrency = Cryptocurrency(id=1, name="CRYPTO", price="1000")
    assert cryptocurrency.id == 1
    assert cryptocurrency.name == "CRYPTO"
    assert cryptocurrency.price == "1000"


def test_operations_history():
    operations_history = OperationsHistory(
        id=1, name_user="USER", name_crypto="CRYPTO", cost="1", operation=True
    )
    assert operations_history.id == 1
    assert operations_history.name_user == "USER"
    assert operations_history.cost == "1"
    assert operations_history.name_crypto == "CRYPTO"
    assert operations_history.operation is True
