from starlette.routing import Route


async def not_implemented(request):
    return {"status": "not implemented"}


routes = [
    # Web
    Route("/", not_implemented, name="home"),
    Route("/workers", not_implemented, name="workers"),
    Route("/worker/{hostname}", not_implemented, name="worker"),
    Route("/task/{task_id}", not_implemented, name="task"),
    Route("/tasks", not_implemented, name="tasks"),
    Route("/tasks/datatable", not_implemented, name="tasks-datatable"),
    Route("/broker", not_implemented, name="broker"),

    # Workers
    Route("/api/workers", not_implemented, name="list-workers"),
    Route(
        "/api/worker/shutdown/{hostname}",
        not_implemented,
        name="shutdown-worker",
    ),
    Route(
        "/api/worker/pool/restart/{hostname}",
        not_implemented,
        name="restart-worker-pool",
    ),
    Route(
        "/api/worker/pool/grow/{hostname}",
        not_implemented,
        name="grow-worker-pool",
    ),
    Route(
        "/api/worker/pool/shrink/{hostname}",
        not_implemented,
        name="shrink-worker-pool",
    ),
    Route(
        "/api/worker/pool/autoscale/{hostname}",
        not_implemented,
        name="autoscale-worker",
    ),
    Route(
        "/api/worker/queue/add-consumer/{hostname}",
        not_implemented,
        name="add-consumer",
    ),
    Route(
        "/api/worker/queue/cancel-consumer/{hostname}",
        not_implemented,
        name="cancel-consumer",
    ),

    # Tasks
    Route("/api/tasks", not_implemented, name="list-tasks"),
    Route("/api/task/types", not_implemented, name="list-task-types"),
    Route("/api/queues/length", not_implemented, name="queue-lengths"),
    Route("/api/task/info/{task_id}", not_implemented, name="task-info"),
    Route("/api/task/apply/{task_id}", not_implemented, name="apply-task"),
    Route(
        "/api/task/async-apply/{task_id}",
        not_implemented,
        name="async-apply-task",
    ),
    Route(
        "/api/task/send-task/{task_id}",
        not_implemented,
        name="send-task",
    ),
    Route(
        "/api/task/result/{task_id}",
        not_implemented,
        name="task-result",
    ),
    Route(
        "/api/task/abort/{task_id}",
        not_implemented,
        name="abort-task",
    ),
    Route(
        "/api/task/timeout/{task_id}",
        not_implemented,
        name="timeout-task",
    ),
    Route(
        "/api/task/rate-limit/{task_id}",
        not_implemented,
        name="rate-limit-task",
    ),
    Route(
        "/api/task/revoke/{task_id}",
        not_implemented,
        name="revoke-task",
    ),

    # System
    Route("/metrics", not_implemented, name="metrics"),
    Route("/healthcheck", not_implemented, name="healthcheck"),
    Route("/login", not_implemented, name="login"),

    # Catch-all
    Route("/{path:path}", not_implemented, name="not-found"),
]
