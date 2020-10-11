from sqlalchemy import create_engine
import logging
import re


"""Здесь все логика работы сервера"""

class ClientError(Exception):
    """ ERROR """


class ValidChange(object):
    """Дескриптор данных для валидации и исправления слов"""
    def _valid_wordsss(self, val):
        val = re.sub(r'[^a-z,A-Z,а-я,А-Я]+', r'', val)
        if not val.isalpha():
            raise ValueError('На вход поданы одни лишь цифры')
        return val

    def __init__(self, name = 'название атрибута'):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError(f'Неверный тип {value} - {type(value)}')

        if self.name in ['word', 'translate', 'deck_name']:
            value = self._valid_wordsss(value)
        instance.__dict__[self.name] = value


class Card:
    """Создание карточки (слово - перевод)"""

    word = ValidChange('word')
    translate = ValidChange('translate')

    def __init__(self, word, translate):
        self.word = word
        self.translate = translate

    # def translate(self, word):
    #     url = f'https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=ru&dt=t&q={word}'
    #     word_lst = requests.post(url)
    #     translate_word = word_lst.json()
    #     return translate_word[0][0][0]

    def save(self, login, deckid=0):
        WrapperDB().save_card(self.word, self.translate, login) # word ==card_name

    def update(self, word, new_word, new_translate):
        self.word = new_word
        self.translate = new_translate
        WrapperDB().update_card(word, new_word, new_translate)

    def __str__(self):
        return f"{self.word} {self.translate}"

    def __repr__(self):
        return f"{self.word} {self.translate}"


class Deck:
    """Создание колоды карт(по сути темы)"""
    # card_list - список объектов - карточек
    deck_name = ValidChange('deck_name')

    def __init__(self, deck_name, card_list): #или list id
        self.deck_name = deck_name
        self.card_list = card_list

    def save_deck(self, login):
        WrapperDB().save_deck(self.deck_name, self.card_list, login)

    def add_new_card(self):
        WrapperDB().save_card(login)


class Server:
    """Основная логика работы по созданию и передаче"""
    def __init__(self, login):#, password):
        self.login = login
        # self.password = password
        # self.authentication = Server.is_authentication()
        # print(self.authentication)

    @classmethod
    def is_authentication(cls, login, password):
        status = WrapperDB().is_authentication(login, password)
        return status

    # def registration(self, login, password):
    #     WrapperDB().registrationDB(login,password)

    def create_card(self, word, translate):
        a = Card(word, translate)
        a.save(self.login)

    def update_card(self, word, new_word, new_translate):
        card_obj = WrapperDB().get_card(word, self.login)
        if type(card_obj) is bool:
            return {word: 'not exists', 'status': False}
        card_obj.update(word, new_word, new_translate)
        return True

    def delete_card(self, card_name):
        return WrapperDB().delete_card(card_name, self.login)

    def create_deck(self,deck_name, card_list):
        b = Deck(deck_name, card_list)
        b.save_deck(self.login)

    def receive_deck(self, deck_name):
        return WrapperDB().get_deck(deck_name, self.login)

    def rename_deck(self, deck_name, new_deck_name):
        return WrapperDB().update_deck(deck_name, new_deck_name, self.login)

    def delete_card_from_deck(self, deck_name, card_name):
        try:
            deckid = WrapperDB().what_deck(deck_name, self.login)
            return WrapperDB().del_card_from_deck(card_name, deckid, self.login)
        except UnboundLocalError:
            return False, 'Wrong deck name'

    def delete_deck(self, deck_name):
        try:
            deckid = WrapperDB().what_deck(deck_name, self.login)
            return WrapperDB().del_deck(deckid, self.login)
        except UnboundLocalError:
            return False, 'Wrong deck name'

    def receive_card(self,word):
        card_obj = WrapperDB().get_card(word, self.login)
        if type(card_obj) is bool:
            return False
        return card_obj.word, card_obj.translate

    def receive_all_cards(self):
        word_list = []
        for i in WrapperDB().get_all_cards(self.login):
            word_list.append(i)
        return word_list

    def receive_all_decks(self):
        return WrapperDB().get_all_decks(self.login)

    def add_card_to_deck(self, deck_name, card_name):
         return WrapperDB().add_card_to_deck(deck_name,card_name, self.login)

    def add_new_card_to_deck(self, deck_name, word, translate):
        deck_id = WrapperDB().what_deck(deck_name, self.login)
        return WrapperDB().save_card(word, translate, self.login, deck_id)


