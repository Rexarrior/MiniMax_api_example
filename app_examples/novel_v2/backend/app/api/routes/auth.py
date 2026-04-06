from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str | None = None


# STUB: This is a placeholder for OAuth2 Google integration
# Currently returns a mock token without actual Google auth
@router.post("/google", response_model=AuthResponse)
async def google_auth_stub():
    """
    OAuth2 Google authentication stub.
    NOTE: This endpoint is not yet functional.
    """
    return AuthResponse(
        access_token="stub-token-not-valid", token_type="bearer", user_id=None
    )


@router.get("/callback")
async def auth_callback():
    """
    OAuth2 callback endpoint stub.
    NOTE: This endpoint is not yet functional.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="OAuth2 callback not implemented yet",
    )
