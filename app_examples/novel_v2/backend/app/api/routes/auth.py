from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str | None = None


# STUB: This is a placeholder for OAuth2 Google integration
# Currently returns 501 Not Implemented - DO NOT USE IN PRODUCTION
@router.post("/google", response_model=AuthResponse)
async def google_auth_placeholder():
    """
    OAuth2 Google authentication stub.

    WARNING: This endpoint is NOT YET IMPLEMENTED and returns 501.
    It exists as a placeholder for future OAuth2 integration.

    DO NOT use in production until properly implemented with real Google OAuth.
    """
    logger.warning("Auth endpoint /auth/google called but not implemented - returning 501")
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Google OAuth2 not implemented yet. Auth is a placeholder.",
    )


@router.get("/callback")
async def auth_callback_placeholder():
    """
    OAuth2 callback endpoint stub.

    WARNING: This endpoint is NOT YET IMPLEMENTED.
    """
    logger.warning("Auth callback endpoint called but not implemented - returning 501")
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="OAuth2 callback not implemented yet",
    )
