import os
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

bearer = HTTPBearer()


def require_auth(credentials: HTTPAuthorizationCredentials = Security(bearer)):
    if credentials.credentials != os.getenv("API_SECRET_TOKEN"):
        raise HTTPException(status_code=401, detail="Unauthorized")
