import sqlite3

def check_equivalence(predicted, gold, database):
    con = sqlite3.connect(f"spider/database/{database}/{database}.sqlite")
    con.text_factory = bytes
    cur = con.cursor()
    try:
        cur.execute(predicted)
        predicted_res = cur.fetchall()
    except sqlite3.OperationalError:
        predicted_res = None
    cur.execute(gold)
    gold_res = cur.fetchall()
    con.close()

    is_equivalent = predicted_res == gold_res
    return is_equivalent


