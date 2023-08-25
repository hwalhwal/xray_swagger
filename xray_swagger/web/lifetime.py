from __future__ import annotations

import re
from typing import TYPE_CHECKING, Awaitable, Callable

from fastapi import FastAPI
from loguru import logger
from sqlalchemy import Engine, event
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from xray_swagger.services.redis.lifetime import init_redis, shutdown_redis
from xray_swagger.settings import settings

if TYPE_CHECKING:
    from sqlalchemy.engine import ExecutionContext
    from sqlalchemy.engine.base import Connection
    from sqlalchemy.engine.interfaces import DBAPICursor, _DBAPIAnyExecuteParams

    # from sqlalchemy.dialects.postgresql.asyncpg import AsyncAdapt_asyncpg_cursor
    # from sqlalchemy.dialects.postgresql.asyncpg import PGExecutionContext_asyncpg

STMT_INTPLTN = re.compile(r"\$(\d+)")


@event.listens_for(Engine, "before_cursor_execute")
def receive_before_cursor_execute(
    conn: Connection,
    cursor: DBAPICursor,
    statement: str,
    parameters: _DBAPIAnyExecuteParams,
    context: ExecutionContext,
    executemany: bool,
):
    "listen for the 'before_cursor_execute' event"
    logger.debug("\n====================================================")
    logger.debug(context.dialect.name)
    if parameters:
        sub_statement = re.sub(STMT_INTPLTN, r'"{\1}"', statement)
        # logger.debug(sub_statement)
        logger.debug("\n" + sub_statement.format(None, *parameters))
    else:
        logger.debug("\n" + statement)


def _setup_db(app: FastAPI) -> None:  # pragma: no cover
    """
    Creates connection to the database.

    This function creates SQLAlchemy engine instance,
    session_factory for creating sessions
    and stores them in the application's state property.

    :param app: fastAPI application.
    """
    engine = create_async_engine(str(settings.db_url), echo=settings.db_echo)
    session_factory = async_sessionmaker(
        engine,
        expire_on_commit=False,
    )
    app.state.db_engine = engine
    app.state.db_session_factory = session_factory


def register_startup_event(
    app: FastAPI,
) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    Actions to run on application startup.

    This function uses fastAPI app to store data
    in the state, such as db_engine.

    :param app: the fastAPI application.
    :return: function that actually performs actions.
    """

    @app.on_event("startup")
    async def _startup() -> None:  # noqa: WPS430
        _setup_db(app)
        init_redis(app)
        pass  # noqa: WPS420

    return _startup


def register_shutdown_event(
    app: FastAPI,
) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    Actions to run on application's shutdown.

    :param app: fastAPI application.
    :return: function that actually performs actions.
    """

    @app.on_event("shutdown")
    async def _shutdown() -> None:  # noqa: WPS430
        await app.state.db_engine.dispose()

        await shutdown_redis(app)
        pass  # noqa: WPS420

    return _shutdown
