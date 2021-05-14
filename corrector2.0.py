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
            result_candidates = {}

            for word in suggestions:
                cursor.execute("SELECT token FROM tokens WHERE token = ?", (word,))
                conn.commit()
                if cursor.fetchone() is not None:
                    result_candidates[word] = word_probas[word]

            result_candidates2 = {k: v for k, v in sorted(result_candidates.items(), key=lambda item: item[1], reverse=True)}

            return result_candidates2


        def correct_repeat(token):
            for symbol in token:
                pattern = "{3,}"
                pattern2 = r"" + symbol + pattern
                text = re.sub(pattern2, symbol, token)
                cursor.execute("SELECT token FROM tokens WHERE token = ?", (text,))
                conn.commit()
                if cursor.fetchone() is not None:
                    return text
                else:
                    return corrector(text)

            return None



        # Программа

        user_text = input("""Введите, пожалуйста, текст, а затем нажмите "Enter": """)

        need_to_correct = token(user_text)

        correction_dictionary = {}
        for word in need_to_correct:
            correction_dictionary[word] = [corrector(word)]


        for k, v in correction_dictionary.items():
            new_dict = {}
            non_repeated = correct_repeat(k)
            if non_repeated is not None:
                if type(non_repeated) != dict:
                    new_dict[non_repeated] = word_probas[non_repeated]
                    v.append(new_dict)
                else:
                    v.append(non_repeated)
            for i in v:
                if type(i) == dict:
                    if len(i) == 0:
                        v.remove(i)
            if len(v) > 1:
                v.remove(v[1])

        for k, v in correction_dictionary.items():
            if k not in tokens:
                for i in v:
                    print("Ошибка в правописании:", k, "- Возможно вы имели в виду:", list(v[0].keys()))



    while True:
        main()



















