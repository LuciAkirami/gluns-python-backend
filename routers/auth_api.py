from fastapi import APIRouter, HTTPException
from ..utils.http_utils import login_keycloak

router = APIRouter()

@router.post("/login")
async def login(username: str, password: str):
    """Handle login using Keycloak."""
    try:
        data = login_keycloak(username, password)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error during login")
