from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from xray_swagger.db.dependencies import get_db_session


class DAOBase:
    """Base Class for DAO."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:
        self.session = session
