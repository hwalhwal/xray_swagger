import enum

from fastapi import APIRouter
from pydantic import BaseModel, Field, RootModel

inspection_router = APIRouter(prefix="/inspection", tags=["inspection"])


class EInspectionMode(enum.Enum):
    """
    ### 검사모드

    - 표준검사
        - 제품에 설정된 설정값을 그대로 이용
    - Test 모드
        - 검사 이미지 저장 경로가 달라짐.
            - 표준검사: `../XFoodData/image`
            - Test모드: `../XFoodData/image_TEST_MODE`
    - 설정모드
        - 제품 설정값 없이 진행. 새 제품에 대해 테스트해볼 경우 사용
            - 제품 설정값이 특정 프리셋에 저장되지 않는 것일 뿐이지, 어딘가에서 설정값을 불러오거나 해야 할 것임.
    """

    DEFAULT = 0
    TEST = 1
    SETTING = 2


class InspectionMode(RootModel):
    root: EInspectionMode


class EInspectionMethod(enum.Enum):
    """
    ### 검사방법

    **NG발생에 대한 벨트 정지 조건을 설정하는 기능**

    - 제품연속흐름
        - 이물 발견해도 x-ray 장치들 및 컨베이어는 멈추지 않고 `리젝터`를 사용하여 이물혼입 제품을 걸러낸다
    - 1회검사
        - 제품 이물 발견 시마다 x-ray 장치들 및 컨베이어가 중지된다.
            - 1회검사 이미지 저장 옵션
                - NG 발생 시에만 검사 종료
                - 제품 1회 통과시 무조건 검사종료
    """

    USE_REJECTOR = 0
    STOP_ON_NG_EVENT = 1


class InspectionMethod(RootModel):
    root: EInspectionMethod


class EContaminantInspectionMode(enum.IntEnum):
    """
    이물검사 모드

    - NO_CONTAMINANT_INSPECTION = 0
    - RULE_BASED = 1
    - AI = 2
    """

    NO_CONTAMINANT_INSPECTION = 0
    RULE_BASED = 1
    AI = 2


class InspectionItemMultiselect(BaseModel):
    """
    ### 검사 항목

    - 이물검사
    - 결품검사
    - 파손검사
    - 금속탐지
    """

    contaminant: EContaminantInspectionMode = Field(
        default=EContaminantInspectionMode.NO_CONTAMINANT_INSPECTION,
    )
    missingItem: bool = Field(default=False, description="결품검사")
    damagedItem: bool = Field(default=False, description="파손검사")
    metalDetect: bool = Field(default=False, description="금속탐지")


@inspection_router.put("/mode")
async def put_mode(mode: InspectionMode) -> InspectionMode:
    return mode


@inspection_router.put("/method")
async def put_method(method: InspectionMethod) -> InspectionMethod:
    return method


@inspection_router.put("/item-multiselect")
async def put_item_multiselect(
    item: InspectionItemMultiselect,
) -> InspectionItemMultiselect:
    return item
