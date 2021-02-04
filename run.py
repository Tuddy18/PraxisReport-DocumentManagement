#!flask/bin/python
from app import app

SECRET_KEY = "\xf9'\xe4p(\xa9\x12\x1a!\x94\x8d\x1c\x99l\xc7\xb7e\xc7c\x86\x02MJ\xa0"
app.secret_key = SECRET_KEY

if __name__ == '__main__':
    app.run(host="0.0.0.0")
    # app.run()