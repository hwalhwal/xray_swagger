from __future__ import annotations

import enum
from typing import TYPE_CHECKING, Any, Literal, Optional, Union

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field, RootModel
from pydantic.types import conlist
from typing_extensions import Literal

if TYPE_CHECKING:
    from pydantic.main import IncEx

preprocessor_router = APIRouter(prefix="/preprocessor", tags=["preprocessor"])


NoneType = type(None)
Matrix3by3 = conlist(
    item_type=conlist(float, min_length=3, max_length=3),
    min_length=3,
    max_length=3,
)


class MParamBase(BaseModel):
    def model_dump(
        self,
        *,
        mode: str = "python",
        include: IncEx = None,
        exclude: IncEx = None,
        by_alias: bool = False,
        exclude_unset: bool = True,  # Forced
        exclude_defaults: bool = False,
        exclude_none: bool = True,  # Forced
        round_trip: bool = False,
        warnings: bool = True,
    ) -> dict[str, Any]:
        return super().model_dump(
            mode=mode,
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            warnings=warnings,
        )


class MParam_apply_clahe(MParamBase):
    clip_limit: Optional[float] = Field(
        default=None,
        description="CLAHE의 클리핑 한계값. 기본값은 1입니다.",
    )
    tile_grid_size: Optional[
        conlist(item_type=float, min_length=2, max_length=2)
    ] = Field(default=None, description="CLAHE의 타일 그리드 크기. 기본값은 (8, 8)입니다.")


class MParam_apply_unsharp_mask(MParamBase):
    blur_amount: Optional[float] = Field(
        default=None,
        description="블러 강도를 조절하는 매개변수. 기본값은 2.5입니다.",
    )


class MParam_apply_unsharp_mask2(MParamBase):
    blur_sigma: Optional[float] = Field(
        default=None,
        description="블러 시그마 값. 기본값은 1.0입니다.",
    )
    sharpen_strength: Optional[float] = Field(
        default=None,
        description="언샤프 마스크 강도. 기본값은 1.5입니다.",
    )


class MParam_stretch_histogram(RootModel):
    root: NoneType = None


class MParam_denoize(RootModel):
    root: NoneType = None


class MParam_enhance_gray(MParamBase):
    alpha: Optional[float] = Field(
        default=None,
        description="sharpen 강도를 조절하는 매개변수. 기본값은 1.5입니다.",
    )
    beta: Optional[float] = Field(
        default=None,
        description="sharpen 강도를 조절하는 매개변수. 기본값은 -0.5입니다.",
    )
    blur_amount: Optional[int] = Field(
        default=None,
        description="Gaussian blur 강도를 조절하는 매개변수. 기본값은 3입니다.",
    )
    brightness: Optional[int] = Field(
        default=None,
        description="밝기 조절을 위한 값 (0-100). 기본값은 0입니다.",
        ge=0,
        le=100,
    )
    blur_sigma: Optional[float] = Field(
        default=None,
        description="블러 시그마 값. 기본값은 3.2입니다.",
    )
    sharpen_strength: Optional[float] = Field(
        default=None,
        description="언샤프 마스크 강도. 기본값은 1.0입니다.",
    )


class MParam_gaussian_blur(MParamBase):
    kernel_size: Optional[int] = Field(default=None, description="블러 커널 크기. 기본값은 0입니다.")
    blur_amount: Optional[float] = Field(
        default=None,
        description="가우시안 블러 강도를 조절하는 매개변수. 기본값은 3입니다.",
    )


class MParam_equalize(RootModel):
    root: NoneType = None


class MParam_convert_scale(MParamBase):
    alpha: Optional[float] = Field(default=None, description="스케일 매개변수. 기본값은 1.5입니다")
    beta: Optional[float] = Field(default=None, description="밝기 매개변수. 기본값은 30입니다.")


class MParam_adjust_gamma(MParamBase):
    gamma: float = Field(description="조정할 감마값. 기본값은 1.0입니다.")


class MParam_auto_adjust_gamma(MParamBase):
    target_brightness: Optional[int] = Field(
        default=None,
        description="목표 밝기. 기본값은 128입니다.",
    )
    target_gamma: Optional[float] = Field(
        default=None,
        description="목표 감마값. 기본값은 2.5입니다.",
    )
    max_iterations: Optional[int] = Field(
        default=None,
        description="최대 반복 횟수. 기본값은 10입니다.",
    )


