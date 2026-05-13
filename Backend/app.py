from fastapi import FastAPI
from routes import router
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://quiet-bubblegum-f0f176.netlify.app",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)

@app.get("/")
def home():
    return {"message": "NeuroGuide API running"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
