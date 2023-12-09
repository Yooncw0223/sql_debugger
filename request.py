
import os

from openai import OpenAI
import jsonlines
import json
from evaluate import check_equivalence

client = OpenAI(api_key=os.environ.get("openaiAPI"))

# response = client.chat.completions.create(
#     model="gpt-3.5-turbo-1106",
#     response_format={ "type": "json_object" },
#     messages = [
#         {
#             "role": "system", 
#             "content": "You are helping the user debug their SQL query by returning a JSON, given an English prompt and a sample SQL query. The given query may already be correct."}, 
#         {
#             "role": "user", 
#             "content": "How do I express 'What is the average miles per gallon(mpg) of the cars with 4 cylinders?' in SQLite? I currently have 'SELECT AVG(MPG) FROM cars_data WHERE Cylinders = 4', and if this is correct, please return this query in the format specified below.\
# Create a valid JSON that represents the corrected query:\
# {\
# \"sql_query\": \"The correct SQL query\",\
# \"explanation\": \"How you corrected the query\",\
# \"correct\": \"Whether the given SQL query is correct\",\
# }\
# "},
#     ],
# )
#
# num_correct = 0
# num_total = 0
# with jsonlines.open('test_dataset.jsonl') as reader:
#     count = 0
#     for obj in list(reader)[:10]:
#         response = client.chat.completions.create(
#             model="gpt-3.5-turbo-1106",
#             response_format={ "type": "json_object" },
#             messages = obj['messages'],
#         )
#         responseJSONInStr = response.choices[0].message.content
#         messages = json.loads(responseJSONInStr)
#         num_total += 1
#
#         gold = obj['gold']
#         db = obj['database']
#
#         if check_equivalence(messages['sql_query'], gold, db):
#             num_correct += 1
#         print(count)
#         count += 1
#
#     print("correct: ", num_correct)
#     print("total: ", num_total)
#     print("Accuracy: ", num_correct / num_total)
#     

from gpt_interface import *
import csv
# response = client.chat.completions.create(
#     model="gpt-3.5-turbo-1106",
#     response_format={ "type": "json_object" },
#     messages = [],
# )



# response = get_gpt_response([{"role": "system", "content": "You are helping the user debug their SQL query by returning a JSON, given an English prompt and a sample SQL query. The given query may already be correct."}, {"role": "user", "content": "How do I express 'How many singers do we have?' in SQLite? I currently have 'SELECT COUNT(*) FROM singer', and if this is correct, please return this query in the format specified below.Create a valid JSON that represents the corrected query:{\"sql_query\": \"The correct SQL query\",\"explanation\": \"How you corrected the query\",\"correct\": \"Whether the given SQL query is correct\",}"}])
#

# print(response)
# print(type(response))



from build_train_test import Approach3


index = 500
with open('DIN-SQL.csv') as f:
    all_data = list(csv.reader(f))[1:]
prompt, predicted, gold, db = all_data[index]


print(Approach3.conversation(prompt, predicted, db))




