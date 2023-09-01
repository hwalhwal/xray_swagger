from __future__ import annotations

import typing
from datetime import datetime

from sqlalchemy import select

from xray_swagger.db.dao._base import DAOBase
from xray_swagger.db.models.user import AuthLevel, User

if typing.TYPE_CHECKING:
    from xray_swagger.web.api.users.schema import UserUpdateDTO

__all__ = ("UserDAO",)


class UserDAO(DAOBase):
    async def create(
        self,
        username: str,
        password: str,
        fullname: str,
        phone_number: str = None,
        company: str = None,
        job_title: str = None,
        authlevel: AuthLevel = AuthLevel.OPERATOR,
    ) -> User:
        new_user = User(
            username=username,
            password=password,
            fullname=fullname,
            phone_number=phone_number,
            company=company,
            job_title=job_title,
            authlevel=authlevel,
        )
        self.session.add(new_user)
        print(f"{new_user.id=}")
        await self.session.flush()
        print(f"{new_user.id=}")
        return new_user

    async def get_by_id(self, id: int) -> User | None:
        raw = await self.session.execute(select(User).where(User.id == id))
        return raw.scalar()

    async def get_by_username(self, name: str) -> User | None:
        raw = await self.session.execute(select(User).where(User.username == name))
        return raw.scalar()

    async def get_all(self) -> list[User]:
        # TODO: delete 된 유저 filter 기본 (관리자 이상만 해제가능)
        # TODO: sort, query, pagenation
        raw = await self.session.execute(select(User))
        return raw.scalars().fetchall()

    async def update(self, db_obj: User, update_fields: UserUpdateDTO) -> None:
        refined_update_fields = update_fields.model_dump(exclude_unset=True)
        for k in refined_update_fields.keys():
            print(f"{type(db_obj).__name__}.{k} = {db_obj.__getattribute__(k)}")
        # UPDATE FIELDS
        async with self.session.begin_nested():
            print(f"=== UPDATE {type(db_obj).__name__}")
            for k, v in refined_update_fields.items():
                db_obj.__setattr__(k, v)

        for k in refined_update_fields.keys():
            print(f"{type(db_obj).__name__}.{k} = {db_obj.__getattribute__(k)}")

    async def delete(self, db_obj: User) -> None:
        db_obj.deleted_at = datetime.utcnow()
        await self.session.commit()
        await self.session.refresh(db_obj)
