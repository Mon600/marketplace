from fastapi import Request, FastAPI

from fastapi import HTTPException


class CookieBearer:
    def __init__(self, token_type: str = 'users_access_token'):
        self.token_type = token_type


    async def __call__(self, request: Request):
        refesh_token = request.cookies.get('users_refresh_token')
        access_token = request.cookies.get('users_access_token')
        if not refesh_token:
            raise HTTPException(
                status_code=401,
                detail="Not authenticated",
            )
        if not access_token:
            return {'refresh_token': refesh_token}
        return {"access_token": access_token, "refresh_token": refesh_token}