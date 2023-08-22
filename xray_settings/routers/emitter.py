from fastapi import APIRouter
from pydantic import RootModel
from pydantic.types import conint

emitter_router = APIRouter(prefix="/emitter", tags=["emitter"])


class XrayEmitterVoltage(RootModel):
    root: conint(ge=0, le=10000)


class XrayEmitterCurrent(RootModel):
    root: conint(ge=0, le=10000)


class WatchDogTimerEnable(RootModel):
    root: bool


@emitter_router.put("/voltage")
async def put_voltage(voltage: XrayEmitterVoltage) -> XrayEmitterVoltage:
    return voltage


@emitter_router.put("/current")
async def put_current(current: XrayEmitterVoltage) -> XrayEmitterCurrent:
    return current


@emitter_router.put("/watchdog-enable")
async def put_watchdog_timer_enable(
    is_enable: WatchDogTimerEnable,
) -> WatchDogTimerEnable:
    return is_enable