class MParam_set_target_brightness(MParamBase):
    target_brightness: int = Field(description="목표 밝기")


class MParam_text_filter(MParamBase):
    kernel_size: Optional[int] = Field(default=None, description="커널 크기. 기본값은 5입니다.")
    blur_amount: Optional[float] = Field(
        default=None,
        description="블러 강도를 조절하는 매개변수. 기본값은 0입니다.",
    )
    alpha: Optional[float] = Field(
        default=None,
        description="원본 이미지와 흐린 이미지의 가중치 조절 매개변수. 기본값은 1.5입니다.",
    )
    beta: Optional[float] = Field(
        default=None,
        description="원본 이미지와 흐린 이미지의 가중치 조절 매개변수. 기본값은 -0.5입니다.",
    )
    gamma: Optional[float] = Field(default=None, description="밝기 조절 매개변수. 기본값은 0입니다.")


class MParam_remove_background(RootModel):
    root: NoneType = None


class MParam_color_inversion(RootModel):
    root: NoneType = None


class MParam_filter_dark_pixels(MParamBase):
    threshold: int = Field(description="밝기 기준값.")


class EColorConversionCodes(enum.IntEnum):
    COLOR_BGR2BGRA = 0
    COLOR_RGB2RGBA = COLOR_BGR2BGRA
    COLOR_BGRA2BGR = 1
    COLOR_RGBA2RGB = COLOR_BGRA2BGR
    COLOR_BGR2RGBA = 2
    COLOR_RGB2BGRA = COLOR_BGR2RGBA
    COLOR_RGBA2BGR = 3
    COLOR_BGRA2RGB = COLOR_RGBA2BGR
    COLOR_BGR2RGB = 4
    COLOR_RGB2BGR = COLOR_BGR2RGB
    COLOR_BGRA2RGBA = 5
    COLOR_RGBA2BGRA = COLOR_BGRA2RGBA
    COLOR_BGR2GRAY = 6
    COLOR_RGB2GRAY = 7
    COLOR_GRAY2BGR = 8
    COLOR_GRAY2RGB = COLOR_GRAY2BGR
    COLOR_GRAY2BGRA = 9
    COLOR_GRAY2RGBA = COLOR_GRAY2BGRA
    COLOR_BGRA2GRAY = 10
    COLOR_RGBA2GRAY = 11
    COLOR_BGR2BGR565 = 12
    COLOR_RGB2BGR565 = 13
    COLOR_BGR5652BGR = 14
    COLOR_BGR5652RGB = 15
    COLOR_BGRA2BGR565 = 16
    COLOR_RGBA2BGR565 = 17
    COLOR_BGR5652BGRA = 18
    COLOR_BGR5652RGBA = 19
    COLOR_GRAY2BGR565 = 20
    COLOR_BGR5652GRAY = 21
    COLOR_BGR2BGR555 = 22
    COLOR_RGB2BGR555 = 23
    COLOR_BGR5552BGR = 24
    COLOR_BGR5552RGB = 25
    COLOR_BGRA2BGR555 = 26
    COLOR_RGBA2BGR555 = 27
    COLOR_BGR5552BGRA = 28
    COLOR_BGR5552RGBA = 29
    COLOR_GRAY2BGR555 = 30
    COLOR_BGR5552GRAY = 31
    COLOR_BGR2XYZ = 32
    COLOR_RGB2XYZ = 33
    COLOR_XYZ2BGR = 34
    COLOR_XYZ2RGB = 35
    COLOR_BGR2YCrCb = 36
    COLOR_RGB2YCrCb = 37
    COLOR_YCrCb2BGR = 38
    COLOR_YCrCb2RGB = 39
    COLOR_BGR2HSV = 40
    COLOR_RGB2HSV = 41
    COLOR_BGR2Lab = 44
    COLOR_RGB2Lab = 45
    COLOR_BGR2Luv = 50
    COLOR_RGB2Luv = 51
    COLOR_BGR2HLS = 52
    COLOR_RGB2HLS = 53
    COLOR_HSV2BGR = 54
    COLOR_HSV2RGB = 55
    COLOR_Lab2BGR = 56
    COLOR_Lab2RGB = 57
    COLOR_Luv2BGR = 58
    COLOR_Luv2RGB = 59
    COLOR_HLS2BGR = 60
    COLOR_HLS2RGB = 61
    COLOR_BGR2HSV_FULL = 66
    COLOR_RGB2HSV_FULL = 67
    COLOR_BGR2HLS_FULL = 68
    COLOR_RGB2HLS_FULL = 69
    COLOR_HSV2BGR_FULL = 70
    COLOR_HSV2RGB_FULL = 71
    COLOR_HLS2BGR_FULL = 72
    COLOR_HLS2RGB_FULL = 73
    COLOR_LBGR2Lab = 74
    COLOR_LRGB2Lab = 75
    COLOR_LBGR2Luv = 76
    COLOR_LRGB2Luv = 77
    COLOR_Lab2LBGR = 78
    COLOR_Lab2LRGB = 79
    COLOR_Luv2LBGR = 80
    COLOR_Luv2LRGB = 81
    COLOR_BGR2YUV = 82
    COLOR_RGB2YUV = 83
    COLOR_YUV2BGR = 84
    COLOR_YUV2RGB = 85
    COLOR_YUV2RGB_NV12 = 90
    COLOR_YUV2BGR_NV12 = 91
    COLOR_YUV2RGB_NV21 = 92
    COLOR_YUV2BGR_NV21 = 93
    COLOR_YUV420sp2RGB = COLOR_YUV2RGB_NV21
    COLOR_YUV420sp2BGR = COLOR_YUV2BGR_NV21
    COLOR_YUV2RGBA_NV12 = 94
    COLOR_YUV2BGRA_NV12 = 95
    COLOR_YUV2RGBA_NV21 = 96
    COLOR_YUV2BGRA_NV21 = 97
    COLOR_YUV420sp2RGBA = COLOR_YUV2RGBA_NV21
    COLOR_YUV420sp2BGRA = COLOR_YUV2BGRA_NV21
    COLOR_YUV2RGB_YV12 = 98
    COLOR_YUV2BGR_YV12 = 99
    COLOR_YUV2RGB_IYUV = 100
    COLOR_YUV2BGR_IYUV = 101
    COLOR_YUV2RGB_I420 = COLOR_YUV2RGB_IYUV
    COLOR_YUV2BGR_I420 = COLOR_YUV2BGR_IYUV
    COLOR_YUV420p2RGB = COLOR_YUV2RGB_YV12
    COLOR_YUV420p2BGR = COLOR_YUV2BGR_YV12
    COLOR_YUV2RGBA_YV12 = 102
    COLOR_YUV2BGRA_YV12 = 103
    COLOR_YUV2RGBA_IYUV = 104
    COLOR_YUV2BGRA_IYUV = 105
    COLOR_YUV2RGBA_I420 = COLOR_YUV2RGBA_IYUV
    COLOR_YUV2BGRA_I420 = COLOR_YUV2BGRA_IYUV
    COLOR_YUV420p2RGBA = COLOR_YUV2RGBA_YV12
    COLOR_YUV420p2BGRA = COLOR_YUV2BGRA_YV12
    COLOR_YUV2GRAY_420 = 106
    COLOR_YUV2GRAY_NV21 = COLOR_YUV2GRAY_420
    COLOR_YUV2GRAY_NV12 = COLOR_YUV2GRAY_420
    COLOR_YUV2GRAY_YV12 = COLOR_YUV2GRAY_420
    COLOR_YUV2GRAY_IYUV = COLOR_YUV2GRAY_420
    COLOR_YUV2GRAY_I420 = COLOR_YUV2GRAY_420
    COLOR_YUV420sp2GRAY = COLOR_YUV2GRAY_420
    COLOR_YUV420p2GRAY = COLOR_YUV2GRAY_420
    COLOR_YUV2RGB_UYVY = 107
    COLOR_YUV2BGR_UYVY = 108
    COLOR_YUV2RGB_Y422 = COLOR_YUV2RGB_UYVY
    COLOR_YUV2BGR_Y422 = COLOR_YUV2BGR_UYVY
    COLOR_YUV2RGB_UYNV = COLOR_YUV2RGB_UYVY
    COLOR_YUV2BGR_UYNV = COLOR_YUV2BGR_UYVY
    COLOR_YUV2RGBA_UYVY = 111
    COLOR_YUV2BGRA_UYVY = 112
    COLOR_YUV2RGBA_Y422 = COLOR_YUV2RGBA_UYVY
    COLOR_YUV2BGRA_Y422 = COLOR_YUV2BGRA_UYVY
    COLOR_YUV2RGBA_UYNV = COLOR_YUV2RGBA_UYVY
    COLOR_YUV2BGRA_UYNV = COLOR_YUV2BGRA_UYVY
    COLOR_YUV2RGB_YUY2 = 115
    COLOR_YUV2BGR_YUY2 = 116
    COLOR_YUV2RGB_YVYU = 117
    COLOR_YUV2BGR_YVYU = 118
    COLOR_YUV2RGB_YUYV = COLOR_YUV2RGB_YUY2
    COLOR_YUV2BGR_YUYV = COLOR_YUV2BGR_YUY2
    COLOR_YUV2RGB_YUNV = COLOR_YUV2RGB_YUY2
    COLOR_YUV2BGR_YUNV = COLOR_YUV2BGR_YUY2
    COLOR_YUV2RGBA_YUY2 = 119
    COLOR_YUV2BGRA_YUY2 = 120
    COLOR_YUV2RGBA_YVYU = 121
    COLOR_YUV2BGRA_YVYU = 122
    COLOR_YUV2RGBA_YUYV = COLOR_YUV2RGBA_YUY2
    COLOR_YUV2BGRA_YUYV = COLOR_YUV2BGRA_YUY2
    COLOR_YUV2RGBA_YUNV = COLOR_YUV2RGBA_YUY2
    COLOR_YUV2BGRA_YUNV = COLOR_YUV2BGRA_YUY2
    COLOR_YUV2GRAY_UYVY = 123
    COLOR_YUV2GRAY_YUY2 = 124
    COLOR_YUV2GRAY_Y422 = COLOR_YUV2GRAY_UYVY
    COLOR_YUV2GRAY_UYNV = COLOR_YUV2GRAY_UYVY
    COLOR_YUV2GRAY_YVYU = COLOR_YUV2GRAY_YUY2
    COLOR_YUV2GRAY_YUYV = COLOR_YUV2GRAY_YUY2
    COLOR_YUV2GRAY_YUNV = COLOR_YUV2GRAY_YUY2
    COLOR_RGBA2mRGBA = 125
    COLOR_mRGBA2RGBA = 126
    COLOR_RGB2YUV_I420 = 127
    COLOR_BGR2YUV_I420 = 128
    COLOR_RGB2YUV_IYUV = COLOR_RGB2YUV_I420
    COLOR_BGR2YUV_IYUV = COLOR_BGR2YUV_I420
    COLOR_RGBA2YUV_I420 = 129
    COLOR_BGRA2YUV_I420 = 130
    COLOR_RGBA2YUV_IYUV = COLOR_RGBA2YUV_I420
    COLOR_BGRA2YUV_IYUV = COLOR_BGRA2YUV_I420
    COLOR_RGB2YUV_YV12 = 131
    COLOR_BGR2YUV_YV12 = 132
    COLOR_RGBA2YUV_YV12 = 133
    COLOR_BGRA2YUV_YV12 = 134
    COLOR_BayerBG2BGR = 46
    COLOR_BayerGB2BGR = 47
    COLOR_BayerRG2BGR = 48
    COLOR_BayerGR2BGR = 49
    COLOR_BayerRGGB2BGR = COLOR_BayerBG2BGR
    COLOR_BayerGRBG2BGR = COLOR_BayerGB2BGR
    COLOR_BayerBGGR2BGR = COLOR_BayerRG2BGR
    COLOR_BayerGBRG2BGR = COLOR_BayerGR2BGR
    COLOR_BayerRGGB2RGB = COLOR_BayerBGGR2BGR
    COLOR_BayerGRBG2RGB = COLOR_BayerGBRG2BGR
    COLOR_BayerBGGR2RGB = COLOR_BayerRGGB2BGR
    COLOR_BayerGBRG2RGB = COLOR_BayerGRBG2BGR
    COLOR_BayerBG2RGB = COLOR_BayerRG2BGR
    COLOR_BayerGB2RGB = COLOR_BayerGR2BGR
    COLOR_BayerRG2RGB = COLOR_BayerBG2BGR
    COLOR_BayerGR2RGB = COLOR_BayerGB2BGR
    COLOR_BayerBG2GRAY = 86
    COLOR_BayerGB2GRAY = 87
    COLOR_BayerRG2GRAY = 88
    COLOR_BayerGR2GRAY = 89
    COLOR_BayerRGGB2GRAY = COLOR_BayerBG2GRAY
    COLOR_BayerGRBG2GRAY = COLOR_BayerGB2GRAY
    COLOR_BayerBGGR2GRAY = COLOR_BayerRG2GRAY
    COLOR_BayerGBRG2GRAY = COLOR_BayerGR2GRAY
    COLOR_BayerBG2BGR_VNG = 62
    COLOR_BayerGB2BGR_VNG = 63
    COLOR_BayerRG2BGR_VNG = 64
    COLOR_BayerGR2BGR_VNG = 65
    COLOR_BayerRGGB2BGR_VNG = COLOR_BayerBG2BGR_VNG
    COLOR_BayerGRBG2BGR_VNG = COLOR_BayerGB2BGR_VNG
    COLOR_BayerBGGR2BGR_VNG = COLOR_BayerRG2BGR_VNG
    COLOR_BayerGBRG2BGR_VNG = COLOR_BayerGR2BGR_VNG
    COLOR_BayerRGGB2RGB_VNG = COLOR_BayerBGGR2BGR_VNG
    COLOR_BayerGRBG2RGB_VNG = COLOR_BayerGBRG2BGR_VNG
    COLOR_BayerBGGR2RGB_VNG = COLOR_BayerRGGB2BGR_VNG
    COLOR_BayerGBRG2RGB_VNG = COLOR_BayerGRBG2BGR_VNG
    COLOR_BayerBG2RGB_VNG = COLOR_BayerRG2BGR_VNG
    COLOR_BayerGB2RGB_VNG = COLOR_BayerGR2BGR_VNG
    COLOR_BayerRG2RGB_VNG = COLOR_BayerBG2BGR_VNG
    COLOR_BayerGR2RGB_VNG = COLOR_BayerGB2BGR_VNG
    COLOR_BayerBG2BGR_EA = 135
    COLOR_BayerGB2BGR_EA = 136
    COLOR_BayerRG2BGR_EA = 137
    COLOR_BayerGR2BGR_EA = 138
    COLOR_BayerRGGB2BGR_EA = COLOR_BayerBG2BGR_EA
    COLOR_BayerGRBG2BGR_EA = COLOR_BayerGB2BGR_EA
    COLOR_BayerBGGR2BGR_EA = COLOR_BayerRG2BGR_EA
    COLOR_BayerGBRG2BGR_EA = COLOR_BayerGR2BGR_EA
    COLOR_BayerRGGB2RGB_EA = COLOR_BayerBGGR2BGR_EA
    COLOR_BayerGRBG2RGB_EA = COLOR_BayerGBRG2BGR_EA
    COLOR_BayerBGGR2RGB_EA = COLOR_BayerRGGB2BGR_EA
    COLOR_BayerGBRG2RGB_EA = COLOR_BayerGRBG2BGR_EA
    COLOR_BayerBG2RGB_EA = COLOR_BayerRG2BGR_EA
    COLOR_BayerGB2RGB_EA = COLOR_BayerGR2BGR_EA
    COLOR_BayerRG2RGB_EA = COLOR_BayerBG2BGR_EA
    COLOR_BayerGR2RGB_EA = COLOR_BayerGB2BGR_EA
    COLOR_BayerBG2BGRA = 139
    COLOR_BayerGB2BGRA = 140
    COLOR_BayerRG2BGRA = 141
    COLOR_BayerGR2BGRA = 142
    COLOR_BayerRGGB2BGRA = COLOR_BayerBG2BGRA
    COLOR_BayerGRBG2BGRA = COLOR_BayerGB2BGRA
    COLOR_BayerBGGR2BGRA = COLOR_BayerRG2BGRA
    COLOR_BayerGBRG2BGRA = COLOR_BayerGR2BGRA
    COLOR_BayerRGGB2RGBA = COLOR_BayerBGGR2BGRA
    COLOR_BayerGRBG2RGBA = COLOR_BayerGBRG2BGRA
    COLOR_BayerBGGR2RGBA = COLOR_BayerRGGB2BGRA
    COLOR_BayerGBRG2RGBA = COLOR_BayerGRBG2BGRA
    COLOR_BayerBG2RGBA = COLOR_BayerRG2BGRA
    COLOR_BayerGB2RGBA = COLOR_BayerGR2BGRA
    COLOR_BayerRG2RGBA = COLOR_BayerBG2BGRA
    COLOR_BayerGR2RGBA = COLOR_BayerGB2BGRA
    COLOR_COLORCVT_MAX = 143


