import os
import argparse
from openai import AzureOpenAI
import tiktoken

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
  api_key=os.getenv("AZURE_OPENAI_API_KEY"),
  api_version="2024-02-01"
)

def create_prompt(question):
  parts = []
  parts.append('Mongodb Pokemon Collection Sample Data:')
  # parts.append("here's the data linke: https://raw.githubusercontent.com/XuHaoJun/openai-playground/refs/heads/main/data/pokedex.json")
  parts.append('```json')
  with open('data/pokedex.json', 'r', encoding='utf-8') as file:
    text = file.read()
    print(text)
    parts.append(text)
  parts.append('```')
  parts.append('Translate this question into Mongodb Query:')
  parts.append(question)
  return '\n'.join(parts)

def call_llm(prompt):
  messages = [
    {'content': prompt, 'role': 'user'}
  ]
  reply = client.chat.completions.create(model='gpt-4o', messages=messages)
  return reply.choices[0].message.content


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('question', type=str, help='Question to translate')
  args = parser.parse_args()
  prompt = create_prompt(args.question)
  print('prompt tokens:', len(tiktoken.encoding_for_model('gpt-4o').encode(prompt)))
  answer = call_llm(prompt)
  print(answer)