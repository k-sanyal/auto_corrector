import sqlite3 as sql
import re


def token(text):
    return re.findall(r'[а-я]+', text.lower())

with open("Corpus_correction.txt", encoding="utf-8") as f:
    big_db = f.read()

    tokens_db = token(big_db)
    vocabulary = set(tokens_db)

conn = sql.connect("data2.db")
curs = conn.cursor()

for i in vocabulary:
    try:
        query = "INSERT INTO tokens VALUES (?)"
        curs.execute(query, (i,))
        conn.commit()
    except Exception:
        pass

