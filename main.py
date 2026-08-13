from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Tote and Trend API is running"}