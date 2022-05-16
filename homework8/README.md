# News Service

### Description:
REST API сервис, где пользователи могут добавлять, оценивать,
смотреть и комментировать новости.

####  Бизнес-Логика:

Через API можно заводить новых пользователей. Пользователи делятся
на клиентов и администраторов. 

Сущности:
1. Пост
2. Комментарий к посту
3. Оценку посту (лайк или дизлайк)
4. Пользователь (администратор или клиент)

Администратора можно добавить через файл admin, написав туда
`login` и `password`. Также администратор может выдать роль
администратора другому пользователю.

Любой пользователь может создать свой пост, написать комментарий
или поставить лайк к существующему посту. Клиент может удалить
только свой пост, либо комментарий. Администратор может удалить
любой пост и любой комментарий. Для любого запроса к посту
присутствует пагинация.

В базе данных хранятся не пароли, а только хеши от них.

Пост состоит из заголовка, текста и фотографии.

Можно запрашивать посты по:
- post_id - отдельный пост
- user_id - все посты отдельного пользователя
- все посты, которые были созданы в течение дня

Технические особенности:
1. API сервис на `FastAPI`.
2. СУБД `SQLite`, взаимодействие через `sqlalchemy`.
3. Аутентификация через `OAuth2`.


### Create venv:
    make venv

### Run tests:
    make test

### Run linters:
    make lint

### Run formatters:
    make format

### Run init db:
    make init

### Run program:
    make up

### Run program with docker:
    make up-docker