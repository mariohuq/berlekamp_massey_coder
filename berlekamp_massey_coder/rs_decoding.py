from . import gf
from . import help_gf
from .gf import Polynomial


def rs_calc_syndromes(msg, red_code_len):  # вычисляет синдромы ошибок
    #  msg - входящее сообщение, представленное вектором многочленов (целых чисел)
    # red_code_len - количество символов, представляющих избыточный код
    synd = [0] * (red_code_len + 1)

    for i in range(1, red_code_len + 1):
        temp = gf.pow(help_gf.GENERATOR, i - 1)
        synd[i] = gf.poly_eval(msg, temp)

    return synd


def rs_find_errarta_locator(err_pos):
    # err_pos - вектор с позициями ошибочных символов
    # возвращает многочлен локатора ошибок

    # находит локаторы ошибок
    e_loc = Polynomial([1])

    for pos in err_pos:
        # since we know location of the error, we can find L(x) as
        # L(x) = \prod (1 + x*alpha^(i))

        e_loc *= Polynomial([gf.pow(help_gf.GENERATOR, pos), 1])

    return e_loc


def rs_find_error_evaluator(synd, err_loc, err_loc_size):
    # synd - многочлен синдромов ошибок (вектор int)
    # err_loc - многочлен локатора ошибок L(x)
    # err_loc_size - размер L(x)
    poly_mul = Polynomial(synd) * err_loc
    remainder = poly_mul.coefficients[-err_loc_size:]
    return Polynomial(remainder)


def rs_correct_errata(msg_in, synd, err_pos):
    coef_pos = [len(msg_in) - 1 - pos for pos in err_pos]

    # находит многочлен локатора ошибки L(x) в соответствии с известным местоположением ошибки
    err_loc = rs_find_errarta_locator(coef_pos)

    # находит полиномиал ошибки W(x)
    synd.reverse()
    err_eval = rs_find_error_evaluator(synd, err_loc, len(err_loc))


    # x - сохранит положение ошибок
    # нам нужно получить многочлен определения местоположения ошибки X из позиций ошибок в err_pos
    # (корни многочлена определения местоположения ошибки, т.е. где он равен 0)
    x = [gf.pow(help_gf.GENERATOR, -(255 - pos)) for pos in coef_pos]

    E = [0] * len(msg_in)  # сохранит значения, которые необходимо исправить в исходном сообщении с ошибками

    for i in range(len(x)):
        x_i_inv = gf.inverse(x[i])

        # Находит формальную производную полинома локатора ошибок
        # формальная производная от локатора ошибок используется в качестве знаменателя алгоритма Форни,
        # который говорит, что i-е значение ошибки задается error_evaluator(gf.inverse(Xi)) / error_locator_derivative(gf.inverse(Xi)).
        err_loc_prime_tmp = [gf.sub(1, gf.mult(x_i_inv, x[j])) for j in range(len(x)) if j != i]

        # многочлен ошибки Yi = W(Xi ^(-1))/L'(Xi ^(-1))
        # вычисляет произведение, которое является знаменателем алгоритма Форни (производная от локатора ошибок)
        err_loc_prime = 1
        for coef in err_loc_prime_tmp:
            err_loc_prime = gf.mult(err_loc_prime, coef)

        err_loc_prime_tmp.clear()

        y = gf.poly_eval(err_eval, x_i_inv)  # numerator
        y = gf.mult(gf.pow(x[i], 1), y)

        if err_loc_prime == 0:  # divisor should not be 0
            raise ValueError("Could not find error magnitude")

        magnitude = gf.div(y, err_loc_prime)   # Значение погрешности, вычисленное алгоритмом Форни
        # Деление оценки погрешности на производную от локатора ошибок
        E[err_pos[i]] = magnitude  # возвращает нам значение ошибки, то есть значение для восстановления символа

    msg_in += Polynomial(E)  # C(x) = C'(x) + E(x) (xor)
    return msg_in


