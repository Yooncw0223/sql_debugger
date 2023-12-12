
import os

from openai import OpenAI

client = OpenAI(api_key=os.environ.get("openaiAPI"))

client.fine_tuning.jobs.create(
  # training_file="file-7emHlOyaQFFFNByMrbtJRr9M",
  training_file="file-H0EbmsfonulTsCAZMG1IxZZO",
  model="gpt-3.5-turbo"
)
