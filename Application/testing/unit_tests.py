import unittest
import sys


# через from file import class или func прокидываешь сюда, я прям тут напишу


def summ(a, b):
    try:
        summ = int(a) + int(b)
    except ValueError:
        return'Неверные данные!'
    return summ


       
class TestEstimation(unittest.TestCase):
    """ 
    self.widget -  переменная в которую складываешь объект который нужно потестить
    self.assertEqual - два аргумента, 
          1-й действительные ответ функции или класса
          2-й это ответ который ожидаешь от функции если 1 и 2 несовпали тест провалится
     есть много всяких иквелов assertTrue() ... (гуугл)
    """
    def test_summ_int(self):
        self.widget = summ(1, 6)
        self.assertEqual(self.widget, 7)
    
    def test_summ_str(self):
        self.widget = summ('1', 1)
        self.assertEqual(self.widget, 2)

    def test2_summ_str(self):
        self.widget = summ('a', 1)
        self.assertEqual(self.widget, 'Неверные данные!')

    def test_summ_float(self):
        self.widget = summ(2.8, 9.00001)
        self.assertEqual(self.widget, 11)


if __name__ == '__main__':
    unittest.main()
# можно запускать через консоль: unittest file_name.py