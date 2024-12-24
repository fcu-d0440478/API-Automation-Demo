from fastapi import FastAPI
from api.routes.auth import router as auth_router
from api.routes.protected import router as protected_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(protected_router, tags=["protected"])


@app.get("/")
def read_root():
    return {"message": "Welcome to API Automation Demo"}
