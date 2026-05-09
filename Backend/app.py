from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "NeuroGuide API running"}

@app.on_event("startup")
async def startup_event():
    try:
        from routes import router
        app.include_router(router)
        print("Routes loaded successfully!")
    except Exception as e:
        print(f"Error loading routes: {e}")