def rs_find_error_locator(synd, red_code_len):
    # synd - многочлен синдромов ошибок (вектор int)
    # red_code_len - количество символов, представляющих избыточный код
    # возвращает многочлен локатора ошибок L(x)
    err_loc = Polynomial([1])  # многочлен определения ошибки C(x)
    old_loc = Polynomial([1])  # многочлен локатора ошибок предыдущей итерации

    synd_shift = len(synd) - red_code_len

    # Алгоритм Берлекампа–Мэсси является альтернативой декодеру Рида–Соломона Питерсона для решения набора линейных уравнений.
    # Основная идея заключается в том, что алгоритм итеративно оценивает полином локатора ошибок. Для этого он вычисляет дельта-расхождение,
    # по которому мы можем определить, нужно ли нам обновлять локатор ошибок или нет
    for i in range(red_code_len):
        k = i + synd_shift

        # вычисление дельты расхождения
        delta = synd[k]

        for j in range(1, len(err_loc)):
            delta ^= gf.mult(err_loc.coefficients[len(err_loc) - 1 - j], synd[k - j])  # delta = Sn + C1*Sn-1 +..+ Cj*Sk-j

        # сдвигаем многочлены, чтобы вычислить следующую степень
        old_loc.coefficients.append(0)

        if delta != 0:  # if дельта == 0, алгоритм предполагает, что C(x) и L верны на данный момент, и продолжает
            if len(old_loc) > len(err_loc):  # ~2*L <= k + erase_count
                # Вычисление полиномиальной сигмы локатора ошибок
                new_loc = gf.poly_scale(old_loc, delta)
                old_loc = gf.poly_scale(err_loc, gf.inverse(delta))
                err_loc = new_loc

            # Обновление с учетом несоответствия
            err_loc += gf.poly_scale(old_loc, delta)

    while len(err_loc) and err_loc.coefficients[0] == 0:
        err_loc.coefficients.pop(0)

    errs = len(err_loc) - 1
    if errs * 2 > red_code_len:
        raise ValueError("Too many errors to correct")

    return err_loc


def rs_find_errors(err_loc, message_len):
    # err_loc - многочлен локатора ошибок L(x)
    # nmess - размер сообщения
    # возвращает вектор индекса символов, которые необходимо исправить
    err_pos = []

    errs = len(err_loc) - 1
    for i in range(message_len):
        if gf.poly_eval(err_loc, gf.pow(help_gf.GENERATOR, i)) == 0:
            err_pos.append(message_len - 1 - i)

    if len(err_pos) != errs:
        raise ValueError("Too many (or few) errors found for the errata locator polynomial!")

    return err_pos


def rs_decode_msg(msg_in, red_code_len):
    # msg_in - вектор закодированного сообщения
    # red_code_len - количество символов, представляющих избыточный код
    # erase_pos - позиции известных ошибок
    # возвращает декодированное сообщение
    if len(msg_in) > 255:
        raise ValueError("Message is too long")

    msg_out = Polynomial(msg_in)

    # чтобы мы не подсчитывали многочлен генератора несколько раз и не делили,
    # мы сразу подсчитываем многочлен синдрома ошибки, и если в нем нет хотя бы
    # одного значения, отличного от 0, то сообщение не искажается
    synd = rs_calc_syndromes(msg_out, red_code_len)
    max_val = max(synd)

    if max_val == 0:
        return msg_out

    # Найдите многочлен локатора ошибок L(x)
    err_loc = rs_find_error_locator(synd, red_code_len)

    err_loc.coefficients.reverse()

    # Найдите вектор индекса символов, которые необходимо исправить
    err_pos = rs_find_errors(err_loc, len(msg_out))

    if not err_pos:
        raise ValueError("Could not locate error")

    # Найдет значения ошибок и примените их для исправления сообщения
    # Вычислим средство оценки ошибок и полиномы величины ошибок, затем исправим ошибки
    msg_out = rs_correct_errata(msg_out, synd, err_pos)

    # Подсчитаем  многочлен синдрома ошибки, и если в нем нет хотя бы
    # одного значения, отличного от 0, то сообщение успешно декодировано
    synd = rs_calc_syndromes(msg_out, red_code_len)
    max_synd = max(synd)
    if max_synd > 0:
        raise ValueError("Could not correct message")
    return msg_out.coefficients
