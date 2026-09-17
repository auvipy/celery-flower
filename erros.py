from starlette.exceptions import HTTPException
from starlette.requests import Request


async def not_found(request: Request):
    raise HTTPException(status_code=404)
