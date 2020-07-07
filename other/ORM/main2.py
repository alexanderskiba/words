from flask import Flask, request
from flex_server import Server, Deck, ClientError, WrapperDB

app = Flask(__name__)
@app.route('/Server/registration/<user_name>', methods=['POST','GET'])
def registration(user_name):
    login = user_name
    password = request.headers['Password']
    status = Server().registration(login, password)
    if status:
        user_id = Server().authentication(login, password)
        return {"user_id":user_id[0], 'status': True}
    return {"status": False, "info": 'this login already exists'}
#!!!!

@app.route('/Server/authentication/<user_name>', methods=['POST','GET'])
def authentication(user_name):
    login = user_name
    password = request.headers['Password']
    user_id = Server().authentication(login, password)
    if user_id:
        return {"user_id":user_id[0], 'status': True}
    return {"status": False, "info": 'this login already exists'}


@app.route('/Server/create_card/<user_id>', methods=['POST','GET'])
def create_card(user_id):
    data = request.json
    user_serv = Server()
    for key, item in data.items():
        word = key
        translate = item
        answer = user_serv.create_card(word, translate, user_id)
    return {"status": answer}



@app.route('/Server/update_card/<user_id>', methods=['POST','GET'])
def update_card(user_id):
    data = request.json
    user_serv = Server()
    for key, item in data.items():
        word = key
        new_word = item[0]
        translate = item[1]
        answer = user_serv.update_card(user_id, word, new_word, translate)

    return {"status": answer}


@app.route('/Server/delete_card/<user_id>', methods=['POST','GET'])
def delete_card(user_id):
    data = request.json
    user_serv = Server()
    for key in data:
        card_name = key
    answer = user_serv.delete_card(user_id, card_name)
    return {"status":answer,
            "delete card": card_name}

@app.route('/Server/receive_card/<user_id>', methods=['POST','GET'])
def receive_card(user_id):
    data = request.json
    user_serv = Server()
    for key, item in data.items():
        word = key
    card_dict = {}
    card = user_serv.receive_card_by_str(user_id, word)

    word, translate = card[0].word, card[0].translate
    card_dict['word'] = word
    card_dict['translate'] = translate
    return {"status": True, "info": card_dict}


@app.route('/Server/receive_all_cards/<user_id>', methods=['POST','GET'])
def receive_all_cards(user_id):
    user_serv = Server()
    rec_dict = {}
    # card_list = []
    # rec_dict["status"] = True
    # rec_dict["cards"] = card_list
    answer = user_serv.receive_all_cards(user_id)
    print(answer)
    for card in answer:
        word = card.word
        translate = card.translate
        rec_dict[word] = translate
    return {"status": True, "info": rec_dict}

@app.route('/Server/create_deck/<user_id>', methods=['POST','GET'])
def create_deck(user_id):
    data = request.json  # принимаем словарь от клиента
    user_serv = Server()
    for key in data:
        deck_name = key
    answer = user_serv.create_deck(user_id, deck_name)
    return {'status': answer, 'create deck': deck_name}
    # return {"status": False, "info": 'wrong client'}

@app.route('/Server/receive_deck/<user_id>', methods=['POST','GET'])
def receive_deck(user_id):
    user_serv = Server()
    data = request.json
    for key in data:
        deck_name = key
    answer = user_serv.receive_deck(user_id, deck_name)
    rec_dict = {}
    for card in answer:
        word = card.word
        translate = card.translate
        rec_dict[word] = translate
    return {"status": True, "info": rec_dict}


@app.route('/Server/rename_deck/<user_id>', methods=['POST','GET'])
def rename_deck(user_id):
    data = request.json
    user_serv = Server()
    for key, value in data.items():
        deck_name = key
        new_deck_name = value
    answer = user_serv.rename_deck(user_id, deck_name, new_deck_name)
    return {'status': answer}
    # return {"status": False, "info": 'wrong client'}
#
# @app.route('/Server/delete_card_from_deck/<user_id>', methods=['POST','GET'])
# def delete_card_from_deck(user_id):
#     user_serv = Server()
#     data = request.json
#     for key, value in data.items():
#         deck_name = key
#         card_name = value
#     answer = user_serv.delete_card_from_deck(deck_name, card_name)
#     return {'status': answer}
#     # return {"status": False, "info": 'wrong client'}

@app.route('/Server/delete_deck/<user_id>', methods=['POST','GET'])
def delete_deck(user_id):
    user_serv = Server()
    data = request.json
    for key in data:
        deck_name = key
    answer = user_serv.delete_deck(user_id, deck_name)
    return {'status': answer}


@app.route('/Server/receive_all_decks/<user_id>', methods=['POST','GET'])
def receive_all_decks(user_id):
    user_serv = Server()
    answer = user_serv.receive_all_decks(user_id)
    deck_dict = {}
    deck_list = []
    for deck in answer:
        deck_list.append(deck.deck_name)
        # deck_dict['decks'] = deck_list.append(deck.deck_name)
    deck_dict['decks'] = deck_list
    return {'status': True, 'info': deck_dict}

@app.route('/Server/add_card_to_deck/<user_id>', methods=['POST','GET'])
def add_card(user_id):
    """добавление существующей карты в колоду"""
    data = request.json
    user_serv = Server()
    for key, value in data.items():
        deck_name = key
        card_name = value
    answer = user_serv.change_deck_of_card(user_id, card_name, deck_name)
    return {'status': answer}

# @app.route('/Server/add_new_to_card_card/<user_name>', methods=['POST','GET'])
# def add_new_card(user_name): # добавление новой(несуществующе карты) в колоду - по факту создание карты внутри колоды
#     login = user_name
#     password = request.headers['Password']
#     data = request.json
#     for key, value in data.items():
#         deck_name = key
#         word = value[0]
#         translate = value[1]
#         user_serv = Server(login, password)
#         if not user_serv.authentication:
#             return {"status": False, "info": 'wrong client'}
#         answer = user_serv.add_new_card_to_deck(deck_name, word, translate)
#     return {'status': answer}


if __name__ == "__main__":
    app.run()