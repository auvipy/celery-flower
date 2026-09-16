import copy
import logging

from starlette.exceptions import HTTPException
from starlette.requests import Request

from ..utils.search import QuerySyntaxError
from ..utils.tasks import (
    as_dict,
    get_task_by_id,
    search_tasks,
)

from . import (
    get_argument,
    get_flower_app,
    render_template,
    require_authentication,
    json_response,
)

logger = logging.getLogger(__name__)


async def task(request: Request):
    require_authentication(request)

    task_id = request.path_params["task_id"]
    app = get_flower_app(request)

    task = get_task_by_id(
        app.events,
        task_id,
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Unknown task '{task_id}'",
        )

    task = format_task(request, task)

    return render_template(
        request,
        "task.html",
        task=task,
        read_only=app.options.read_only,
    )


async def tasks_datatable(request: Request):
    require_authentication(request)

    app = get_flower_app(request)

    draw = get_argument(
        request,
        "draw",
        type=int,
    )

    start = get_argument(
        request,
        "start",
        type=int,
    )

    length = get_argument(
        request,
        "length",
        type=int,
    )

    search = get_argument(
        request,
        "search[value]",
        type=str,
    )

    column = get_argument(
        request,
        "order[0][column]",
        type=int,
    )

    sort_by = get_argument(
        request,
        f"columns[{column}][data]",
        type=str,
    )

    sort_order = (
        get_argument(
            request,
            "order[0][dir]",
            type=str,
        )
        == "desc"
    )

    try:
        page = search_tasks(
            app.events,
            search=search,
            sort_by=sort_by,
            descending=sort_order,
            offset=start,
            limit=length,
        )
    except QuerySyntaxError as exc:
        return json_response({
            "draw": draw,
            "data": [],
            "recordsTotal": len(
                app.events.state.tasks
            ),
            "recordsFiltered": 0,
            "searchError": str(exc),
        })

    filtered_tasks = []

    task_map = getattr(
        app.events.state.tasks,
        "data",
        app.events.state.tasks,
    )

    for task_id in page.task_ids:
        task = task_map.get(task_id)

        if task is None:
            continue

        task_dict = as_dict(
            format_task(
                request,
                (task_id, task),
            )[1]
        )

        if task_dict.get("worker"):
            task_dict["worker"] = (
                task_dict["worker"].hostname
            )

        filtered_tasks.append(task_dict)

    return json_response({
        "draw": draw,
        "data": filtered_tasks,
        "recordsTotal": page.total_count,
        "recordsFiltered": page.filtered_count,
    })


async def tasks(request: Request):
    require_authentication(request)

    app = get_flower_app(request)
    capp = app.capp

    time_format = (
        "natural-time"
        if app.options.natural_time
        else "time"
    )

    if capp.conf.timezone:
        time_format += "-" + str(
            capp.conf.timezone
        )

    return render_template(
        request,
        "tasks.html",
        tasks=[],
        columns=app.options.tasks_columns,
        time=time_format,
    )


def format_task(request: Request, task):
    """
    Same behavior as the TasksDataTable override in the
    existing Tornado implementation.
    """
    uuid, args = task

    app = get_flower_app(request)
    custom_format_task = app.options.format_task

    if custom_format_task:
        try:
            args = custom_format_task(
                copy.copy(args)
            )
        except Exception:
            logger.exception(
                "Failed to format '%s' task",
                uuid,
            )

    return uuid, args
