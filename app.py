from starlette.applications import Starlette

from .routers import routes


app = Starlette(routes=routes)
