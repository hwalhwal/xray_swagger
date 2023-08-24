from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends
from loguru import logger

from xray_swagger.db.dao.settings_dao import (
    SettingsGlobalDAO,
    SettingsProductDAO,
    SettingsProductParameterDAO,
)

from .schema import SettingsGlobalDTO, SettingsProductParameterDTO

router = APIRouter()


@router.get(path="/global", response_model=list[SettingsGlobalDTO])
async def get_all_global_settings(
    dao: SettingsGlobalDAO = Depends(),
):
    d = await dao.get_all()
    return d


@router.put(path="/global/watchdog-timer", response_model=SettingsGlobalDTO)
async def update_watchdog_timer(
    new_value: bool,
    dao: SettingsGlobalDAO = Depends(),
):
    d = await dao.get("Watchdog.Timer")
    await dao.update(d, new_value)

    return d


@router.put(path="/global/conveyor-direction", response_model=SettingsGlobalDTO)
async def update_conveyor_direction(
    new_value: int,
    dao: SettingsGlobalDAO = Depends(),
):
    d = await dao.get("Conveyor.Direction")
    await dao.update(d, new_value)

    return d


@router.put(path="/global/inspection-mode", response_model=SettingsGlobalDTO)
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


@router.post(path="/products/{product_id}")
async def create_product_setting(
    product_id: int,
    value: str,
    dao: SettingsProductDAO = Depends(),
):
    ...
