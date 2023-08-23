from sqlalchemy import JSON, Column, Enum, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import relationship

import xray_swagger.db.models.mixins as mixins
from xray_swagger.db.base import Base
from xray_swagger.db.models.product import Product
from xray_swagger.db.models.user import AuthLevel


class SettingsProductParameter(Base):
    setting_param_name = Column(String(255), primary_key=True)
    authlevel = Column(Enum(AuthLevel), nullable=False)
    json_schema = Column(JSON, nullable=True)


class SettingsProduct(mixins.TimestampMixin, mixins.AuthorMixin, Base):
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
    product = relationship(Product, back_populates="settings")
    changelogs = relationship(
        "SettingsProductChangelog",
        back_populates="settings_product",
    )
    __table_args__ = (Index("idx_product_param", product_id, setting_param_name, unique=True),)


class SettingsGlobal(mixins._ModifiedAt, mixins._LastEditorId, Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    setting_param_name = Column(String(255), nullable=False)
    authlevel = Column(Enum(AuthLevel), nullable=False)
    json_schema = Column(JSON, nullable=False)
    value = Column(JSON, nullable=True)


class SettingsProductChangelog(mixins._CreatedAt, mixins._LastEditorId, Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    version = Column(Integer, nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    settings_product_id = Column(
        Integer,
        ForeignKey("settings_product.id"),
        nullable=False,
    )
    settings_product = relationship(SettingsProduct, back_populates="changelogs")
    patch = Column(Text, nullable=False)
