import typing

from sqlalchemy import select

from xray_swagger.db.dao._base import DAOBase
from xray_swagger.db.models.user import User

if typing.TYPE_CHECKING:
    pass

__all__ = ("UserDAO",)


class UserDAO(DAOBase[User, "UserCreateDTO", "UserUpdateDTO"]):
    async def get_by_username(self, name: str) -> User | None:
        raw = await self.session.execute(select(User).where(User.username == name))
        return raw.scalar()

    # async def get_all(self) -> Sequence[User]:
    # TODO: delete 된 유저 filter 기본 (관리자 이상만 해제가능)
    # TODO: sort, query, pagenation
