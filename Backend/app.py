from fastapi import FastAPI
from routes import router
from fastapi.middleware.cors import CORSMiddleware
#uvicorn app:app --reload 
# cd frontendC python3 -m http.server 5500 
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def home():
    return {"message": "NeuroGuide API running"}