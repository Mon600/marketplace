from fastapi import Request, FastAPI

from fastapi import HTTPException


class CookieBearer:
    def __init__(self, token_type: str = 'users_access_token'):
        self.token_type = token_type


    async def __call__(self, request: Request):
        token = request.cookies.get(self.token_type)
        if not token:
            raise HTTPException(
                status_code=401,
                detail="Not authenticated",
            )
        return token