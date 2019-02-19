from starlette.applications import Starlette
from starlette.templating import Jinja2Templates
from starlette.requests import Request
import json
import requests_html
import asyncio

templates = Jinja2Templates(directory='templates')

app = Starlette()
session = requests_html.AsyncHTMLSession()
ENDPOINT = "http://52.35.39.131:1337/text-gen/predict"

@app.route('/', methods=["GET", "POST"])
async def homepage(request: Request):
    if request.method == "GET":
        return templates.TemplateResponse('index.html', {'result': ["result will appear here"], "request": request})
    else:
        form = await request.form()
        data = {"input": json.dumps({
            "text": form["text"],
            "num_words": int(form["num_words"]),
            "num_tries": 3
        })}
        resp = await asyncio.ensure_future(session.post(ENDPOINT, json=data))
        text = list(resp.json()['output'].values())

        return templates.TemplateResponse('index.html', {'result': text, "request": request})
        