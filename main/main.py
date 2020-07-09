from flask import Flask, request
from server import Server, Deck, ClientError, WrapperDB


app = Flask(__name__)
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
def create_card(user_name):
    # print('Создаем карточку')
    login = user_name
    password = request.headers['Password']
    user_serv = Server(login, password)
    if user_serv.authentication:
        data = request.json #принимаем словарь от клиента
        for key, item in data.items():
            word = key
            translate = item
            user_serv.create_card(word,translate)
        return {"status": True}
    return {"status": False, "info": 'wrong client'}


@app.route('/Server/update_card/<user_name>', methods=['POST','GET'])
def update_card(user_name):
    login = user_name
    password = request.headers['Password']
    user_serv = Server(login, password)
    if user_serv.authentication:
        data = request.json
        for key, item in data.items():
            word = key
            new_word = item[0]
            translate = item[1]
            answer = user_serv.update_card(word, new_word, translate)

        return {"status":answer }
    return {"status": False, "info": 'wrong client'}


@app.route('/Server/delete_card/<user_name>', methods=['POST','GET'])
def delete_card(user_name):
    login = user_name
    password = request.headers['Password']
    user_serv = Server(login, password)
    if user_serv.authentication:
        data = request.json
        for key in data:
            card_name = key
        user_serv.delete_card(card_name)
        return {"status":True,
                "delete card": card_name}
    return {"status": False, "info": 'wrong client'}

@app.route('/Server/receive_card/<user_name>', methods=['POST','GET'])
def receive_card(user_name):
    login = user_name
    password = request.headers['Password']
    user_serv = Server(login, password)
    if user_serv.authentication:
        data = request.json
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

    return {"status": False, "info": 'wrong client'}

@app.route('/Server/receive_all_cards/<user_name>', methods=['POST','GET'])
def receive_all_cards(user_name):
    login = user_name
    password = request.headers['Password']
    user_serv = Server(login, password)
    if user_serv.authentication:
        rec_dict = {}
        card_list = []
        rec_dict["status"] = True
        rec_dict["cards"] = card_list
        for i in user_serv.receive_all_cards():
            card_list.append({i.word:i.translate})
        return rec_dict
    return {"status": False, "info": 'wrong client'}

@app.route('/Server/create_deck/<user_name>', methods=['POST','GET'])
def create_deck(user_name):
    login = user_name
    password = request.headers['Password']
    user_serv = Server(login, password)
    if user_serv.authentication:
        data = request.json  # принимаем словарь от клиента
        for key, value in data.items():
            deck_name = key
            cards = value
            # print(cards)
        user_serv.create_deck(deck_name, cards)
        return {'status': True, 'create deck': deck_name}
    return {"status": False, "info": 'wrong client'}

@app.route('/Server/receive_deck/<user_name>', methods=['POST','GET'])
def receive_deck(user_name):
    login = user_name
    password = request.headers['Password']
    user_serv = Server(login, password)
    if user_serv.authentication:
        data = request.json
        for key in data:
            deck_name = key
        answer = user_serv.receive_deck(deck_name)
        return {'status': True, 'info': answer}
    return {"status": False, "info": 'wrong client'}

@app.route('/Server/rename_deck/<user_name>', methods=['POST','GET'])
def rename_deck(user_name):
    login = user_name
    password = request.headers['Password']
    user_serv = Server(login, password)
    if user_serv.authentication:
        data = request.json
        for key, value in data.items():
            deck_name = key
            new_deck_name = value
        answer = user_serv.rename_deck(deck_name, new_deck_name)
        return {'status': answer}
    return {"status": False, "info": 'wrong client'}

@app.route('/Server/delete_card_from_deck/<user_name>', methods=['POST','GET'])
def delete_card_from_deck(user_name):
    login = user_name
    password = request.headers['Password']
    user_serv = Server(login, password)
    if user_serv.authentication:
        data = request.json
        for key, value in data.items():
            deck_name = key
            card_name = value
        answer = user_serv.delete_card_from_deck(deck_name, card_name)
        return {'status': answer}
    return {"status": False, "info": 'wrong client'}

@app.route('/Server/delete_deck/<user_name>', methods=['POST','GET'])
def delete_deck(user_name):
    login = user_name
    password = request.headers['Password']
    user_serv = Server(login, password)
    if user_serv.authentication:
        data = request.json
        for key in data:
            deck_name = key
        answer = user_serv.delete_deck(deck_name)
        return {'status': answer}
    return {"status": False, "info": 'wrong client'}

@app.route('/Server/receive_all_decks/<user_name>', methods=['POST','GET'])
def receive_all_decks(user_name):
    login = user_name
    password = request.headers['Password']
    user_serv = Server(login, password)
    if user_serv.authentication:
        answer = user_serv.receive_all_decks()
        return {'status': True, 'info': answer}
    return {"status": False, "info": 'wrong client'}

@app.route('/Server/add_card_to_deck/<user_name>', methods=['POST','GET'])
def add_card(user_name):
    """добавление существующей карты в колоду"""
    login = user_name
    password = request.headers['Password']
    data = request.json
    for key, value in data.items():
        deck_name = key
        card_name = value
        user_serv = Server(login,password)
        if not user_serv.authentication:
            return {"status": False, "info": 'wrong client'}
        answer = user_serv.add_card_to_deck(deck_name, card_name)
    return {'status': answer}

@app.route('/Server/add_new_to_card_card/<user_name>', methods=['POST','GET'])
def add_new_card(user_name): # добавление новой(несуществующе карты) в колоду - по факту создание карты внутри колоды
    login = user_name
    password = request.headers['Password']
    data = request.json
    for key, value in data.items():
        deck_name = key
        word = value[0]
        translate = value[1]
        user_serv = Server(login, password)
        if not user_serv.authentication:
            return {"status": False, "info": 'wrong client'}
        answer = user_serv.add_new_card_to_deck(deck_name, word, translate)
    return {'status': answer}


if __name__ == "__main__":
    app.run()