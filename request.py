
import os

from openai import OpenAI

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

response = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    response_format={ "type": "json_object" },
    messages = [{"role": "system", "content": "You are helping the user debug their SQL query by returning a JSON, given an English prompt and a sample SQL query. The given query may already be correct."}, {"role": "user", "content": "How do I express 'How many singers do we have?' in SQLite? I currently have 'SELECT COUNT(*) FROM singer', and if this is correct, please return this query in the format specified below.Create a valid JSON that represents the corrected query:{\"sql_query\": \"The correct SQL query\",\"explanation\": \"How you corrected the query\",\"correct\": \"Whether the given SQL query is correct\",}"}],
)

print(response.choices[0].message.content)
