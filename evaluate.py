import sqlite3

def evaluate_query(query, database):
    con = sqlite3.connect(f"spider/database/{database}/{database}.sqlite")
    con.text_factory = lambda b: b.decode(errors = 'ignore')
    cur = con.cursor()
    try:
        cur.execute(query)
        res = cur.fetchall()
    except sqlite3.OperationalError as error:
        res = error
    con.close()
    return res


def check_equivalence(predicted, gold, database, return_sql_outputs=False):
    predicted_res = evaluate_query(predicted, database)
    gold_res = evaluate_query(gold, database)
    if isinstance(gold_res, sqlite3.OperationalError):
        raise(gold_res)
    is_equivalent = predicted_res == gold_res
    if return_sql_outputs:
        return is_equivalent, predicted_res, gold_res
    else:
        return is_equivalent


