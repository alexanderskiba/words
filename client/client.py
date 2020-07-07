import requests
from client_conf import HOST, PORT

class ClientError(Exception):
    """ ERROR """

class Send:
    def registration(self, login, password):
        """Регистрация пользователя"""
        url = f'http://{HOST}:{PORT}//Server/registration/{login}'
        passwd = {"password": password}
        response = requests.post(url, headers=passwd)
        return response.json()
    # registration('flexer','6666')

    def authentication(self, login, password):
        """Аутинтентификация пользователя"""
        url = f'http://{HOST}:{PORT}//Server/authentication/{login}'
        passwd = {"password": password}
        response = requests.post(url, headers=passwd)
        return response.json()


    def write(self, user_id, word, translate):
        """создание карточки"""
        url = f'http://{HOST}:{PORT}//Server/create_card/{user_id}'
        data = {word: translate}
        response = requests.post(url, json=data)
        print(response.json())

    # write('car', 'машина', 'flexer', '6666')
    # write('cat', 'кот', 'flexer', '6666')
    # write('mouse', 'мышь', 'flexer', '6666')
    # write('beer', 'ПЕВАС', 'flexer', '6666')
    # write('vova', 'вова', 'flexer', '6666')
    # write('flex', 'жесткость', 'flexer', '6666')
    # write('parrot', 'попуг', 'flexer', '6666')
    # write('mem', 'мэм', 'flexer', '6666')

    def update(self, user_id, word, new_word, translate):
        """Изменение карточки"""
        url = f'http://{HOST}:{PORT}//Server/update_card/{user_id}'
        data = {word:[new_word,translate]}
        response = requests.post(url,json=data)
        print(response.json())
    # update('flex','mouse','мышь','bob','qwerty')

    def get_card(self, user_id, word):
        """Получение карточки"""
        url = f'http://{HOST}:{PORT}//Server/receive_card/{user_id}'
        data = {word:''}
        response = requests.post(url,json=data)
        print(response.json())
    # get_card('beer', 'flexer', '6666')

    def get_all_cards(self, user_id):
        """Получение всех карточек"""
        url = f'http://{HOST}:{PORT}//Server/receive_all_cards/{user_id}'
        response = requests.post(url)
        print(response.json())
    # get_all_cards('bob','qwerty')

    def delete_card(self, user_id, card_name):
        """Удаление карточки"""
        url = f'http://{HOST}:{PORT}//Server/delete_card/{user_id}'
        data = {card_name: ''}
        response = requests.post(url, json=data)
        print(response.json())
    # delete_card('cat','bob','qwerty')

    def create_deck(self, user_id, deck_name):
        """Создание колоды"""
        url = f'http://{HOST}:{PORT}//Server/create_deck/{user_id}'
        data = {deck_name: ''}
        response = requests.post(url, json=data)
        print(response.json())
    # create_deck('anything', 'flexer', '6666', 'dog', 'car', 'beer', 'vova', 'flex')
    # create_deck('pets', 'flexer', '6666', 'dog', 'cat')
    # create_deck('pets111', 'flexer', '6666', 'beer', 'parrot', 'mem', 'cat')

    def get_deck(self, user_id, deck):
        """Получение колоды"""
        url = f'http://{HOST}:{PORT}//Server/receive_deck/{user_id}'
        data = {deck:''}
        response = requests.post(url,json=data)
        print(response.json())
    # get_deck('anything','flexer','6666')

    def get_all_decks(self, user_id):
        """Получение всех колод"""
        url = f'http://{HOST}:{PORT}//Server/receive_all_decks/{user_id}'
        response = requests.post(url)
        print(response.json())
    # get_all_decks('flexer', '6666')

    def add_card_to_deck(self, user_id, deck_name, card_name):
        """добавление существующей карты в колоду"""
        url = f'http://{HOST}:{PORT}//Server/add_card_to_deck/{user_id}'
        data = {deck_name: card_name}
        response = requests.post(url, json=data)
        print(response.json())
    # add_card_to_deck('flexer', '6666', 'anything', 'mem')

    # def add_new_card_to_deck(self, user_id, deck_name, word, translate):
    #     """Добавление в существующей колоду несуществующей карты"""
    #     url = f'http://127.0.0.1:5000//Server/add_new_to_card_card/{user_id}'
    #     data = {deck_name: [word, translate]}
    #     response = requests.post(url, json=data)
    #     print(response.json())

    # add_new_card_to_deck('flexer', '6666', 'anything', 'bench', 'скамейка')

    def rename_deck(self, user_id, deck_name, new_deck_name):
        """Изменение название колоды"""
        url = f'http://{HOST}:{PORT}//Server/rename_deck/{user_id}'
        data = {deck_name: new_deck_name}
        response = requests.post(url, json=data)
        print(response.json())
    # rename_deck('flexer', '6666', 'pets111', 'pets666')

    # def delete_card_from_deck(self, user_id, deck_name, card_name):
    #     """Удаление карты из колоды"""
    #     url = f'http://127.0.0.1:5000//Server/delete_card_from_deck/{user_id}'
    #     data = {deck_name: card_name}
    #     response = requests.post(url, json=data)
    #     print(response.json())
    # # delete_card_from_deck('flexer','6666','pets666','mem')

    def delete_deck(self,user_id, deck_name):
        """Удаление колоды"""
        url = f'http://{HOST}:{PORT}//Server/delete_deck/{user_id}'
        data = {deck_name:''}
        response = requests.post(url, json=data)
        print(response.json())

    # delete_deck('flexer','6666','pets666')
