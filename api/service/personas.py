from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json

app = FastAPI()

@app.get("/personas")
async def get_personas():
    with open("ai_paralegal_ssot/personas.json") as f:
        personas = json.load(f)
    return JSONResponse(content=personas)