class MParam_cvtColor(MParamBase):
    mode: EColorConversionCodes


class EDDepth(enum.IntEnum):
    CV_8U = 0
    CV_16U = 2
    CV_32F = 5


class MParam_apply_laplacian(MParamBase):
    kernel_size: Optional[int] = Field(
        default=None,
        description="The size of the Laplacian kernel.",
    )
    ddepth: Optional[EDDepth] = Field(
        default=EDDepth.CV_8U,
        description="""
        Depth of the output image. Defaults to cv2.CV_8U.
            - cv2.CV_8U: 8비트 부호 없는 정수 (0 ~ 255 범위)
            - cv2.CV_16U: 16비트 부호 있는 정수
            - cv2.CV_32F: 32비트 부동 소수점""",
    )


class ESharpeningFilterKernelType(enum.IntEnum):
    UNSHARP_MASK = 1
    LAPLACIAN = 2
    MEAN = 3
    GAUSSIAN = 4
    SOBEL_X = 5
    SOBEL_Y = 6
    EMBOSSING = 7


class MParam_apply_sharpening_filter(MParamBase):
    kernel_type: ESharpeningFilterKernelType = Field(
        description="The type of sharpening kernel to use.",
    )
    append_kernel: Optional[bool] = Field(
        default=None,
        description="If True, appends the new_kernel to the filter before applying. Defaults to False.",
    )
    new_kernel: Optional[Matrix3by3] = Field(
        default=None,
        description="A custom sharpening kernel to use. Required if append_kernel is True.",
    )
    divide: Optional[float] = Field(
        default=None,
        description="Value to divide the kernel by.",
    )


