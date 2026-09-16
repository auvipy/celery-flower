import logging

from starlette.exceptions import HTTPException
from starlette.requests import Request

from ..utils.broker import Broker

from . import (
    get_flower_app,
    get_active_queue_names,
    render_template,
    require_authentication,
)

logger = logging.getLogger(__name__)


async def broker(request: Request):
    require_authentication(request)

    app = get_flower_app(request)

    http_api = None

    if (
        app.transport == "amqp"
        and app.options.broker_api
    ):
        http_api = app.options.broker_api

    try:
        broker = Broker(
            app.broker_uri_with_password,
            http_api=http_api,
            broker_options=(
                app.capp.conf
                .broker_transport_options
            ),
            broker_use_ssl=(
                app.capp.conf.broker_use_ssl
            ),
        )
    except NotImplementedError as exc:
        raise HTTPException(
            status_code=404,
            detail=(
                f"'{app.transport}' "
                "broker is not supported"
            ),
        ) from exc

    try:
        queues = await broker.queues(
            get_active_queue_names(request)
        )
    except Exception as exc:
        queues = []
        logger.error(
            "Unable to get queues: '%s'",
            exc,
        )

    return render_template(
        request,
        "broker.html",
        broker_url=app.broker_uri,
        queues=queues,
    )
