import enum

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict

router = APIRouter(prefix="/contour", tags=["contour"])


class EContourMode(enum.IntEnum):
    INNER = 0
    OUTER = 1


class EContourShape(enum.IntEnum):
    RECTANGLE = 0
    ELLIPSE = 1
    POLYGON = 3
    ORIGINAL = 4


class ContourDetectionSetting(BaseModel):
    model_config = ConfigDict(extra="forbid")

    enabled: bool = False
    mode: EContourMode = EContourMode.OUTER
    shape: EContourShape = EContourShape.POLYGON


@router.put("/")
async def put_setting(input: ContourDetectionSetting) -> ContourDetectionSetting:
    return input
