from functools import wraps
from flask import Flask, request
from scripts.logic.utilities import Server, Deck, ClientError, WrapperDB


app = Flask(__name__)


def authentication(func):
    @wraps(func)
    def wrapper(user_name):
        login = user_name
        password = request.headers['Password']
        # user_serv = Server(login, password)
        
        if Server.is_authentication(login, password):
            return func(user_name)
        return {"status": "AuthenticationError"}
    return wrapper


@app.route('/Server/registration/<user_name>', methods=['POST','GET'])
def registration(user_name):
    login = user_name
    password = request.headers['Password']
    try:
        WrapperDB().registrationDB(login, password)
    except ClientError:
        return {'status': False, 'info': 'this login already exists'}
    return {'status': True, 'info': f'create user with login {login}'}


@app.route('/Server/create_card/<user_name>', methods=['POST','GET'])
@authentication
def create_card(user_name):
    print('Создаем карточку')
  
    data = request.json #принимаем словарь от клиента
    user_serv = Server(user_name)
    for key, item in data.items():
        word = key
        translate = item
        user_serv.create_card(word,translate)
    return {"status": True}



@app.route('/Server/update_card/<user_name>', methods=['POST','GET'])
@authentication
def update_card(user_name):
    data = request.json
    user_serv = Server(user_name)

    for key, item in data.items():
        word = key
        new_word = item[0]
        translate = item[1]
        answer = user_serv.update_card(word, new_word, translate)
    return {"status":answer }


@app.route('/Server/delete_card/<user_name>', methods=['POST','GET'])
@authentication
def delete_card(user_name):
    data = request.json
    user_serv = Server(user_name)

    for key in data:
        card_name = key
    answer = user_serv.delete_card(card_name)
    return {"status":answer,
            "delete card": card_name}


@app.route('/Server/receive_card/<user_name>', methods=['POST','GET'])
@authentication
def receive_card(user_name):
    data = request.json
    user_serv = Server(user_name)

    for key, item in data.items():
        word = key
    card = user_serv.receive_card(word)
    if not card:
        card_dict = {word: 'not exists'}
        answer = False
        return {"status": answer, "info": card_dict}
    else:
        card_dict = {'word': card[0], 'translate': card[1]}
        answer = True
        return {"status": answer, "info": card_dict}


@app.route('/Server/receive_all_cards/<user_name>', methods=['POST','GET'])
@authentication
def receive_all_cards(user_name):
    rec_dict = {}
    card_list = []
    rec_dict["status"] = True
    rec_dict["cards"] = card_list
    user_serv = Server(user_name)

    for i in user_serv.receive_all_cards():
        card_list.append({i.word:i.translate})
    return rec_dict


@app.route('/Server/create_deck/<user_name>', methods=['POST','GET'])
@authentication
def create_deck(user_name):
    data = request.json  # принимаем словарь от клиента
    user_serv = Server(user_name)

    for key, value in data.items():
        deck_name = key
        cards = value
        # print(cards)
    user_serv.create_deck(deck_name, cards)
    return {'status': True, 'create deck': deck_name}


@app.route('/Server/receive_deck/<user_name>', methods=['POST','GET'])
@authentication
def receive_deck(user_name):
    data = request.json
    user_serv = Server(user_name)

    for key in data:
        deck_name = key
    answer = user_serv.receive_deck(deck_name)
    return {'info': answer}


@app.route('/Server/rename_deck/<user_name>', methods=['POST','GET'])
@authentication
def rename_deck(user_name):
    data = request.json
    user_serv = Server(user_name)

    for key, value in data.items():
        deck_name = key
        new_deck_name = value
    answer = user_serv.rename_deck(deck_name, new_deck_name)
    return {'status': answer}


@app.route('/Server/delete_card_from_deck/<user_name>', methods=['POST','GET'])
@authentication
def delete_card_from_deck(user_name):
    data = request.json
    user_serv = Server(user_name)

    for key, value in data.items():
        deck_name = key
        card_name = value
    answer = user_serv.delete_card_from_deck(deck_name, card_name)
    return {'status': answer}


@app.route('/Server/delete_deck/<user_name>', methods=['POST','GET'])
@authentication
def delete_deck(user_name):
    data = request.json
    user_serv = Server(user_name)

    for key in data:
        deck_name = key
    answer = user_serv.delete_deck(deck_name)
    return {'status': answer}


@app.route('/Server/receive_all_decks/<user_name>', methods=['POST','GET'])
@authentication
def receive_all_decks(user_name):
    user_serv = Server(user_name)

    answer = user_serv.receive_all_decks()
    return {'status': True, 'info': answer}


@app.route('/Server/add_card_to_deck/<user_name>', methods=['POST','GET'])
@authentication
def add_card(user_name):
    """добавление существующей карты в колоду"""
    data = request.json
    user_serv = Server(user_name)

    for key, value in data.items():
        deck_name = key
        card_name = value
        answer = user_serv.add_card_to_deck(deck_name, card_name)
    return {'status': answer}


@app.route('/Server/add_new_to_card_card/<user_name>', methods=['POST','GET'])
@authentication
def add_new_card(user_name): # добавление новой(несуществующе карты) в колоду - по факту создание карты внутри колоды
    data = request.json
    user_serv = Server(user_name)

    for key, value in data.items():
        deck_name = key
        word = value[0]
        translate = value[1]
        answer = user_serv.add_new_card_to_deck(deck_name, word, translate)
    return {'status': answer}
