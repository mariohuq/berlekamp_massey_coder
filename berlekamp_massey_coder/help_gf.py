GENERATOR = 2


def gf_mult(x, y, prim=0, field_charac_full=256):
    # x - левый операнд
    # y - правый операнд
    # prim - примитивный двоичный многочлен
    # возвращает x*y
    res = 0

    while y:
        if y & 1 == 1:
            res = res ^ x
        y = y >> 1  # y // 2
        x = x << 1  # x * 2

        if prim > 0 and x & field_charac_full:  # if x ~ 256 use xor
            x = x ^ prim

    return res


def find_prime_polys(c_exp=8):  # ищет неприводимые полиномы

    root_charac = 2
    field_charac = pow(root_charac, c_exp) - 1  # 255
    field_charac_next = pow(root_charac, c_exp + 1) - 1  # 511

    prim_candidates = []
    irreducible_polynomial = []
    seen = [0] * (field_charac + 1)

    for i in range(field_charac + 2, field_charac_next, root_charac):  # we need the number > 256 to avoid repetitions
        prim_candidates.append(i)  # try every simple polynomial, excluding even ones

    # Здесь реализован подход перебор для нахождения всех этих простых многочленов, путем генерации всех возможных
    # простых многочленов (т.е. каждого целого числа между field_charac + 1 и field_charac * 2), а затем мы строим
    # все поле Галуа, и мы отклоняем простой многочлен-кандидат, если он дублирует хотя бы одно значение или если он
    # генерирует значение выше field_charac(т.е. вызывает переполнение).
    for i in range(len(prim_candidates)):
        prim = prim_candidates[i]

        seen = [0] * (
                    field_charac + 1)  # указывает, было ли значение в поле уже сгенерировано (seen[x] ?== 1) или нет

        conflict = False  # чтобы выяснить, был ли хотя бы 1 конфликт
        x = 1

        for j in range(field_charac):
            x = gf_mult(x, GENERATOR, prim, field_charac + 1)  # вычислите следующее значение в поле

            if x > field_charac or seen[x] == 1:  # если этот номер является дубликатом, то мы отклоняем его
                conflict = True
                break
            else:
                seen[x] = 1 # запомнить это значение, чтобы обнаруживать будущие дубликаты

        if not conflict:  # если конфликта не было, то это простой многочлен
            irreducible_polynomial.append(prim)

    return irreducible_polynomial


def init_tables(prim=285, c_exp=8):  # получим таблицы
    # prim - простой двоичный многочлен
    # c_exp - показатель степени поля Галуа
    field_charac = 2 ** c_exp - 1  # 255

    gf_exp = [0] * (field_charac * 2)
    gf_log = [0] * (field_charac + 1)

    # Для каждого элемента из поля Галуа мы вычисляем логарифм и exp
    x = 1
    for i in range(field_charac):
        gf_exp[i] = x
        gf_log[x] = i
        x = gf_mult(x, GENERATOR, prim, field_charac + 1)

    for i in range(field_charac, field_charac * 2):
        gf_exp[i] = gf_exp[i - field_charac]

    return gf_exp, gf_log
