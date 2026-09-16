from starlette.requests import Request
from starlette.responses import Response


class FlowerCORSMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive=receive)

        flower = request.app.state.flower
        options = flower.options

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                headers = list(message.get("headers", []))

                if not (
                    options.basic_auth
                    or options.auth
                ):
                    headers.extend([
                        (
                            b"access-control-allow-origin",
                            b"*",
                        ),
                        (
                            b"access-control-allow-headers",
                            (
                                b"x-requested-with,"
                                b"access-control-allow-origin,"
                                b"authorization,"
                                b"content-type"
                            ),
                        ),
                        (
                            b"access-control-allow-methods",
                            (
                                b"PUT, DELETE, OPTIONS, "
                                b"POST, GET, PATCH"
                            ),
                        ),
                    ])

                message["headers"] = headers

            await send(message)

        if request.method == "OPTIONS":
            response = Response(status_code=204)
            await response(scope, receive, send_wrapper)
            return

        await self.app(scope, receive, send_wrapper)
