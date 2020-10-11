import requests

def registration(login, password):
    """Регистрация пользователя"""
    url = f'http://127.0.0.1:5000//Server/registration/{login}'
    passwd = {"password":password}
    response = requests.post(url, headers=passwd)
    print(response.json())
# registration('flexer','6666')


def write(word, translate, login, password):
    """создание карточки"""
    url = f'http://127.0.0.1:5000//Server/create_card/{login}'
    passwd = {"password":password}
    data = {word: translate}
    response = requests.post(url, json=data, headers=passwd)
    print(response.json())

write('eeee', 'roocckkk', 'flexer', '6666')
# write('cat', 'кот', 'flexer', '6666')
# write('mouse', 'мышь', 'flexer', '6666')
# write('beer', 'ПЕВАС', 'flexer', '6666')
# write('vova', 'вова', 'flexer', '6666')
# write('life', 'жизнь', 'flexer', '6666')
# write('parrot', 'попуг', 'flexer', '6666')
# write('mem', 'мэм', 'flexer', '6666')

def update(word, new_word, translate, login, password):
    """Изменение карточки"""
    url = f'http://127.0.0.1:5000//Server/update_card/{login}'
    passwd = {"password": password}
    data = {word:[new_word,translate]}
    response = requests.post(url,json=data, headers=passwd)
    print(response.json())
# update('SYCH','aaaaa','bbbbb','flexer','6666')

def get_card(word, login, password):
    """Получение карточки"""
    url = f'http://127.0.0.1:5000//Server/receive_card/{login}'
    passwd = {"password": password}
    data = {word:''}
    response = requests.post(url,json=data, headers=passwd)
    print(response.json())
# get_card('жумайсынба', 'flexer', '6666')

def get_all_cards(login, password):
    """Получение всех карточек"""
    url = f'http://127.0.0.1:5000//Server/receive_all_cards/{login}'
    passwd = {"password": password}
    response = requests.post(url, headers=passwd)
    print(response.json())
# get_all_cards('flexer','6666')

def delete_card(card_name, login, password):
    """Удаление карточки"""
    url = f'http://127.0.0.1:5000//Server/delete_card/{login}'
    passwd = {"password": password}
    data = {card_name: ''}
    response = requests.post(url, json=data, headers=passwd)
    print(response.json())
# delete_card('жумайсынба','flexer','6666')

def create_deck(deck_name, login, password, *args):
    """Создание колоды"""
    url = f'http://127.0.0.1:5000//Server/create_deck/{login}'
    passwd = {"password": password}
    data = {deck_name: args}
    response = requests.post(url, json=data, headers=passwd)
    print(response.json())
# create_deck('anything', 'flexer', '6666', 'dog', 'car', 'beer', 'vova', 'flex')
# create_deck('pets', 'flexer', '6666', 'dog', 'cat')
# create_deck('flex_deck', 'flexer', '6666', 'parrot', 'beer', 'bnv', 'bnvmm')

def get_deck(deck, login, password):
    """Получение колоды"""
    url = f'http://127.0.0.1:5000//Server/receive_deck/{login}'
    passwd = {"password": password}
    data = {deck:''}
    response = requests.post(url,json=data, headers=passwd)
    print(response.json())
# get_deck('anythingaa','flexer','6666')

def get_all_decks(login, password):
    """Получение всех колод"""
    url = f'http://127.0.0.1:5000//Server/receive_all_decks/{login}'
    passwd = {"password": password}
    response = requests.post(url, headers=passwd)
    print(response.json())
# get_all_decks('flexer', '6666')

def add_card_to_deck(login, password, deck_name, card_name):
    """добавление существующей карты в колоду"""
    url = f'http://127.0.0.1:5000//Server/add_card_to_deck/{login}'
    data = {deck_name: card_name}
    passwd = {"password": password}
    response = requests.post(url, json=data, headers=passwd)
    print(response.json())
# add_card_to_deck('flexer', '6666', 'shiddd', 'hjgjhkgj')

def add_new_card_to_deck(login, password, deck_name, word, translate):
    """Добавление в существующей колоду несуществующей карты"""
    url = f'http://127.0.0.1:5000//Server/add_new_to_card_card/{login}'
    data = {deck_name: [word, translate]}
    passwd = {"password": password}
    response = requests.post(url, json=data, headers=passwd)
    print(response.json())

# add_new_card_to_deck('flexer', '6666', 'anything', 'bench', 'скамейка')

def rename_deck(login, password, deck_name, new_deck_name):
    """Изменение название колоды"""
    url = f'http://127.0.0.1:5000//Server/rename_deck/{login}'
    data = {deck_name: new_deck_name}
    passwd = {"password": password}
    response = requests.post(url, json=data, headers=passwd)
    print(response.json())
# rename_deck('flexer', '6666', 'pets111451', 'pets66sd6')

def delete_card_from_deck(login, password, deck_name, card_name):
    """Удаление карты из колоды"""
    url = f'http://127.0.0.1:5000//Server/delete_card_from_deck/{login}'
    data = {deck_name: card_name}
    passwd = {"password": password}
    response = requests.post(url, json=data, headers=passwd)
    print(response.json())
# delete_card_from_deck('flexer','6666','pets66546','mem')

def delete_deck(login, password, deck_name):
    """Удаление колоды"""
    url = f'http://127.0.0.1:5000//Server/delete_deck/{login}'
    data = {deck_name:''}
    passwd = {"password": password}
    response = requests.post(url, json=data, headers=passwd)
    print(response.json())

# delete_deck('flexer','6666','вапавпвап')







