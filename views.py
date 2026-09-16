from starlette.requests import Request
from starlette.responses import Response


async def workers(request: Request) -> Response:
    """
    Replacement for:
        WorkersView
    """
    raise NotImplementedError


async def worker(request: Request) -> Response:
    """
    Replacement for:
        WorkerView
    """
    hostname = request.path_params["hostname"]

    raise NotImplementedError


async def task(request: Request) -> Response:
    """
    Replacement for:
        TaskView
    """
    task_id = request.path_params["task_id"]

    raise NotImplementedError


async def tasks(request: Request) -> Response:
    """
    Replacement for:
        TasksView
    """
    raise NotImplementedError


async def tasks_datatable(request: Request) -> Response:
    """
    Replacement for:
        TasksDataTable
    """
    raise NotImplementedError


async def broker(request: Request) -> Response:
    """
    Replacement for:
        BrokerView
    """
    raise NotImplementedError


async def login(request: Request) -> Response:
    """
    Replacement for:
        auth.LoginHandler
    """
    raise NotImplementedError


async def not_found(request: Request) -> Response:
    """
    Replacement for:
        NotFoundErrorHandler
    """
    raise NotImplementedError
