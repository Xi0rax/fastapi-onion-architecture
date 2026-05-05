from datetime import datetime, timedelta, UTC

import jwt

from auth.src.config import settings


def create_access_token(user_id: str) -> str:
    payload = {
        "sub": user_id,
        "exp": datetime.now(UTC) + timedelta(hours=24),
    }

    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")