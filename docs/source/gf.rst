gf.py
-----

В файле gf.py реализована алгебрна полей Галуа

* exp_ - список значений экспоненты от элементов поля. exp_[x]= e\:sup:`x`\
* log_ - список значений логарифма от элементов поля. log_[x] = log(x)
* add(x,y) - функция сложения элементов поля Галуа. Побитовый xor.

.. code-block:: python
   :emphasize-lines: 

   def add(x,y):
       return x^y

*sub(x,y) - функция вычитания элементов поля Галуа.

.. code-block:: python
   :emphasize-lines:

   def sub(x,y):
       return x^y

*mult(x,y) - функция умножения элементов поля Галуа.

.. code-block:: python
   :emphasize-lines: 

   def mult(x, y):
    if x == 0 or y == 0:
        return 0
    return exp_[(log_[x] + log_[y]) % 255]

* div(x,y) - функция деления элементов поля Галуа.

.. code-block:: python
   :emphasize-lines:

   def div(x, y):
    if y == 0:
        raise ValueError("y must not be zero")
    if x == 0:
        return 0
    return exp_[(log_[x] - log_[y]) % 255]


* pow(x,y) - функция возведение в степень элементов поля Галуа.

.. code-block:: python
   :emphasize-lines: 

   def pow(x, power):
    i = log_[x]
    i *= power
    i %= 255
    return exp_[i]

* inverse(x,y) - функция инвресии элементов поля Галуа.

.. code-block:: python
   :emphasize-lines: 

    def inverse(x):
        return exp_[255 - log_[x]]
* poly_scale(p,x) - умножение вектора на константу
.. code-block:: python
   :emphasize-lines: 

    def poly_scale(p, x):  
        res = [mult(coeff, x) for coeff in p]
        return res

* poly_add(p,q) -  сложение полиномов.
.. code-block:: python
   :emphasize-lines: 
    def poly_add(p, q):  # сложение полиномов
        res = [0] * max(len(p), len(q))

        for i in range(len(p)):
            res[i + len(res) - len(p)] = p[i]

        for i in range(len(q)):
            res[i + len(res) - len(q)] = add(res[i + len(res) - len(q)], q[i])

        return res

* poly_mult(p,q) - умножение полиномов.
.. code-block:: python
   :emphasize-lines: 
    def poly_mult(p, q):
        res = [0] * (len(p) + len(q) - 1)

        for j in range(len(q)):
            for i in range(len(p)):
                res[i + j] = add(res[i + j], mult(p[i], q[j]))

        return res

* poly_div(dividend, divisor) -  деление полиномов. quotient - целая часть, remainder - остаток
.. code-block:: python
   :emphasize-lines: 

    def poly_div(dividend, divisor):
        remainder = dividend.copy()

        for i in range(len(dividend) - (len(divisor) - 1)):
            coef = remainder[i]
            if coef != 0:
                for j in range(1, len(divisor)):
                    if divisor[j] != 0:
                        remainder[i + j] = sub(remainder[i + j], mult(divisor[j], coef))

        quotient = remainder[:len(dividend) - (len(divisor) - 1)]
        remainder = remainder[len(dividend) - (len(divisor) - 1):]

        return quotient, remainder


Пример входных данных
----------------------
dividend = [1, 0, 1, 1, 0, 0, 0, 0]  # пример полинома-делимого
divisor = [1, 1, 1]  # пример полинома-делителя

#. Вызов функции
quotient, remainder = gf.poly_div(dividend, divisor)

#. Вывод результатов
print("Частное:", quotient)
print("Остаток:", remainder)'''


* poly_eval(poly,x)- 
.. code-block:: python
   :emphasize-lines: 
    def poly_eval(poly, x):
        y = poly[0]
        for i in range(1, len(poly)):
            y = add(mult(y, x), poly[i])
        return y






