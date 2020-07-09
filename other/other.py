import re
# from flask import Flask
# """простейший сервер"""
# app = Flask(__name__)
#
# @app.route('/hello/kek') # запускаем и в браузере вводим http://127.0.0.1:5000//hello/kek
# def hello_world():       # и увидим то, что возвращает функция
#     return 'salamaleikum'
# if __name__ == "__main__":
#     app.run()



string1 = 'fdfd4/4hAAk2.4khk468'
new = re.sub(r'[^a-z,A-Z]+', r'', string1)
print(new)

string2 = '685444512dfa12'
new2 = re.sub(r'[^a-z,A-Z]+', r'', string2)
if not new2.isalpha():
    raise ValueError
else:print(new2)

kek = 'пизда'
if kek.isalpha():
    print('путин')