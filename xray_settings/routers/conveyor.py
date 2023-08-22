import enum

from fastapi import APIRouter
from pydantic import RootModel
from pydantic.types import conint

conveyor_router = APIRouter(prefix="/conveyor", tags=["conveyor"])


class ConveyorVelocity(RootModel):
    root: conint(ge=0, le=255)


class EConveyorDirection(enum.Enum):
    CW = 0
    CCW = 1


class ConveyorDirection(RootModel):
    root: EConveyorDirection


@conveyor_router.put("/voltage", response_model=ConveyorVelocity)
async def put_velocity(velocity: ConveyorVelocity) -> ConveyorVelocity:
    return velocity


@conveyor_router.put("/direction", response_model=ConveyorDirection)
async def put_direction(direction: ConveyorDirection) -> ConveyorDirection:
    return direction
