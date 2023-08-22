from sqlalchemy.orm import DeclarativeBase, declared_attr

from xray_swagger.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta

    @declared_attr.directive
    def __tablename__(cls) -> str:
        sn = [c if c.islower() else f"_{c.lower()}" for c in cls.__name__]
        return "".join(sn)[1:]
        # return cls.__name__.lower()
