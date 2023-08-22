from datetime import timedelta

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field, RootModel
from pydantic.types import PositiveInt

image_router = APIRouter(prefix="/image", tags=["image"])


class ImageGenerationSettings(BaseModel):
    maximumImageHeight: PositiveInt = Field(
        description="Unit: pixel (0.4mm) Detector에서 설정할 최대 이미지 높이",
    )
    데이터수집길이: int
    airFactor: PositiveInt = Field(description="X-선 투과 밀도 threshold")
    tuningValue: PositiveInt = Field(description="검사이미지밝기 조정 (분석 전에 이미지 밝기 조정)")


class ImageStoringOptionMultiselect(BaseModel):
    NGImageOriginal: bool = Field(default=True, description="NG 이미지 원본")
    NGImageWithMarking: bool = Field(default=True, description="이물 탐지영역 표시된 NG 이미지")
    normalImage: bool = Field(default=False, description="정상 제품 판정 이미지")


class NGImageRetentionPeriod(RootModel):
    root: timedelta = Field(
        default=timedelta(days=365),
        description="NG 이미지의 보존 기간 설정",
        le=timedelta(days=730),
    )


class ImageInspectionPreviewPostprocessing(BaseModel):
    """
    NG 이미지 혹은 정상이미지를 preview할 때 시인성을 위해 후처리하는 로직을 저장
    """

    model_config = ConfigDict(extra="forbid")

    gamma: int = Field(default=0, description="")
    inversion: int = Field(default=0, description="")
    contrast: int = Field(default=0, description="")
    sharpening: int = Field(default=0, description="")


@image_router.put("/generation-setting")
async def put_generation_setting(
    payload: ImageGenerationSettings,
) -> ImageGenerationSettings:
    return payload


@image_router.put("/storing-option")
async def put_storing_option(
    payload: ImageStoringOptionMultiselect,
) -> ImageStoringOptionMultiselect:
    return payload


@image_router.put("/ng-image-retention-period")
async def put_ng_image_retention_period(
    payload: NGImageRetentionPeriod,
) -> NGImageRetentionPeriod:
    print(payload)
    return payload