class ConnectDB:
    """Соединение с базой данных"""
    def __init__(self):
        self.cur_string = self.get_conn()
        self.cur = create_engine(self.cur_string)
        # print('Создано подключение к БД')

    def get_conn(self):
        # with open("conf.json")
        host = "127.0.0.1"
        port = "5432"
        user = "postgres"
        passwd = "31471"
        db_name = "eng_words"
        cur_string = f"postgresql://{user}:{passwd}@{host}:{port}/{db_name}"
        return cur_string


class WrapperDB: # Вся алхимия здесь
    """Класс - посредник по передаче информации в БД.
    Необходим для того, чтобы сохранить логику приложения
    при замене базы данных(просто можем поменять базу на MongoDB(например)
    и редактировать только текущий класс и класс соединения с БД)"""
    def __init__(self): #  ConnectDB().cursor()
        # self.cur_str  ConnectDB.cur_string
        self.cur = ConnectDB().cur

    def save_card(self, word, translate, login, deckid=0):
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS cards (ID SERIAL PRIMARY KEY, "
            "Word varchar(255), Translate varchar(255), DeckID varchar(255), userID varchar(255))")
        result = self.cur.execute(f"SELECT user_id, login FROM users WHERE login = '{login}'")
        for userid in result:
            # print(userid[0])
            self.cur.execute(f"INSERT INTO cards (Word, Translate, DeckID, userID) VALUES ('{word}','{translate}','{deckid}','{userid[0]}')")
        return True

    def what_deck(self, deck_name, login):
        user = self.cur.execute(f"SELECT user_id, login FROM users WHERE login = '{login}'")
        for us in user:
            result = self.cur.execute(f"SELECT deck_id, deck_name FROM"
                                      f" decks WHERE deck_name = '{deck_name}' and userid = '{us[0]}'")
            for i in result:
                deck_id = i[0]
        return deck_id

    def delete_card(self, card_name, login):
        """Функция для удаления карты из всех колод"""
        user = self.cur.execute(f"SELECT user_id, login FROM users WHERE login = '{login}'")
        for us in user:
            self.cur.execute(f"DELETE FROM cards WHERE word = '{card_name}' AND userid = '{us[0]}'")
            return True

    def del_card_from_deck(self, card_name, deck_id, login):
        """Функция для удаления карты из колоды"""
        user = self.cur.execute(f"SELECT user_id, login FROM users WHERE login = '{login}'")
        for us in user:
            self.cur.execute(f"UPDATE cards SET deckid = '0' WHERE word = '{card_name}'"
                             f" and deckid = '{deck_id}' and userid = '{us[0]}'")
        return True

    def update_card(self, card_name, new_word, new_translate): #все нормально, логин не забыт, т/к сначала идет получение карты(get)
        """Функция для обновления данных карты"""
        self.cur.execute(f"UPDATE cards "
                         f"SET word = '{new_word}', translate ='{new_translate}' "
                         f"WHERE word = '{card_name}'")
        return True

    def save_deck(self, deck_name, card_list, login): # or deck_id
        """Функция для добавления колоды пользователем"""
        # print(deck_name)
        # print(card_list)
        # print(login)
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS decks (DECK_ID SERIAL PRIMARY KEY, "
            "deck_name varchar(255), userID varchar(255))")
        result = self.cur.execute(f"SELECT user_id, login FROM users WHERE login = '{login}' ")
        for user in result:
            self.cur.execute(f"INSERT INTO decks (deck_name, userID) VALUES ('{deck_name}', '{user[0]}')")
        res2 = self.cur.execute(f"SELECT deck_id, deck_name FROM decks "
                                f"WHERE deck_name = '{deck_name}' and userid = '{user[0]}'")
        for id_deck in res2:
            for card in card_list:
                self.cur.execute(f"UPDATE cards SET deckid = '{id_deck[0]}' "
                                 f"WHERE word = '{card}' and userid = '{user[0]}'")
        return True

    def del_deck(self, deck_id, login): # deck_id
        user = self.cur.execute(f"SELECT user_id, login FROM users WHERE login = '{login}'")
        for us in user:
            self.cur.execute(f"UPDATE cards SET deckid = '0' WHERE deckid = '{deck_id}' and userid = '{us[0]}'")
            self.cur.execute(f"DELETE FROM decks WHERE deck_id = '{deck_id}' and userid = '{us[0]}'")
        return True

    def update_deck(self, deck_name, new_deck_name,login):  # or deck_id
        user = self.cur.execute(f"SELECT user_id, login FROM users WHERE login = '{login}'")
        for us in user:
            self.cur.execute(f"UPDATE decks SET deck_name = '{new_deck_name}' WHERE deck_name = '{deck_name}' and userid = '{us[0]}'")
        return True

    def get_card(self, card_name, login):
        user = self.cur.execute(f"SELECT user_id, login FROM users WHERE login = '{login}'")
        for us in user:
            result = self.cur.execute(f"SELECT word, translate from cards WHERE word = '{card_name}' AND userid = '{us[0]}'")
            for i in result:
                #здесь все начинает ломаться при запросе несуществующего слова
                word, translate = i[0], i[1]
            try:
                obj = Card(word, translate)
                return obj
            except UnboundLocalError:
                return False

    def get_all_cards(self, login):
        """Возвращает данные для всех карт пользователя"""
        user = self.cur.execute(f"SELECT user_id, login FROM users WHERE login = '{login}'")
        for us in user:
            result = self.cur.execute(f"SELECT word, translate from cards WHERE userid = '{us[0]}'")

            for i in result:
                word, translate = i[0], i[1]
                obj = Card(word, translate)
                yield obj

    def get_deck(self, deck_name, login):
        deck_dict = {}
        card_dict = {}
        user = self.cur.execute(f"SELECT user_id, login FROM users WHERE login = '{login}'")
        for us in user:
            deck = self.cur.execute(f"SELECT deck_id, deck_name FROM decks WHERE userid = '{us[0]}' and deck_name = '{deck_name}'")
            for i in deck:
                deck_dict['deck_name'] = i[1]
                cards = self.cur.execute(f"SELECT word, translate FROM cards WHERE userid = '{us[0]}' and deckid = '{i[0]}'")
                for card in cards:
                    card_dict[card[0]] = card[1]
            if len(card_dict) == 0:
                deck_dict['cards'] = f'No cards or deck with name {deck_name} not exists'
                status = False
            else:
                deck_dict['cards'] = card_dict
                status = True
            return deck_dict, {'status': status}

    def get_all_decks(self, login):
        """Получение всех колод"""
        decks_dict = {}
        decks_list = []
        user = self.cur.execute(f"SELECT user_id, login from users WHERE login = '{login}'")
        for us in user:
            all_decks = self.cur.execute(f"SELECT deck_name from decks WHERE userid = '{us[0]}'")
            for deck in all_decks:
                decks_list.append(deck[0])
            decks_dict['decks'] = decks_list
        return decks_dict

    def add_card_to_deck(self, deck_name, card_name, login):
        """Добавление существующей карты в колоду"""
        user = self.cur.execute(f"SELECT user_id, login from users WHERE login = '{login}'")
        for us in user:
            deck = self.cur.execute(f"SELECT deck_id, deck_name from decks WHERE userid = '{us[0]}' and deck_name = '{deck_name}'")
            for elem in deck:
                self.cur.execute(f"UPDATE cards SET deckid = '{elem[0]}' WHERE word = '{card_name}' and userid = '{us[0]}'")
        return True

    def is_authentication(self, login, password):
        result = self.cur.execute(f"SELECT login, password FROM users WHERE login = '{login}' AND password = '{password}'")
        for user in result:
            if user:
                return True
        return False

    def registrationDB(self, login, password):
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS users (USER_ID SERIAL PRIMARY KEY,  login VARCHAR(50), password VARCHAR(50))")

        if self.user_in_DB(login):
            raise ClientError('Такой пользователь уже существует') # как сообщить клиенту? try except?
        else:
            result = self.cur.execute(f"INSERT INTO users (login, password) VALUES ('{login}','{password}')")
            return True

    def user_in_DB(self,login):
        result = self.cur.execute(f"SELECT login, password FROM users WHERE login = '{login}'")
        for user in result:
            if user:
                return True
        return False



    # def create_table(self):
    #     result = self.cur.execute(f"CREATE TABLE users (USER_ID SERIAL PRIMARY KEY,  login VARCHAR(50), password VARCHAR(50))")

    # def registration(self):
    #     result = self.cur.execute("INSERT INTO (login, password)")

# WrapperDB().create_table()
# print(WrapperDB().user_in_DB('vasya'))
