from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Mood Food FastAPI Server"}