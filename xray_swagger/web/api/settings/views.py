import json
from datetime import datetime
from typing import Any, Sequence

import fastjsonschema
from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends
from loguru import logger
from pydantic.json_schema import JsonSchemaValue

from xray_swagger.db.dao.settings_dao import (
    SettingsGlobalDAO,
    SettingsProductChangelogDAO,
    SettingsProductDAO,
    SettingsProductParameterDAO,
)
from xray_swagger.db.models.user import User
from xray_swagger.web.dependencies.permissions import (
    IsAuthenticated,
    IsEngineer,
    IsSupervisor,
    PermissionsDependency,
)
from xray_swagger.web.dependencies.users import get_current_active_user
from xray_swagger.web.utils import make_patch_text

from .schema import (
    SettingsGlobalDTO,
    SettingsGlobalUpdateDTO,
    SettingsProductChangelogCreateDTO,
    SettingsProductChangelogDTO,
    SettingsProductCreateDTO,
    SettingsProductDTO,
    SettingsProductParameterDTO,
    SettingsProductUpdateDTO,
)

router = APIRouter()


@router.get(path="/global")
async def get_all_global_settings(
    dao: SettingsGlobalDAO = Depends(),
) -> Sequence[SettingsGlobalDTO]:
    d = await dao.get_all()
    return d


@router.patch(path="/global/watchdog-timer")
async def update_watchdog_timer(
    new_value: bool,
    user: User = Depends(get_current_active_user),
    authorize: bool = Depends(PermissionsDependency([IsAuthenticated, IsEngineer])),
    dao: SettingsGlobalDAO = Depends(),
) -> SettingsGlobalDTO:
    logger.debug(f"User permission check <IsEngineer> passed? {authorize=}")
    d = await dao.get("Watchdog.Timer")

    payload = SettingsGlobalUpdateDTO.from_raw_value(
        param_value=new_value,
        param_schema=d.json_schema,
        user_id=user.id,
    )
    await dao.update(d, payload, exclude_none=True)

    return d


@router.patch(
    path="/global/conveyor-direction",
    dependencies=[Depends(PermissionsDependency([IsAuthenticated, IsEngineer]))],
)
async def update_conveyor_direction(
    new_value: int,
    user: User = Depends(get_current_active_user),
    dao: SettingsGlobalDAO = Depends(),
) -> SettingsGlobalDTO:
    d = await dao.get("Conveyor.Direction")

    payload = SettingsGlobalUpdateDTO.from_raw_value(
        param_value=new_value,
        param_schema=d.json_schema,
        user_id=user.id,
    )
    await dao.update(d, payload, exclude_none=True)

    return d


@router.patch(
    path="/global/inspection-mode",
    dependencies=[Depends(PermissionsDependency([IsAuthenticated, IsSupervisor]))],
)
async def update_inspection_mode(
    new_value: int,
    user: User = Depends(get_current_active_user),
    dao: SettingsGlobalDAO = Depends(),
) -> SettingsGlobalDTO:
    d = await dao.get("Inspection.Mode")

    payload = SettingsGlobalUpdateDTO.from_raw_value(
        param_value=new_value,
        param_schema=d.json_schema,
        user_id=user.id,
    )
    await dao.update(d, payload, exclude_none=True)

    return d


@router.get(path="/product-params")
async def get_settings_product_params(
    name_query: str = None,
    dao: SettingsProductParameterDAO = Depends(),
) -> Sequence[SettingsProductParameterDTO]:
    if name_query:
        logger.debug(f"{name_query=}")
        d = await dao.filter(name_query)
    else:
        d = await dao.get_all()

    if not d:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    logger.debug(f"{len(d)=}")
    logger.debug(d[0].__dict__)

    return d


@router.get(path="/product-params/{setting_param_name}")
async def get_settings_product_param_by_name(
    setting_param_name: str,
    dao: SettingsProductParameterDAO = Depends(),
) -> SettingsProductParameterDTO:
    d = await dao.get(setting_param_name)

    return SettingsProductParameterDTO.model_validate(d)


##########################################################################################
#
##########################################################################################

from xray_swagger.web.api.products.views import router as products_router  # noqa: E402


