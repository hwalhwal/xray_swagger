from typing import TYPE_CHECKING, AsyncGenerator

from loguru import logger
from starlette.requests import Request

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_db_session(request: Request) -> AsyncGenerator["AsyncSession", None]:
    """
    Create and get database session.

    :param request: current request.
    :yield: database session.
    """
    session: "AsyncSession" = request.app.state.db_session_factory()
    logger.debug("== Postgres Asyncsession registered")

    try:  # noqa: WPS501
        logger.debug("<<< Yield db session")
        yield session
    finally:
        logger.debug(">>> Close db session")
        await session.commit()
        await session.close()
