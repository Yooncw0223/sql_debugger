# csv comes from paper: https://arxiv.org/abs/2304.11015

import csv
import json
import jsonlines
import sqlite3

# with open('DIN-SQL.csv') as f:
#     with jsonlines.open('output.jsonl', mode='w') as writer:
#         reader = csv.reader(f)
#         line_count = 0
#         for line in reader:
#             if line_count > 0:
#                 record = {'messages':[
#                     {'role': 'system', 'content': ''},
#                     {'role': 'user', 'content': f'line[0]'},
#                     {'role': 'assistant', 'content': ''},
#                 ]}
#                 writer.write(json.dumps(record))
#             line_count += 1

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

with open('DIN-SQL.csv') as f:
    reader = csv.reader(f)
    lines = reader

    line_idx = 0
    output_dataset = []
    for line in lines:
        if line_idx > 0:
            is_equivalent = check_equivalence(line[1], line[2], line[3])
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

        line_idx += 1
    with jsonlines.open('output.jsonl', mode='w') as writer:
        writer.write_all(output_dataset)
