
import os

from openai import OpenAI

client = OpenAI(api_key=os.environ.get("openaiAPI"))

client.fine_tuning.jobs.create(
  training_file="file-6wYNDF6GI8LBO20AEmG9rPqp",
  model="gpt-3.5-turbo"
)
