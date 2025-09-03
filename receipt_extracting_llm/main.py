from fastapi import FastAPI
from routes import router

app = FastAPI(title="Fiş Okuma API", version="1.0")

# Router ekleme
app.include_router(router)
