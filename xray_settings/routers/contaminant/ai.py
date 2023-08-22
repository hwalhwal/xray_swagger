import enum

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict

router = APIRouter(prefix="/ai")


class Ambient(enum.IntEnum):
    """
    ### Ambient (식품카테고리)

    - RAW_MEAT = 0
    - PROCESSED_SHELLFISH = 1
    - INSTANT_RICE = 2
    - CANNED_FOOD = 3
    """

    RAW_MEAT = 0
    PROCESSED_SHELLFISH = 1
    INSTANT_RICE = 2
    CANNED_FOOD = 3


class Target(enum.IntEnum):
    """
    ### Target (이물종류)

    - INJECTION_NEEDLES = 0
        - 주사바늘 이외에도, 점, 선 형태의 작은 쇳조각을 포함해서 탐지
    - BONES = 1
    - SEASHELLS = 2
    """

    INJECTION_NEEDLES = 0
    BONES = 1
    SEASHELLS = 2


class AISettingContaminantDetection(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ambient: Ambient
    target: Target


@router.put("/")
async def put(input: AISettingContaminantDetection) -> AISettingContaminantDetection:
    return input
