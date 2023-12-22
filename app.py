from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles

# Import the scrape_reviews and summarize_reviews functions from your summarize.py file
from summarize import scrape_reviews, summarize

import google.generativeai as palm
import config

app = FastAPI()


palm.configure(api_key=config.API_KEY)
models = [
    m for m in palm.list_models() if "generateText" in m.supported_generation_methods
]
model = models[0].name

@app.post("/scrape-and-summarize/")
async def scrape_and_summarize(request: Request):
    data = await request.json()
    url = data.get("url")
    if not url:
        raise HTTPException(status_code=422, detail="URL is required")
    try:
        reviews = await scrape_reviews(url)
        summary = summarize(reviews, model)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app.mount("/", StaticFiles(directory=".", html=True), name="static")