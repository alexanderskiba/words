from flask import Flask
"""простейший сервер"""
app = Flask(__name__)

@app.route('/hello/kek') # запускаем и в браузере вводим http://127.0.0.1:5000//hello/kek
def hello_world():       # и увидим то, что возвращает функция
    return 'salamaleikum'
if __name__ == "__main__":
    app.run()
