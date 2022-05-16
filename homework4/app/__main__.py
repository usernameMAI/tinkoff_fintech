from threading import Thread

from app.application import app
from app.databases import create_db
from app.update_crypto_costs import update_costs

if __name__ == '__main__':
    create_db()
    th = Thread(target=update_costs)
    th.start()
    app.run(debug=False)
