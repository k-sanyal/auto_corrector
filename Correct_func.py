def dist0(word):
    return {word}


def dist1(word):
    # Разбиваем слово на всевозможные части (левая - правая)
    pairs = [(word[:i], word[i:]) for i in range(len(word) + 1)]

    # переставляем последнюю букву левой части с первой буквой правой части
    transposition = []
    for half1, half2 in pairs:
        if len(half1) == 1:
            transposition.append(half2[0] + half1[0] + half2[1:])
        if len(half1) > 1 and len(half2) != 0:
            transposition.append(half1[0:-1] + half2[0] + half1[-1] + half2[1:])

    # левая часть + правая часть без 1 буквы
    deletion = []
    for half1, half2 in pairs:
        if len(half2) != 0:
            deletion.append(half1 + half2[1:])

    # заменяем первую букву правой части на каждую букву алфавита
    replacement = []
    alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    for half1, half2 in pairs:
        for letter in alphabet:
            if len(half2) != 0:
                replacement.append(half1 + letter + half2[1:])

    # вставляем букву из алфавита между левой и правой частью
    insertion = []
    for half1, half2 in pairs:
        for letter in alphabet:
            insertion.append(half1 + letter + half2)

    return set(transposition + deletion + replacement + insertion)


# дублируем функцию на расстояние=1
def dist2(word):
    return set(b for a in dist1(word) for b in dist1(a))






