Модуль RS Code
===============

.. module:: rs_code
   :platform: Unix, Windows
   :synopsis: Модуль для операций с кодированием Рида-Соломона.



Введение
------------

Этот модуль предоставляет функции для операций с кодированием Рида-Соломона.

Функции
---------

.. autofunction:: rs_generator_poly

.. autofunction:: rs_encode_msg

Подробности Функций
----------------

.. autofunction:: rs_generator_poly

   Эта функция вычисляет многочлен-генератор для заданного числа избыточных символов.

   :param red_code_len: Количество символов, представляющих избыточный код.
   :type red_code_len: int
   :return: Многочлен-генератор.
   :rtype: list

.. autofunction:: rs_encode_msg

   Эта функция кодирует входное сообщение, представленное вектором многочленов, добавляя избыточную информацию.

   :param msg_in: Входное сообщение, представленное вектором многочленов (в данном случае целых чисел).
   :type msg_in: list
   :param red_code_len: Количество символов, представляющих избыточный код.
   :type red_code_len: int
   :return: Закодированное сообщение в виде вектора [msg_in] + [избыточная информация] (в данном случае целые числа).
   :rtype: list
   :raises ValueError: Если общее количество символов (сообщения + избыточного кода) превышает 256.

Примеры использования
---------------

Вот примеры, демонстрирующие использование функций модуля кодирования Рида-Соломона.

1. Пример использования `rs_generator_poly`:

   .. code-block:: python

      from rs_code import rs_generator_poly

      # Вычислить многочлен-генератор для 3 избыточных символов
      red_code_len = 3
      generator_poly = rs_generator_poly(red_code_len)
      print(f"Многочлен-генератор для {red_code_len} избыточных символов: {generator_poly}")

2. Пример использования `rs_encode_msg`:

   .. code-block:: python

      from rs_code import rs_encode_msg

      # Закодировать сообщение с избыточными символами
      input_message = [1, 2, 3, 4]
      red_code_len = 3
      encoded_message = rs_encode_msg(input_message, red_code_len)
      print(f"Закодированное сообщение: {encoded_message}")

