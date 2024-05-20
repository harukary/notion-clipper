from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, AnyUrl
# import requests
from bs4 import BeautifulSoup
import openai, os

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
NOTION_TOKEN = os.environ['NOTION_TOKEN']
CLIP_DB_ID = os.environ['CLIP_DB_ID']

app = FastAPI()

class UrlPayload(BaseModel):
    url: AnyUrl

client = openai.Client()

@app.get("/")
def read_root():
    response = client.chat.completions.create(
        messages=[{'role':'user', 'content':'Hi.'}],
        model='gpt-3.5-turbo'
    )
    return {
        "Hello": "World",
        "OpenAI": response.choices[0].message.content
    }
