from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from scraper import scrape_once
import asyncio

@app.get("/refresh")
def refresh_ads():
    try:
        asyncio.run(scrape_once())
        return {"status": "Oglasi osveženi!"}
    except Exception as e:
        return {"error": str(e)}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/oglasi")
def get_ads():
    try:
        if not os.path.exists("oglasi.json"):
            return {"oglasi": []}
        with open("oglasi.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        return {"error": str(e)}
