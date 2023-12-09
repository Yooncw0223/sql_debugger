
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

def get_gpt_response(messages, model_name="gpt-3.5-turbo-1106"):
    # dummy function. eventually, link this up to gpt, and delete this.
    response = client.chat.completions.create(
        model=model_name,
        response_format={ "type": "json_object" },
        messages = messages,
    )
    result = response.choices[0].message.content
    return json.loads(result if result else "{}");


# filename must be from openai portal
def fine_tune_model(train_dataset_filename: str, model_to_finetune = "gpt-3.5-turbo-1106"):
    client.fine_tuning.jobs.create(
        training_file=train_dataset_filename,
        model=model_to_finetune
    )

# physical file's name
def create_dataset_file(dataset_filename):
    client.files.create(
        file=open(dataset_filename, "rb"),
        purpose="fine-tune"
    )