############################################################


class FunctionSignatureBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    filter_name: str
    params: NoneType = None


class ApplyClahe(FunctionSignatureBase):
    """
    이미지에 CLAHE (Contrast Limited Adaptive Histogram Equalization)를 적용합니다.
    """

    filter_name: Literal["apply_clahe"]
    params: MParam_apply_clahe


class ApplyUnsharpMask(FunctionSignatureBase):
    """
    이미지에 언샤프 마스크(Unsharp Masking)를 적용하여 선명도를 향상시킵니다.
    """

    filter_name: Literal["apply_unsharp_mask"]
    params: MParam_apply_unsharp_mask


class ApplyUnsharpMask2(FunctionSignatureBase):
    """
    이미지에 언샤프 마스크(Unsharp Masking)를 적용하여 선명도를 향상시킵니다.
    """

    filter_name: Literal["apply_unsharp_mask2"]
    params: MParam_apply_unsharp_mask2


class StretchHistogram(FunctionSignatureBase):
    """
    이미지의 히스토그램을 스트레칭하여 대비를 향상시킵니다.
    """

    filter_name: Literal["stretch_histogram"]
    params: MParam_stretch_histogram


class Denoize(FunctionSignatureBase):
    """
    이미지의 잡음(noise)을 제거합니다. (굉장히 오래 걸림)
    """

    filter_name: Literal["denoize"]
    params: MParam_denoize


