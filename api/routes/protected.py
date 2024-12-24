from fastapi import APIRouter, Depends
from api.routes.auth import get_current_user

router = APIRouter()


@router.get("/protected")
def read_protected_data(current_user: dict = Depends(get_current_user)):
    return {"message": f"Hello, {current_user['email']}!"}
