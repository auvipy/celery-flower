from starlette.requests import Request
from starlette.responses import Response


# Workers

async def list_workers(request: Request) -> Response:
    raise NotImplementedError


async def shutdown_worker(request: Request) -> Response:
    hostname = request.path_params["hostname"]

    raise NotImplementedError


async def restart_worker_pool(request: Request) -> Response:
    hostname = request.path_params["hostname"]

    raise NotImplementedError


async def grow_worker_pool(request: Request) -> Response:
    hostname = request.path_params["hostname"]

    raise NotImplementedError


async def shrink_worker_pool(request: Request) -> Response:
    hostname = request.path_params["hostname"]

    raise NotImplementedError


async def autoscale_worker(request: Request) -> Response:
    hostname = request.path_params["hostname"]

    raise NotImplementedError


async def add_consumer(request: Request) -> Response:
    hostname = request.path_params["hostname"]

    raise NotImplementedError


async def cancel_consumer(request: Request) -> Response:
    hostname = request.path_params["hostname"]

    raise NotImplementedError


# Tasks

async def list_tasks(request: Request) -> Response:
    raise NotImplementedError


async def list_task_types(request: Request) -> Response:
    raise NotImplementedError


async def queue_lengths(request: Request) -> Response:
    raise NotImplementedError


async def task_info(request: Request) -> Response:
    task_id = request.path_params["task_id"]

    raise NotImplementedError


async def apply_task(request: Request) -> Response:
    task_id = request.path_params["task_id"]

    raise NotImplementedError


async def async_apply_task(request: Request) -> Response:
    task_id = request.path_params["task_id"]

    raise NotImplementedError


async def send_task(request: Request) -> Response:
    task_id = request.path_params["task_id"]

    raise NotImplementedError


async def task_result(request: Request) -> Response:
    task_id = request.path_params["task_id"]

    raise NotImplementedError


async def abort_task(request: Request) -> Response:
    task_id = request.path_params["task_id"]

    raise NotImplementedError


async def timeout_task(request: Request) -> Response:
    task_id = request.path_params["task_id"]

    raise NotImplementedError


async def rate_limit_task(request: Request) -> Response:
    task_id = request.path_params["task_id"]

    raise NotImplementedError


async def revoke_task(request: Request) -> Response:
    task_id = request.path_params["task_id"]

    raise NotImplementedError


# Monitoring

async def metrics(request: Request) -> Response:
    raise NotImplementedError


async def healthcheck(request: Request) -> Response:
    raise NotImplementedError
