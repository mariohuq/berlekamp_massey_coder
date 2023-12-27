Модуль RS Decode
=================

.. module:: rs_decode
   :platform: Unix, Windows
   :synopsis: Модуль для операций декодирования Рида-Соломона.



Введение
------------

Этот модуль предоставляет функции для операций декодирования Рида-Соломона.

Функции
---------

.. autofunction:: rs_calc_syndromes

.. autofunction:: rs_find_errarta_locator

.. autofunction:: rs_find_error_evaluator

.. autofunction:: rs_correct_errata

.. autofunction:: rs_find_error_locator

.. autofunction:: rs_find_errors

.. autofunction:: rs_decode_msg

Подробности функций
----------------

.. autofunction:: rs_calc_syndromes

   Эта функция вычисляет синдромы ошибок для данного сообщения.

   :param msg: Входное сообщение, представленное вектором многочленов (целых чисел).
   :type msg: list
   :param red_code_len: Количество символов, представляющих избыточный код.
   :type red_code_len: int
   :return: Синдромы ошибок.
   :rtype: list

.. autofunction:: rs_find_errarta_locator

   Эта функция находит многочлен-локатор ошибок.

   :param err_pos: Вектор с позициями ошибочных символов.
   :type err_pos: list
   :return: Многочлен-локатор ошибок.
   :rtype: list

.. autofunction:: rs_find_error_evaluator

   Эта функция находит многочлен-оценщик ошибок.

   :param synd: Многочлен синдромов ошибок (вектор целых чисел).
   :param err_loc: Многочлен-локатор ошибок L(x).
   :param err_loc_size: Размер L(x).
   :return: Многочлен-оценщик ошибок.
   :rtype: list

.. autofunction:: rs_correct_errata

   Эта функция исправляет ошибки во входном сообщении.

   :param msg_in: Входное сообщение.
   :type msg_in: list
   :param synd: Многочлен синдромов ошибок (вектор целых чисел).
   :param err_pos: Позиции ошибок.
   :type err_pos: list
   :return: Исправленное сообщение.
   :rtype: list

.. autofunction:: rs_find_error_locator

   Эта функция находит многочлен-локатор ошибок.

   :param synd: Многочлен синдромов ошибок (вектор целых чисел).
   :param red_code_len: Количество символов, представляющих избыточный код.
   :return: Многочлен-локатор ошибок L(x).
   :rtype: list

.. autofunction:: rs_find_errors

   Эта функция находит позиции ошибок в сообщении.

   :param err_loc: Многочлен-локатор ошибок L(x).
   :param message_len: Размер сообщения.
   :return: Позиции ошибок.
   :rtype: list

.. autofunction:: rs_decode_msg

   Эта функция декодирует входное сообщение.

   :param msg_in: Входное сообщение.
   :type msg_in: list
   :param red_code_len: Количество символов, представляющих избыточный код.
   :return: Декодированное сообщение.
   :rtype: list

Примеры использования
---------------

Вот примеры, демонстрирующие использование функций в модуле декодирования Рида-Соломона.

1. Пример использования `rs_decode_msg`:

   .. code-block:: python

      from rs_decode import rs_decode_msg

      # Декодировать сообщение с избыточными символами
      input_message = [1, 2, 3, 4]
      red_code_len = 3
      decoded_message = rs_decode_msg(input_message, red_code_len)
      print(f"Декодированное сообщение: {decoded_message}")