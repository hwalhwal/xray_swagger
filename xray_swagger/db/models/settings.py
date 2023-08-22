from sqlalchemy import JSON, Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from xray_swagger.db.base import Base
from xray_swagger.db.models.mixins import AuthorMixin, TimestampMixin
from xray_swagger.db.models.user import AuthLevel


class SettingsProductParameter(Base):

    setting_param_name = Column(String(255), primary_key=True)
    authlevel = Column(Enum(AuthLevel), nullable=False)
    containers_affected = Column(JSON, nullable=True)
    setting_template = Column(JSON, nullable=True)


class SettingsProduct(TimestampMixin, AuthorMixin, Base):

    # index를 product에 거는게 좋아보임. 혹은 필요없고.

    id = Column(Integer, primary_key=True, autoincrement=True)
    setting_param_name = Column(
        String(255),
        ForeignKey("settings_product_parameter.setting_param_name"),
        nullable=False,
        onupdate="CASCADE",
    )
    version = Column(Integer, nullable=False, default=0)  # 세팅변경시 ++
    value = Column(JSON, nullable=True)  # setting_template 기반으로
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    product = relationship("Product", back_populates="settings")
    changelogs = relationship(
        "SettingsProductChangelog",
        back_populates="settings_product",
    )


class SettingsGlobal(TimestampMixin, AuthorMixin, Base):

    id = Column(Integer, primary_key=True, autoincrement=True)
    setting_param_name = Column(String(255), nullable=False)
    authlevel = Column(Enum(AuthLevel), nullable=False)
    json_schema = Column(JSON, nullable=False)
    value = Column(JSON, nullable=True)


class SettingsProductChangelog(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    version = Column(Integer, nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    settings_product_id = Column(
        Integer,
        ForeignKey("settings_product.id"),
        nullable=False,
    )
    settings_product = relationship(SettingsProduct, back_populates="changelogs")
    editor_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
    )
    patch = Column(Text, nullable=False)
