from collections import Counter
import re
import sqlite3 as sql
from Correct_func import *
import nltk

conn = sql.connect("data_base1 (1).db")
cursor = conn.cursor()

with open("Corpus_correction.txt", encoding="utf-8") as f:
    big = f.read()


    def main():

        # токенизируем

        def token(text):
            return re.findall(r'[а-я]+', text.lower())

        tokens = token(big)

        word_counter = Counter(tokens)

        total_words = float(sum(word_counter.values()))

        # вероятность появления слова в корпусе - {слово: вероятность}
        word_probas = {word: word_counter[word] / total_words for word in word_counter.keys()}

        # основные функции

        def corrector(word):
            if word in tokens:
                return word

            suggestions = dist1(word) or dist2(word) or [word]
            result_candidates = []

            for word in suggestions:
                cursor.execute("SELECT token FROM tokens WHERE token = ?", (word,))
                conn.commit()
                if cursor.fetchone() is not None:
                    result_candidates.append(word)

            return result_candidates


        def correct_repeat(token):
            for symbol in token:
                pattern = "{3,}"
                pattern2 = r"" + symbol + pattern
                text = re.sub(pattern2, symbol, token)
                cursor.execute("SELECT token FROM tokens WHERE token = ?", (text,))
                conn.commit()
                if cursor.fetchone() is not None:
                    return text

            return None

        bigrams = list(nltk.bigrams(tokens))
        bigram_counter = Counter(bigrams)
        total_bigrams = float(sum(bigram_counter.values()))

        # вероятность появления биграмы в корпусе - {биграма: вероятность}
        bigram_probas = {bigram: bigram_counter[bigram] / total_bigrams for bigram in bigram_counter.keys()}


        # Программа

        user_text = input("""Введите, пожалуйста, текст, а затем нажмите "Enter": """)

        text = token(user_text)

        # инпут юзера распределяется на биграмы
        user_bigrams = list(nltk.bigrams(text))
        bi = [list(i) for i in user_bigrams]



        bigram_dict = {}

        for word in text:
            cursor.execute("SELECT token FROM tokens WHERE token = ?", (word,))
            conn.commit()
            if cursor.fetchone() is None:
                bigram_dict[word] = [corrector(word)]

        for k, v in bigram_dict.items():
            for bigram in bi:
                for word in bigram:
                    if word == k:
                        v.append(bigram)

        left_bigram = {}
        right_bigram = {}
        start_bigram = {}
        end_bigram = {}
        di = {}

        for k, v in bigram_dict.items():
            if len(v) == 3:
                for i in v[0]:
                    left_bigram[i] = []
                    right_bigram[i] = []

            for k2, v2 in left_bigram.items():
                if k2 in v[0]:
                    v2.append(v[1][0])
                    v2.append(k2)
                if tuple(v2) in bigrams:
                    v2.append(bigram_probas[tuple(v2)])

            for k3, v3 in right_bigram.items():
                if k3 in v[0]:
                    v3.append(k3)
                    v3.append(v[2][1])
                if tuple(v3) in bigrams:
                    v3.append(bigram_probas[tuple(v3)])

            for k4, v4 in left_bigram.items():
                for k5, v5 in right_bigram.items():
                    if k4 == k5:
                        if len(v4) == 3 and len(v5) == 3:
                            di[k4] = v4[2] * v5[2]

            if len(v) == 2:
                for i in v[0]:
                    start_bigram[i] = []
                    end_bigram[i] = []

                for k6, v6 in start_bigram.items():
                    if k6 in v[0]:
                        v6.append(k6)
                        v6.append(v[1][1])
                    if tuple(v6) in bigrams:
                        v6.append(bigram_probas[tuple(v6)])
                    if len(v6) == 3:
                        di[k6] = v6[2]

                for k7, v7 in end_bigram.items():
                    if k7 in v[0]:
                        v7.append(k7)
                        v7.append(v[1][0])
                    if tuple(v7) in bigrams:
                        v7.append(bigram_probas[tuple(v7)])
                    if len(v7) == 3:
                        di[k7] = v7[2]


        di2 = {k: v for k, v in sorted(di.items(), key=lambda item: item[1], reverse=True)}

        for k, v in bigram_dict.items():
            v.append({})

        for k, v in di2.items():
            for k2, v2 in bigram_dict.items():
                if len(v2) > 3:
                    if k in v2[0]:
                        v2[3][k] = v
                else:
                    if k in v2[0]:
                        v2[2][k] = v

        for k, v in bigram_dict.items():
            if len(v) == 4:
                print("Ошибка в правописании:", k, "- Возможно вы имели в виду:", list(v[3].keys())[0])
            if len(v) == 3:
                print("Ошибка в правописании:", k, "- Возможно вы имели в виду:", list(v[2].keys())[0])


    while True:
        main()
