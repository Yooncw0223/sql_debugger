# csv comes from paper: https://arxiv.org/abs/2304.11015

import csv
import json
import jsonlines
import sqlite3
import numpy as np
from sklearn.model_selection import train_test_split

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

def build_dataset(train_data):
    output_dataset = []
    for line in train_data:
        output_dataset.append({'messages':[
            {
                "role": "system", 
                "content": "You are helping the user debug their SQL query by returning a JSON, given an English prompt and a sample SQL query. The given query may already be correct."},
            {
                'role': 'user', 
                'content': "How do I express \'" + str(line[0]) + "\' in SQLite? I currently have \'" + str(line[1]) + "\', and if this is correct, please return this query in the format specified below.\
Create a valid JSON that represents the corrected query:\
{\
\"sql_query\": \"The correct SQL query\",\
\"explanation\": \"How you corrected the query\",\
\"correct\": \"Whether the given SQL query is correct\",\
}\
"},
],
})
    return output_dataset

if __name__ == "__main__":
    with open('DIN-SQL.csv') as f:
        all_data = list(csv.reader(f))[1:]
    num_data = len(all_data)
    train, test = train_test_split(all_data, test_size=0.3, random_state=0)
    train_dataset = build_dataset(train)
    with jsonlines.open('train_dataset.jsonl', mode='w') as writer:
        writer.write_all(train_dataset)
    with jsonlines.open('test_dataset.jsonl', mode='w') as writer:
        writer.write_all(test)