class EnhanceGray(FunctionSignatureBase):
    """
    주어진 이미지를 흑백 이미지로 변환한 후 sharpen 및 brightness 조절을 수행합니다.
    """

    filter_name: Literal["enhance_gray"]
    params: MParam_enhance_gray


class GaussianBlur(FunctionSignatureBase):
    """
    이미지에 가우시안 블러(Gaussian blur)를 적용하여 smoothing합니다.
    """

    filter_name: Literal["gaussian_blur"]
    params: MParam_gaussian_blur


class Equalize(FunctionSignatureBase):
    """
    이미지에 히스토그램 평활화(Histogram Equalization)를 적용하여 대비를 향상시킵니다.
    """

    filter_name: Literal["equalize"]
    params: MParam_equalize


class ConvertScale(FunctionSignatureBase):
    """
    이미지의 스케일을 조정하고 밝기를 변경합니다.
    """

    filter_name: Literal["convert_scale"]
    params: MParam_convert_scale


class AdjustGamma(FunctionSignatureBase):
    """
    이미지의 감마값을 조정하여 밝기를 변경합니다.
    """

    filter_name: Literal["adjust_gamma"]
    params: MParam_adjust_gamma


class AutoAdjustGamma(FunctionSignatureBase):
    """
    주어진 이미지의 감마값과 밝기를 자동으로 조정합니다.
    """

    filter_name: Literal["auto_adjust_gamma"]
    params: MParam_auto_adjust_gamma


