#todo создать порядок для аргументов функций

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class ClientError(Exception):
    """ ERROR """

"""Здесь все логика работы сервера"""
class Card(Base):
    """
    Создание карточки (слово - перевод)
    """
    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True)
    word = Column(String(255))
    translate = Column(String(255))
    deckid = Column(Integer)
    userid = Column(Integer)

    def __init__(self, word, translate, deckid, userid):
        self.word = word
        self.translate = translate
        self.deckid = deckid
        self.userid = userid

    def __str__(self):
        return f"{self.word} {self.translate}"

    def __repr__(self):
        return f"{self.word} {self.translate}"

    def get_dict(self):
        return {'userid': self.userid, 'deckid': self.deckid,
                'word': self.word, 'translate': self.translate}


class Deck(Base):
    """
    Создание колоды карт(по сути темы)
    """
    __tablename__ = 'decks'

    deck_id = Column(Integer, primary_key=True)
    deck_name = Column(String(255))
    userid = Column(Integer)

    def __init__(self, deck_name, userid):
        self.deck_name = deck_name
        self.userid = userid

    def get_dict(self):
        return {'deckname': self.deck_id,
                'userid': self.userid}


class User(Base):
    """Класс пользователь"""
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    login = Column(String(255))
    password = Column(String(255))

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def get_dict(self):
        return {'login': self.login, 'user_id': self.user_id}

    #todo __repr__ or __str__


class Server:
    """Основная логика работы по созданию и передаче"""
    def __init__(self):
        host = "127.0.0.1"
        port = "5432"
        user = "postgres"
        passwd = "31471"
        db_name = "eng_words"
        self._database_ = WrapperDB(host, port, user, passwd, db_name)
        # self.login = login
        # self.password = password
        # self.user = self.authentication(login, password)
        # print(self.authentication)

    @classmethod
    def get_result(self, data):
        answer = data.copy()
        if not answer:
            answer = dict()
            answer['status'] = False
        else:
            answer['status'] = True
        return answer

    def authentication(self, login, password):
        """
        Аутентификация пользователя по логину-паролю
        """
        user = self._database_.get_user(login, password)
        return user

    def registration(self, login, password):
        """
        Регистрация нового пользователя
        """
        status = self._database_.add_user(login, password)
        return status

    def create_card(self, word, translate, user_id, deck_id=0):
        """
        Создание карты
        """
        status = self._database_.save_card(word, translate, user_id, deck_id)
        return status

    def change_deck_of_card(self, user_id, card_name, deck_name):
        deck = self._database_.get_decks_by_name(user_id, deck_name)
        deck_id = str(deck[0].deck_id)
        result = self._database_.change_deck_of_card(user_id, card_name, deck_id)
        if not result:
            return False
        return True

    def update_card(self, user_id, word, new_word, new_translate):
        """
        Обновление данных карты
        """
        status = self._database_.update_card(user_id, word, new_word, new_translate)
        return status

    def delete_card(self, user_id, word):
        """
        Удаление карты
        """
        status = self._database_.delete_card(user_id, word)
        return status

    def receive_card_by_str(self, user_id, str_for_serching):
        """
        Получение карты по строке, которая должна соответствовать
        слову или его переводу
        """
        cards = self._database_.get_cards_by_str(user_id, str_for_serching)
        return cards

    def create_deck(self, user_id, deck_name):
        """
        Создание колоды
        """
        status = self._database_.save_deck(user_id, deck_name)
        return status

    def receive_deck(self, user_id, deck_name):
        """
        Получение списка кард колоды
        """
        deck = self._database_.get_decks_by_name(user_id, deck_name)
        deck_id = str(deck[0].deck_id)
        cards_of_deck = self._database_.get_cards_of_deck(user_id, deck_id)
        return cards_of_deck
        # return deck

    def rename_deck(self, user_id, deck_name, new_deck_name):
        """
        Переименование колоды
        """
        deck = self._database_.get_decks_by_name(user_id, deck_name)
        deck_id = str(deck[0].deck_id)
        answer = self._database_.update_deck(user_id, deck_id, new_deck_name)
        return answer

    def delete_deck(self, user_id, deck_name):
        """
        Удаление колоды со всеми ее картами
        """
        deck = self._database_.get_decks_by_name(user_id, deck_name)
        deck_id = str(deck[0].deck_id)
        answer = self._database_.del_deck(user_id, deck_id)
        return answer

    def receive_all_cards(self, user_id):
        """
        Получить все карты пользователя
        """
        cards = self._database_.get_all_cards(user_id)
        return cards

    def receive_all_decks(self, user_id):
        """
        Получить все колоды пользователя
        """
        decks = self._database_.get_all_decks(user_id)
        return decks


class ConnectDB:
    """Соединение с базой данных"""

    def __init__(self, host, port, user, passwd, db_name):

        # Todo Понять, что делать с "postgresql" в строке
        # Скорее всего ее должен генерить админ или кто этим занимается
        # Поэтому в будущем db_connection_str будет аргументом
        db_connection_str = f"postgresql://{user}:{passwd}@{host}:{port}/{db_name}"
        self._cur_ = create_engine(db_connection_str)

        Session = sessionmaker(bind=self._cur_)
        self.session = Session()


