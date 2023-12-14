import sqlite3

def evaluate_query(query, database):
    con = sqlite3.connect(f"spider/database/{database}/{database}.sqlite")
    con.text_factory = lambda b: b.decode(errors = 'ignore')
    cur = con.cursor()
    try:
        cur.execute(query)
        res = cur.fetchall()
        res = [set(res_tuple) for res_tuple in res]
    except sqlite3.OperationalError as error:
        res = error
    con.close()
    return res


from evaluation import *

def check_equivalence(predicted, gold, database, return_sql_outputs=False):
    goldFile = "gold.txt"
    predictedFile = "predicted.txt"
    
    with open(goldFile, "w") as f:
        f.write(gold + "\t" + database)

    with open(predictedFile, "w") as f:
        f.write(predicted + "\t" + database)
    
    db_dir = f"spider/database/"

    predicted_res = evaluate_query(predicted, database)
    gold_res = evaluate_query(gold, database)
    if isinstance(gold_res, sqlite3.OperationalError):
        raise(gold_res)
    is_equivalent = bool(evaluate1(goldFile, predictedFile, db_dir))
    if return_sql_outputs:
        return is_equivalent, predicted_res, gold_res
    else:
        return is_equivalent


# some models (fine-tuned ones due to API) cannot return in json format
def check_equivalence_single(predicted, gold, database, return_sql_outputs=False):
    goldFile = "gold.txt"
    predictedFile = "predicted.txt"
    
    with open(goldFile, "w") as f:
        f.write(gold + "\t" + database)

    with open(predictedFile, "w") as f:
        f.write(predicted + "\t" + database)
    
    db_dir = f"spider/database/"

    predicted_res = evaluate_query(predicted, database)
    gold_res = evaluate_query(gold, database)
    if isinstance(gold_res, sqlite3.OperationalError):
        raise(gold_res)
    is_equivalent = bool(evaluate1(goldFile, predictedFile, db_dir))
    if return_sql_outputs:
        return is_equivalent, predicted_res, gold_res
    else:
        return is_equivalent



