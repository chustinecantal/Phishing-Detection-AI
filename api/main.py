from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Phishing Detection API running"}