method_storage = {'write':Send().write, 'update': Send().update,
                  'get_card': Send().get_card, 'get_all_cards': Send().get_all_cards,
                  'delete_card': Send().delete_card, 'create_deck': Send().create_deck,
                  'get_deck': Send().get_deck, 'get_all_decks': Send().get_all_decks,
                  'add_card_to_deck': Send().add_card_to_deck,
                  'rename_deck': Send().rename_deck,
                  'delete_deck': Send().delete_deck
                  }



def auth_reg():
    print('Для того, чтобы начать работу введите логин и пароль')
    while True:
        try:
            print('Аутентификация\n\n\n')
            log_in = input('Введите логин: ')
            pass_word = input('Введите пароль: ')
            answer = Send().authentication(log_in, pass_word)
            if answer['status']:
                user_id = answer['user_id']
                print('Аутентификация', answer['status'], '\n\n\n')
                break
        except UnicodeDecodeError:
            print('Все упало(юникод), попробуй еще')
            continue

        if not answer['status']:
            stat = input('если хотите зарегаться введите REG, для повторной попытки нажмине Enter: \n')
            if stat == 'REG':
                print('Регистрация\n\n\n')
                log_in = input('Введите логин: ')
                pass_word = input('Введите пароль: ')
                answer = Send().registration(log_in, pass_word)
                print('Регистрация: ', answer['status'])
    return user_id

def sending(user_id):
    while True:
        print('\n\n\nСписок доступных действий: \n'
              'Для создания карточки введите write слово перевод \n'
              'Для изменения карточки введите update слово новое_слово новый_перевод \n'
              'Для получения карточки введите get_card слово \n'
              'Для получения всех карточек введите get_all_cards \n'
              'Для удаления карточки введите delete_card слово \n'
              'Для создания колоды введите create_deck название_колоды \n'
              'Для получения колоды введите get_deck название_колоды\n'
              'Для получения всех колод введите get_all_decks \n'
              'Для добавления существующей карты в колоду введите add_card_to_deck название_колоды слово \n'
              'Для изменения названия колоды введите rename_deck название_колоды новое_название_колоды \n'
              'Для удаления колоды введите delete_deck название_колоды \n'
              'Для завершения работы введите end\n')
        try:
            act = input('Введите действие: ')
            list_args = act.split(' ')
            list_args.insert(1, user_id)
        except UnicodeDecodeError:
            print('\n\nВсе упало(юникод), попробуй еще\n\n')
            continue

        if list_args[0] == 'end':
            print('Завершение работы')
            break
        else:
            try:
                method_storage[list_args[0]](*list_args[1:])
            except KeyError:
                print('Неверное действие')
                continue
    return True


def main():
    user_id = auth_reg()
    if user_id:
        sending(user_id)


if __name__ == "__main__":
    main()
