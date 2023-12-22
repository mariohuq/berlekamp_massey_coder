from . import gf
from . import help_gf


def rs_generator_poly(red_code_len):
    # red_code_len - количество символов, представляющих избыточный код
    # вычисляет многочлен генератора для заданного числа избыточных символов
    g = [1]
    temp = [1, 0]

    for i in range(red_code_len):
        temp[1] = gf.pow(help_gf.GENERATOR, i)
        g = gf.poly_mult(g, temp)

    return g


def rs_encode_msg(msg_in, red_code_len):
    # msg_in - входящее сообщение, представленное вектором многочленов (в данном случае целых чисел)
    # red_code_len - количество символов, представляющих избыточный код
    # возвращаемое закодированное сообщение = вектор [msg_in] + [избыточная информация] (в данном случае целые числа)
    if len(msg_in) + red_code_len >= 256:
        raise ValueError("The total number of characters - messages + redundant code - exceeds 256")

    gen = rs_generator_poly(red_code_len)
    msg_out = list(msg_in) + [0] * red_code_len
    _, remainder = gf.poly_div(msg_out, gen)
    return list(msg_in) + remainder[:red_code_len]
