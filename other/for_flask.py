from flask import Flask,request
# """простейший сервер"""
app = Flask(__name__)

@app.route('/hello/<kek>',methods=['POST','GET']) # запускаем и в браузере вводим http://127.0.0.1:5000//hello/kek
def hello_world(kek): #и увидим то, что возвращает функция
    data = request.json
    print(data)
    print(type(data))
    return kek
if __name__ == "__main__":
    app.run()

