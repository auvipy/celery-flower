import copy
import inspect
import logging
import re
import traceback
import hmac

from base64 import b64decode

from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, PlainTextResponse

from ..utils import bugreport, strtobool, template

logger = logging.getLogger(__name__)


def get_flower_app(request: Request):
    """Return the Flower application attached to the Starlette app."""
    return request.app.state.flower


def get_options(request: Request):
    return get_flower_app(request).options


def get_capp(request: Request):
    """Return the Celery application."""
    return get_flower_app(request).capp


def get_current_user(request: Request):
    """
    Starlette equivalent of BaseHandler.get_current_user().
    """
    app = get_flower_app(request)
    options = app.options

    # Basic Auth
    basic_auth = options.basic_auth

    if basic_auth:
        auth_header = request.headers.get("Authorization", "")

        try:
            basic, credentials = auth_header.split()
            credentials = b64decode(credentials.encode()).decode()

            if basic != "Basic":
                raise HTTPException(status_code=401)

            for stored_credential in basic_auth:
                if hmac.compare_digest(stored_credential, credentials):
                    break
            else:
                raise HTTPException(status_code=401)

        except ValueError as exc:
            raise HTTPException(status_code=401) from exc

    # OAuth2 / cookie authentication
    if not options.auth:
        return True

    user = request.cookies.get("user")

    if user and re.match(options.auth, user):
        return user

    return None


def require_authentication(request: Request):
    """
    Equivalent of Tornado's @web.authenticated.
    """
    user = get_current_user(request)

    if user is None:
        raise HTTPException(
            status_code=401,
            headers={"WWW-Authenticate": 'Basic realm="flower"'},
        )

    request.state.user = user
    return user


def get_argument(
    request: Request,
    name,
    default=None,
    *,
    strip=True,
    type=None,
    escape=True,
):
    """
    Starlette equivalent of Flower's BaseHandler.get_argument().
    """
    arg = request.query_params.get(name, default)

    if isinstance(arg, str) and strip:
        arg = arg.strip()

    if arg and isinstance(arg, str) and escape:
        # Preserve the existing Flower behavior.
        from tornado.escape import xhtml_escape

        arg = xhtml_escape(arg)

    if type is not None:
        try:
            if type is bool:
                arg = strtobool(str(arg))
            else:
                arg = type(arg)
        except (ValueError, TypeError) as exc:
            if arg is None and default is None:
                return arg

            raise HTTPException(
                status_code=400,
                detail=(
                    f"Invalid argument '{arg}' "
                    f"of type '{type.__name__}'"
                ),
            ) from exc

    return arg


def format_task(request: Request, task):
    """
    Equivalent of BaseHandler.format_task().
    """
    app = get_flower_app(request)
    custom_format_task = app.options.format_task

    if custom_format_task:
        try:
            task = custom_format_task(copy.copy(task))
        except Exception:
            logger.exception(
                "Failed to format '%s' task",
                task.uuid,
            )

    return task


def get_active_queue_names(request: Request):
    """
    Equivalent of BaseHandler.get_active_queue_names().
    """
    app = get_flower_app(request)

    queues = set()

    for _, info in app.workers.items():
        for queue in info.get("active_queues", []):
            queues.add(queue["name"])

    if not queues:
        queues = (
            {app.capp.conf.task_default_queue}
            | {
                q.name
                for q in app.capp.conf.task_queues or []
                if q.name
            }
        )

    return sorted(queues)


def render_template(
    request: Request,
    template_name: str,
    **context,
):
    """
    Temporary Starlette rendering helper.

    This is intentionally kept very close to the old BaseHandler.render()
    behavior. Template migration can happen separately.
    """
    app = get_flower_app(request)
    options = app.options

    functions = dict(
        inspect.getmembers(template, inspect.isfunction)
    )

    if set(functions) & set(context):
        raise AssertionError(
            "Template context conflicts with template helper name"
        )

    context.update(functions)
    context["url_prefix"] = options.url_prefix

    # This assumes the templates have been migrated to the Starlette
    # template engine used by the new implementation.
    from starlette.templating import Jinja2Templates

    templates = Jinja2Templates(
        directory=app.template_path
    )

    context["request"] = request

    return templates.TemplateResponse(
        request=request,
        name=template_name,
        context=context,
    )


def json_response(data, status_code=200):
    return JSONResponse(
        content=data,
        status_code=status_code,
    )


def text_response(
    data,
    status_code=200,
    media_type="text/plain",
):
    return PlainTextResponse(
        content=data,
        status_code=status_code,
        media_type=media_type,
    )


def html_response(data, status_code=200):
    return HTMLResponse(
        content=data,
        status_code=status_code,
    )
