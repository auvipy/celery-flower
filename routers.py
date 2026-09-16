from starlette.routing import Route

from . import api, views


routes = [
    # App
    Route("/", views.workers, name="main"),
    Route("/workers", views.workers, name="workers"),
    Route("/worker/{hostname}", views.worker, name="worker"),
    Route("/task/{task_id}", views.task, name="task"),
    Route("/tasks", views.tasks, name="tasks"),
    Route("/tasks/datatable", views.tasks_datatable, name="tasks-datatable"),
    Route("/broker", views.broker, name="broker"),

    # Worker API
    Route("/api/workers", api.list_workers, name="list-workers"),
    Route(
        "/api/worker/shutdown/{hostname}",
        api.shutdown_worker,
        name="shutdown-worker",
    ),
    Route(
        "/api/worker/pool/restart/{hostname}",
        api.restart_worker_pool,
        name="restart-worker-pool",
    ),
    Route(
        "/api/worker/pool/grow/{hostname}",
        api.grow_worker_pool,
        name="grow-worker-pool",
    ),
    Route(
        "/api/worker/pool/shrink/{hostname}",
        api.shrink_worker_pool,
        name="shrink-worker-pool",
    ),
    Route(
        "/api/worker/pool/autoscale/{hostname}",
        api.autoscale_worker,
        name="autoscale-worker",
    ),
    Route(
        "/api/worker/queue/add-consumer/{hostname}",
        api.add_consumer,
        name="add-consumer",
    ),
    Route(
        "/api/worker/queue/cancel-consumer/{hostname}",
        api.cancel_consumer,
        name="cancel-consumer",
    ),

    # Task API
    Route("/api/tasks", api.list_tasks, name="list-tasks"),
    Route("/api/task/types", api.list_task_types, name="list-task-types"),
    Route("/api/queues/length", api.queue_lengths, name="queue-lengths"),
    Route("/api/task/info/{task_id}", api.task_info, name="task-info"),
    Route("/api/task/apply/{task_id}", api.apply_task, name="apply-task"),
    Route(
        "/api/task/async-apply/{task_id}",
        api.async_apply_task,
        name="async-apply-task",
    ),
    Route(
        "/api/task/send-task/{task_id}",
        api.send_task,
        name="send-task",
    ),
    Route(
        "/api/task/result/{task_id}",
        api.task_result,
        name="task-result",
    ),
    Route(
        "/api/task/abort/{task_id}",
        api.abort_task,
        name="abort-task",
    ),
    Route(
        "/api/task/timeout/{task_id}",
        api.timeout_task,
        name="timeout-task",
    ),
    Route(
        "/api/task/rate-limit/{task_id}",
        api.rate_limit_task,
        name="rate-limit-task",
    ),
    Route(
        "/api/task/revoke/{task_id}",
        api.revoke_task,
        name="revoke-task",
    ),

    # Metrics / system
    Route("/metrics", api.metrics, name="metrics"),
    Route("/healthcheck", api.healthcheck, name="healthcheck"),

    # Auth
    Route("/login", views.login, name="login"),

    # Error handler
    Route("/{path:path}", views.not_found, name="not-found"),
]