@products_router.post(
    path="/{product_id}/settings",
    status_code=status.HTTP_201_CREATED,
    tags=["settings"],
)
async def create_product_setting(
    product_id: int,
    setting_param_name: str,
    value: Any,
    settings_product_dao: SettingsProductDAO = Depends(),
    param_dao: SettingsProductParameterDAO = Depends(),
    user: User = Depends(get_current_active_user),
) -> SettingsProductDTO:
    logger.debug(f"{setting_param_name}")
    logger.debug(f"{value}({type(value)})")
    param = await param_dao.get(setting_param_name)
    if not param:
        HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Not found settings param: {setting_param_name}",
        )
    payload = SettingsProductCreateDTO.from_raw_value(
        json.loads(value),
        param.json_schema,
        setting_param_name=setting_param_name,
        product_id=product_id,
        user_id=user.id,
    )
    logger.debug(payload)
    new_row = await settings_product_dao.create(payload)
    return new_row


@products_router.get(
    path="/{product_id}/settings",
    tags=["settings"],
)
async def get_all_product_settings(
    product_id: int,  # TODO: set current product to session
    dao: SettingsProductDAO = Depends(),
) -> Sequence[SettingsProductDTO]:
    d = await dao.filter_by_product(product_id)
    return d


@products_router.get(
    path="/{product_id}/settings/{setting_param_name}",
    tags=["settings"],
)
async def get_product_setting(
    product_id: int,
    setting_param_name: str,
    dao: SettingsProductDAO = Depends(),
) -> SettingsProductDTO:
    d = await dao.get(product_id, setting_param_name)
    return d


@products_router.patch(
    path="/{product_id}/settings/{setting_param_name}",
    dependencies=[Depends(PermissionsDependency([IsAuthenticated, IsSupervisor]))],
    tags=["settings"],
)
async def update_product_setting(
    product_id: int,
    setting_param_name: str,
    new_value: Any,
    settings_product_dao: SettingsProductDAO = Depends(),
    param_dao: SettingsProductParameterDAO = Depends(),
    changelog_dao: SettingsProductChangelogDAO = Depends(),
    user: User = Depends(get_current_active_user),
) -> SettingsProductDTO:
    logger.debug(f"{new_value=}({type(new_value)})")
    param = await param_dao.get(setting_param_name)
    settings_product = await settings_product_dao.get(product_id, setting_param_name)
    if not param or not settings_product:
        HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Not found settings param: {setting_param_name}",
        )
    old_value = settings_product.value
    logger.debug(f"{settings_product=!s}")

    new_value = await validate(json.loads(new_value), param.json_schema)
    logger.debug(f"{new_value=}({type(new_value)})")
    logger.debug(f"{old_value=} == {new_value=}")
    # Update only when the new value is not equal to the old value
    if old_value == new_value:  # TODO: non hashable type comparison
        return settings_product

    version = settings_product.version + 1
    modified_at = datetime.utcnow()
    update_payload = SettingsProductUpdateDTO(
        version=version,
        value=new_value,
        last_editor_id=user.id,
        modified_at=modified_at,
    )
    await settings_product_dao.update(settings_product, update_payload)

    patch = make_patch_text(old_value, new_value)
    changelog_payload = SettingsProductChangelogCreateDTO(
        version=version,
        product_id=product_id,
        settings_product_id=settings_product.id,
        patch=patch,
        last_editor_id=user.id,
        modified_at=modified_at,
    )
    changelog = await changelog_dao.create(changelog_payload)
    logger.info(changelog)

    return settings_product


async def validate(value: Any, schema: JsonSchemaValue):
    json_validator = fastjsonschema.compile(schema)
    return json_validator(value)


@products_router.get(
    path="/{product_id}/settings/changelog",
    tags=["settings", "changelog"],
)
async def get_settings_changelog(
    product_id: int,
    name_query: str | None = None,
    dao: SettingsProductChangelogDAO = Depends(),
    # user: User = Depends(get_current_active_user),
) -> Sequence[SettingsProductChangelogDTO]:
    """Get all settings changelogs of the product"""
    d = await dao.filter(product_id, name_query)
    return d
