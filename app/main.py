from dotenv import load_dotenv, find_dotenv; load_dotenv(find_dotenv())
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from bs4 import BeautifulSoup
import requests as req
import notion_client
import openai, os

app = FastAPI()

# Notion APIクライアントの設定
notion = notion_client.Client(auth=os.environ['NOTION_TOKEN'])
database_id = os.environ['DATABSE_ID']

openai_client = openai.Client()

class URLItem(BaseModel):
    url: str

@app.post("/clip")
async def add_page(item: URLItem):
    url = item.url

    # Webページのテキストを取得
    # webpage_text = get_webpage_text(url)
    # if not webpage_text:
    #     raise HTTPException(status_code=404, detail="Web page not found or could not be retrieved")

    # Notionデータベースのプロパティを取得
    # properties = get_database_properties(database_id)

    # LLMを使ってプロパティを生成
    # generated_properties = generate_properties(webpage_text, properties)

    # Notionデータベースにページを追加
    response = create_notion_page(database_id, {
        'URL': {"url": url}
    })
    return response

def get_webpage_text(url: str) -> str:
    response = req.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text()
    return None

def get_database_properties(database_id: str) -> dict:
    response = notion.databases.retrieve(database_id=database_id)
    return response['properties']

def generate_properties(text: str, properties: dict) -> dict:
    prompt = f"以下のテキストに基づいて、次のNotionプロパティに対応する値を生成してください:\n\nテキスト: {text}\n\nプロパティ: {properties}\n\n生成されたプロパティ:"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    generated_properties = response.choices[0].text.strip()
    return eval(generated_properties)  # stringを辞書に変換

def create_notion_page(database_id: str, properties: dict) -> dict:
    new_page = {
        "parent": {"database_id": database_id},
        "properties": properties
    }
    response = notion.pages.create(**new_page)
    return response

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8080)
