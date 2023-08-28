import json
from typing import Any

import fastjsonschema
from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends
from loguru import logger

from xray_swagger.db.dao.settings_dao import (
    SettingsGlobalDAO,
    SettingsProductDAO,
    SettingsProductParameterDAO,
)

from .schema import (
    FullSettingsProductDTO,
    SettingsGlobalDTO,
    SettingsProductDTO,
    SettingsProductParameterDTO,
    SettingsProductUpdateDTO,
)

router = APIRouter()


@router.get(path="/global", response_model=list[SettingsGlobalDTO])
async def get_all_global_settings(
    dao: SettingsGlobalDAO = Depends(),
):
    d = await dao.get_all()
    return d


@router.patch(path="/global/watchdog-timer", response_model=SettingsGlobalDTO)
async def update_watchdog_timer(
    new_value: bool,
    dao: SettingsGlobalDAO = Depends(),
):
    d = await dao.get("Watchdog.Timer")
    await dao.update(d, new_value)

    return d


@router.patch(path="/global/conveyor-direction", response_model=SettingsGlobalDTO)
async def update_conveyor_direction(
    new_value: int,
    dao: SettingsGlobalDAO = Depends(),
):
    d = await dao.get("Conveyor.Direction")
    await dao.update(d, new_value)

    return d


@router.patch(path="/global/inspection-mode", response_model=SettingsGlobalDTO)
async def update_inspection_mode(
    new_value: int,
    dao: SettingsGlobalDAO = Depends(),
):
    d = await dao.get("Inspection.Mode")
    await dao.update(d, new_value)

    return d


@router.get(path="/product-params", response_model=list[SettingsProductParameterDTO])
async def get_settings_product_params(
    name_query: str = None,
    dao: SettingsProductParameterDAO = Depends(),
):
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


@router.get(path="/product-params/{setting_param_name}", response_model=SettingsProductParameterDTO)
async def get_settings_product_param_by_name(
    setting_param_name: str,
    dao: SettingsProductParameterDAO = Depends(),
):
    d = await dao.get(setting_param_name)

    return SettingsProductParameterDTO.model_validate(d)


##########################################################################################
#
##########################################################################################

from xray_swagger.web.api.products.views import router as products_router


@products_router.post(path="/{product_id}/settings", status_code=status.HTTP_201_CREATED)
async def create_product_setting(
    product_id: int,
    setting_param_name: str,
    value: Any,
    settings_product_dao: SettingsProductDAO = Depends(),
    param_dao: SettingsProductParameterDAO = Depends(),
):
    logger.debug(f"{setting_param_name}")
    logger.debug(f"{value}({type(value)})")
    param = await param_dao.get(setting_param_name)
    if not param:
        HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Not found settings param: {setting_param_name}",
        )
    param_schema = param.json_schema
    value = json.loads(value)
    logger.debug(f"{value}({type(value)})")
    json_validator = fastjsonschema.compile(param_schema)
    value = json_validator(value)
    logger.debug(f"{value}({type(value)})")
    # insert
    new_row = FullSettingsProductDTO(
        setting_param_name=setting_param_name,
        version=1,
        value=value,
        product_id=product_id,
        creator_id=1,
        last_editor_id=1,
    )
    await settings_product_dao.create(new_row)


@products_router.get(path="/{product_id}/settings", response_model=list[SettingsProductDTO])
async def get_all_product_settings(
    product_id: int,  # TODO: set current product to session
    dao: SettingsProductDAO = Depends(),
):
    d = await dao.filter_by_product(product_id)
    return d


@products_router.get(
    path="/{product_id}/settings/{setting_param_name}",
    response_model=FullSettingsProductDTO,
)
async def get_product_setting(
    product_id: int,
    setting_param_name: str,
    dao: SettingsProductDAO = Depends(),
):
    d = await dao.get(product_id, setting_param_name)
    return d


@products_router.patch(
    path="/{product_id}/settings/{setting_param_name}",
    response_model=SettingsProductDTO,
)
async def update_product_setting(
    product_id: int,
    setting_param_name: str,
    value: Any,
    settings_product_dao: SettingsProductDAO = Depends(),
    param_dao: SettingsProductParameterDAO = Depends(),
):
    logger.debug(f"{value=}({type(value)})")
    param = await param_dao.get(setting_param_name)
    settings_product = await settings_product_dao.get(product_id, setting_param_name)
    if not param or not settings_product:
        HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Not found settings param: {setting_param_name}",
        )
    old_value = settings_product.value
    logger.debug(f"{settings_product=!s}")

    value = await validate(json.loads(value), param.json_schema)
    logger.debug(f"{value=}({type(value)})")
    logger.debug(f"{old_value=} == {value=}")
    # Update only when the new value is not equal to the old value
    if old_value != value:  # TODO: non hashable type comparison
        version = settings_product.version + 1
        update_payload = SettingsProductUpdateDTO(version=version, value=value, last_editor_id=2)
        await settings_product_dao.update(settings_product, update_payload)

    return settings_product


async def validate(value: Any, schema: dict):
    json_validator = fastjsonschema.compile(schema)
    return json_validator(value)