class SetTargetBrightness(FunctionSignatureBase):
    """
    주어진 이미지의 목표 밝기를 설정합니다.
    """

    filter_name: Literal["set_target_brightness"]
    params: MParam_set_target_brightness


class TextFilter(FunctionSignatureBase):
    """
    주어진 이미지에 텍스트 필터를 적용하여 뚜렷한 글자를 얻습니다.
    """

    filter_name: Literal["text_filter"]
    params: MParam_text_filter


class RemoveBackground(FunctionSignatureBase):
    """
    주어진 이미지의 배경을 제거합니다.
    """

    filter_name: Literal["remove_background"]
    params: MParam_remove_background


class ColorInversion(FunctionSignatureBase):
    """
    주어진 이미지의 색상을 반전시킵니다.
    """

    filter_name: Literal["color_inversion"]
    params: MParam_color_inversion


class FilterDarkPixels(FunctionSignatureBase):
    """
    주어진 이미지에서 일정 밝기 이하인 픽셀을 필터링합니다.
    """

    filter_name: Literal["filter_dark_pixels"]
    params: MParam_filter_dark_pixels


class CvtColor(FunctionSignatureBase):
    """
    Convert the color space of the input image using OpenCV's cvtColor function.
    """

    filter_name: Literal["cvtColor"]
    params: MParam_cvtColor


