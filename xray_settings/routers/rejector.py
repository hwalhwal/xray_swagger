from fastapi import APIRouter
from pydantic import RootModel
from pydantic.types import conint

rejector_router = APIRouter(prefix="/rejector", tags=["rejector"])


class RejectorDelayMS(RootModel):
    root: conint(ge=0, le=10000)


class RejectorOpenMS(RootModel):
    root: conint(ge=0, le=10000)


@rejector_router.put("/delay", response_model=RejectorDelayMS)
async def put_delay(delay: RejectorDelayMS) -> RejectorDelayMS:
    return delay


@rejector_router.put("/open", response_model=RejectorOpenMS)
async def put_open(open: RejectorOpenMS) -> RejectorOpenMS:
    return open
