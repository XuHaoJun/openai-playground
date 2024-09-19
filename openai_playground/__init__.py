import os
import argparse
from openai import AzureOpenAI

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
  api_version="2024-02-01"
)

def create_prompt(text):
  """ Create input prompt for the language model
  Args:
    text (str): A text to classify
  Returns:
    prompt for text to classify
  """
  instructions = 'Is the underlying sentiment positive or negative?'
  formatting = '"Positive" or "Negative"'
  return f'Text:{text}\n{instructions}\nAnswer:{formatting}\n'

def call_llm(prompt):
  """ Call the language model
  Args:
    prompt (str): A prompt for the language model
  Returns:
    The response from the language model
  """
  messages = [
    {'content': prompt, 'role': 'user'}
  ]
  response = client.chat.completions.create(model='gpt-4o', messages=messages)
  return response

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('text', type=str, help='A text go classify')
  args = parser.parse_args()

  print(args.text)
  prompt = create_prompt(args.text)
  answer = call_llm(prompt)
  print(answer)