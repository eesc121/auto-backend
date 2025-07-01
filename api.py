from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json
import os

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

@app.post("/upload")
async def upload_ads(request: Request):
    try:
        data = await request.json()
        with open("oglasi.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return {"status": "Uspešno ažurirano"}
    except Exception as e:
        return {"error": str(e)}
