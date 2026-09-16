import logging
import time

from starlette.exceptions import HTTPException
from starlette.requests import Request

from ..options import options
from . import (
    format_task,
    get_flower_app,
    get_argument,
    render_template,
    require_authentication,
    json_response,
)

logger = logging.getLogger(__name__)


async def worker(request: Request):
    require_authentication(request)

    name = request.path_params["hostname"]
    app = get_flower_app(request)

    try:
        await app.update_workers(workername=name)
    except Exception as exc:
        logger.error(exc)

    worker = app.workers.get(name)

    if worker is None:
        raise HTTPException(
            status_code=404,
            detail=f"Unknown worker '{name}'",
        )

    if "stats" not in worker:
        raise HTTPException(
            status_code=404,
            detail=f"Unable to get stats for '{name}' worker",
        )

    return render_template(
        request,
        "worker.html",
        worker=dict(worker, name=name),
        read_only=app.options.read_only,
    )


async def workers(request: Request):
    require_authentication(request)

    refresh = get_argument(
        request,
        "refresh",
        default=False,
        type=bool,
    )

    json = get_argument(
        request,
        "json",
        default=False,
        type=bool,
    )

    app = get_flower_app(request)
    events = app.events.state

    if refresh:
        try:
            await app.update_workers()
        except Exception as exc:
            logger.exception(
                "Failed to update workers: %s",
                exc,
            )

    workers = {}

    for name, values in events.counter.items():
        if name not in events.workers:
            continue

        worker = events.workers[name]

        info = dict(values)
        info.update(as_dict(worker))
        info.update(status=worker.alive)

        workers[name] = info

    if options.purge_offline_workers is not None:
        timestamp = int(time.time())
        offline_workers = []

        for name, info in workers.items():
            if info.get("status", True):
                continue

            heartbeats = info.get("heartbeats", [])
            last_heartbeat = (
                int(max(heartbeats))
                if heartbeats
                else None
            )

            if (
                not last_heartbeat
                or timestamp - last_heartbeat
                > options.purge_offline_workers
            ):
                offline_workers.append(name)

        for name in offline_workers:
            workers.pop(name)

    if json:
        return json_response(
            {"data": list(workers.values())}
        )

    return render_template(
        request,
        "workers.html",
        workers=workers,
        broker=app.broker_uri,
        autorefresh=(
            1 if app.options.auto_refresh else 0
        ),
    )


def as_dict(worker):
    if hasattr(worker, "_fields"):
        return {
            key: getattr(worker, key)
            for key in worker._fields
        }

    return worker_info(worker)


def worker_info(worker):
    fields = (
        "hostname",
        "pid",
        "freq",
        "heartbeats",
        "clock",
        "active",
        "processed",
        "loadavg",
        "sw_ident",
        "sw_ver",
        "sw_sys",
    )

    return {
        key: value
        for key in fields
        if (value := getattr(worker, key, None)) is not None
    }