class WrapperDB: # Вся алхимия здесь
    """Класс - посредник по передаче информации в БД.
    Необходим для того, чтобы сохранить логику приложения
    при замене базы данных(просто можем поменять базу на MongoDB(например)
    и редактировать только текущий класс и класс соединения с БД)"""
    def __init__(self, host, port, user, passwd, db_name):
        self._cur_ = ConnectDB(host, port, user, passwd, db_name).session

    def save_card(self, word, translation, user_id, deck_id):
        """
        Создание новой карты в таблице cards
        Предполагается, что deck_id проверен заранее
        """

        new_card = Card(word, translation, deck_id, user_id)
        self._cur_.add(new_card)
        a = self._cur_.commit()
        return True

    def change_deck_of_card(self, user_id, card_name, new_deck_id):
        """
        Изменение колоды карты
        """
        card = self.get_card_by_id(user_id, card_name)
        if card:
            card.deckid = new_deck_id
            self._cur_.add(card)
            self._cur_.commit()
            return True
        return False

    def get_cards_by_str(self, user_id, str_for_searching):
        """
        Получение карт по полному совпадению card.word или
        card.translation с str_for_searching
        """
        by_word = self._cur_.query(Card).filter(Card.word == str_for_searching and
                                                Card.userid == user_id).all()
        by_word = set(by_word)
        by_translation = self._cur_.query(Card).filter(Card.translate == str_for_searching and
                                                       Card.userid == user_id).all()
        by_translation = set(by_translation)

        cards = by_word.union(by_translation)
        cards_list = list(cards)
        return cards_list

    def get_card_by_id(self, user_id, word):
        """
        Получение карты по id
        """
        query = self._cur_.query(Card).filter(Card.word == word and Card.userid == user_id)
        card = query.one_or_none()
        return card

    def delete_card(self, user_id, word):
        """
        Удаление карты
        """
        card = self.get_card_by_id(user_id, word)
        if card:
            self._cur_.delete(card)
            self._cur_.commit()
            return True
        return False

    def update_card(self, user_id, word, new_word, new_translate):
        """
        Обновление данных карты
        """
        card = self.get_card_by_id(user_id, word)
        if card:
            card.word = new_word
            card.translate = new_translate
            self._cur_.add(card)
            self._cur_.commit()
            return True
        return False

    def get_all_cards(self, user_id):
        """
        Получение всех карт пользователя
        """
        cards_list = self._cur_.query(Card).filter(Card.userid == user_id).all()
        return cards_list

    def save_deck(self, user_id, deck_name):
        """
        Создание колоды
        """
        deck = Deck(deck_name, user_id)
        self._cur_.add(deck)
        self._cur_.commit()
        return True

    def del_deck(self, user_id, deck_id): # deck_id
        """
        Удаление колоды со всеми ее картами (каскад)
        """
        deck = self.get_deck_by_id(user_id, deck_id)
        if deck:
            self._cur_.delete(deck)
            self._cur_.commit()
            return True
        return False

    def update_deck(self, user_id, deck_id, new_deck_name):
        """
        Обновление данных колоды
        """
        deck = self.get_deck_by_id(user_id, deck_id)
        if deck:
            deck.deck_name = new_deck_name
            self._cur_.add(deck)
            self._cur_.commit()
            return True
        return False

    def get_decks_by_name(self, user_id, deck_name):
        """
        Получение колод, у которых deck.deck_name совпадает с deck_name
        """
        #todo Сделать неполное совпадение
        query = self._cur_.query(Deck).filter(Deck.deck_name == deck_name and Deck.userid == user_id)
        decks = query.all()
        return decks

    def get_deck_by_id(self, user_id, deck_id):
        """
        Получение колоды по id
        """
        query = self._cur_.query(Deck).filter(Deck.deck_id == deck_id and Deck.userid == user_id)
        deck = query.one_or_none()
        return deck

    def get_all_decks(self, user_id):
        """
        Получение всех колод пользователя
        """
        decks = self._cur_.query(Deck).filter(Deck.userid == user_id).all()
        return decks

    def get_cards_of_deck(self, user_id, deck_id):
        """
        Получение всех карт колоды
        """
        query = self._cur_.query(Card).filter(Card.deckid == deck_id and Card.userid == user_id)
        cards = query.all()
        return cards

    def get_user(self, login, password):
        """
        Получение пользователя, если он существует в
        таблице Users.
        """
        query = self._cur_.query(User.user_id).filter(User.login == login, User.password == password)
        user = query.one_or_none()
        return user

    def add_user(self, user_name, password):
        """
        Добавление нового пользователя, если не существует другого
        пользователя с таким же user_name
        """
        if not self.is_user_exist(user_name):
            new_user = User(user_name, password)
            self._cur_.add(new_user)
            self._cur_.commit()
            return True
        return False

    def is_user_exist(self, user_name):
        """
        Проверка, существует ли пользователь
        """
        query = self._cur_.query(User).filter(User.login == user_name)
        user = query.one_or_none()

        if user:
            return True
        return False