class ApplyLaplacian(FunctionSignatureBase):
    """
    Apply Laplacian edge detection to the input image.
    """

    filter_name: Literal["apply_laplacian"]
    params: MParam_apply_laplacian


class ApplySharpeningFilter(FunctionSignatureBase):
    """
    Apply a sharpening filter to an input image using the specified kernel.
    """

    filter_name: Literal["apply_sharpening_filter"]
    params: MParam_apply_sharpening_filter


#################################################

# fmt: off
PreprocCascadingFunctionItem = Union[
    ApplyClahe, ApplyUnsharpMask, ApplyUnsharpMask2,
    StretchHistogram, Denoize, EnhanceGray, GaussianBlur,
    Equalize, ConvertScale, AdjustGamma, AutoAdjustGamma,
    SetTargetBrightness, TextFilter, RemoveBackground,
    ColorInversion, FilterDarkPixels, CvtColor,
    ApplyLaplacian, ApplySharpeningFilter,
]
# fmt: on


class PreprocessorCascadingFunctionSetting(BaseModel):
    functions: conlist(item_type=PreprocCascadingFunctionItem, max_length=10)


class PreprocessorCascadingFunctionSet(RootModel):
    root: dict[str, PreprocessorCascadingFunctionSetting]


@preprocessor_router.put(
    "/cascading",
    response_model_exclude_none=True,
    response_model_exclude_unset=True,
)
async def put_setting(
    payload: PreprocessorCascadingFunctionSet,
) -> PreprocessorCascadingFunctionSet:
    return payload
    # return payload.model_dump(exclude_unset=True, exclude_none=True)
