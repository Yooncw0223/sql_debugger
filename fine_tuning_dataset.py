
import os

from openai import OpenAI

client = OpenAI(api_key=os.environ.get("openaiAPI"))

client.files.create(
  file=open("train_dataset.jsonl", "rb"),
  purpose="fine-tune"
)

print("Just created the data file; proceed with fine-tuning\n")




