# openai-playground

## Prerequirement

- [poetry](https://python-poetry.org/)

## Quickstart

1. `poetry install` install package
2. setup OpenAI key and endpoint:
   - Windows: `$env:AZURE_OPENAI_ENDPOINT="https://<YOUR_AZURE_OPENAI_NAME>.openai.azure.com/"` `$env:AZURE_OPENAI_API_KEY="<YOUR_API_KEY>"`
   - Linux: `export AZURE_OPENAI_ENDPOINT="https://<YOUR_AZURE_OPENAI_NAME>.openai.azure.com/"` `export AZURE_OPENAI_API_KEY="<YOUR_API_KEY>"`
3. `poetry shell` and then run your script.
