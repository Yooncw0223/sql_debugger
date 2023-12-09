
import os

from openai import OpenAI
import jsonlines
import json

from evaluate import evaluate_query
client = OpenAI(api_key=os.environ.get("openaiAPI"))


def get_user_content_initial(prompt, predicted):
    return "How do I express \'" + str(prompt) + "\' in SQLite? \
I currently have \'" + str(predicted) + "\'. \
If you'd like, I can also run any SQL query against the database for you. \
Create a valid JSON: \
{\
\"sql_query\": \"The correct SQL query\", \
\"sql_query_to_run\": \"A SQL query for the user to run. Leave as empty string if no extra information about database is needed.\"\
}\
"
def get_user_content_runSQL(sql_query_to_run, database):
    return evaluate_query(sql_query_to_run, database)

def get_system_content():
    return "You are helping the user debug their SQL query by returning a JSON, \
given an English prompt, and a sample SQL query. \
The given query may already be correct. \
You may ask the user to run a SQL query for you to learn more about the database. \
"

def get_gpt_response(message, model_name):
    # dummy function. eventually, link this up to gpt, and delete this.
    response = client.chat.completions.create(
        model=model_name,
        response_format={ "type": "json_object" },
        messages = [{"role": "system", "content": get_system_content()}, {"role": "user", "content": message}],
    )
    result = response.choices[0].message.content
    return json.loads(result if result else "{}");



