from starlette.routing import Route

from .api import control, tasks as task_api, workers as worker_api
from .views import auth, monitor
from .views import broker, error, tasks, workers


routes = [
    # App
    Route("/", workers.workers, name="main"),
    Route("/workers", workers.workers, name="workers"),
    Route(
        "/worker/{hostname}",
        workers.worker,
        name="worker",
    ),
    Route(
        "/task/{task_id}",
        tasks.task,
        name="task",
    ),
    Route(
        "/tasks",
        tasks.tasks,
        name="tasks",
    ),
    Route(
        "/tasks/datatable",
        tasks.tasks_datatable,
        methods=["GET", "POST"],
        name="tasks-datatable",
    ),
    Route(
        "/broker",
        broker.broker,
        name="broker",
    ),

    # Worker API
    Route(
        "/api/workers",
        worker_api.list_workers,
        methods=["GET"],
        name="list-workers",
    ),

    # ... worker control routes ...

    # Task API
    Route(
        "/api/tasks",
        task_api.list_tasks,
        methods=["GET"],
        name="list-tasks",
    ),

    # ... remaining task API routes ...

    # Metrics
    Route(
        "/metrics",
        monitor.metrics,
        name="metrics",
    ),
    Route(
        "/healthcheck",
        monitor.healthcheck,
        name="healthcheck",
    ),

    # Auth
    Route(
        "/login",
        auth.login,
        name="login",
    ),

    # Error
    Route(
        "/{path:path}",
        error.not_found,
        name="not-found",
    ),
]
