from typing import Literal, Union

import xray_settings.docstrings as docstrings
from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field
from pydantic.types import PositiveInt, confloat, conint, conlist
from xray_settings.x import AuthLevel, validate_input

rule_router = APIRouter(prefix="/rules")

# class RuleDetectParamBase(BaseModel):
#     ...


class AlatHP(BaseModel):
    __doc__ = docstrings.AlatHPDocstring_KO
    model_config = ConfigDict(extra="forbid")

    ReduceValue: PositiveInt = Field(
        title="Reduce Value",
        description=docstrings.ReduceValueDocstring_KO,
        ge=1,
        le=255,
        default=20,
    )
    SmoothingDim: PositiveInt = Field(
        title="Smoothing Dim",
        description=docstrings.SmoothingDimDocstring_KO,
        default=3,
    )
    HipassFilterDim: PositiveInt = Field(
        title="Hipass Filter Dim",
        description=docstrings.HipassFilterDimDocstring_KO,
        ge=1,
        le=255,
        default=9,
        json_schema_extra={"not": {"multipleOf": 2}},
    )
    SmthDim: int = Field(
        title="Smth Dim",
        description=docstrings.SmthDimDocstring_KO,
        default=5,
    )
    SmThThreshold: PositiveInt = Field(
        title="SmTh Threshold",
        description=docstrings.SmthThresholdDocstring_KO,
        ge=1,
        le=255,
        default=80,
    )
    DetectionThreshold: int = Field(
        title="Detection Threshold",
        description=docstrings.DetectionThresholdDocstring_KO,
        default=10,
    )
    DetectionArea: int = Field(
        title="Detection Area",
        description=docstrings.DetectionAreaDocstring_KO,
    )
    MaskValue: conlist(confloat(strict=True, ge=0.0, lt=1.0), min_length=4, max_length=4) = Field(
        title="Mask Value",
        description=docstrings.MaskValueDocstring_KO,
    )


class Al003e(BaseModel):
    __doc__ = docstrings.Al003eDocstring_KO
    model_config = ConfigDict(extra="forbid")

    Reduction1Threshold: PositiveInt = Field(
        title="Reduction1 Threshold",
        description=docstrings.Reduction1ThresholdDocstring_KO,
        ge=1,
        le=255,
        default=80,
    )
    SmoothingDim: PositiveInt = Field(
        title="Smoothing Dim",
        description=docstrings.SmoothingDimDocstring_KO,
        default=3,
    )
    HipassFilterDim: PositiveInt = Field(
        title="Hipass Filter Dim",
        description=docstrings.HipassFilterDimDocstring_KO,
        ge=1,
        le=255,
        default=9,
        json_schema_extra={"not": {"multipleOf": 2}},
    )
    ErodeDim: PositiveInt = Field(
        title="Erode Dim",
        description=docstrings.ErodeDimDocstring_KO,
        ge=1,
        le=255,
        default=3,
    )
    BinaryThreshold: PositiveInt = Field(
        title="Binary Threshold",
        description=docstrings.BinaryThresholdDocstring_KO,
        ge=1,
        le=255,
    )
    ErodeThreshold: PositiveInt = Field(
        title="Erode Threshold",
        description=docstrings.ErodeThresholdDocstring_KO,
        # ge=1, le=255,
        default=5,
    )
    DilateDim: PositiveInt = Field(
        title="Dilate Dim",
        description=docstrings.DilateDimDocstring_KO,
        # ge=1, le=255,
        default=3,
    )
    DetectionThreshold: int = Field(
        title="Detection Threshold",
        description=docstrings.DetectionThresholdDocstring_KO,
        default=10,
    )
    DetectionArea: int = Field(
        title="Detection Area",
        description=docstrings.DetectionAreaDocstring_KO,
    )
    MaskValue: conlist(confloat(strict=True, ge=0.0, lt=1.0), min_length=4, max_length=4) = Field(
        title="Mask Value",
        description=docstrings.MaskValueDocstring_KO,
    )


class Aldong1(BaseModel):
    __doc__ = docstrings.Aldong1Docstring_KO
    model_config = ConfigDict(extra="forbid")

    ReduceValue: PositiveInt = Field(
        title="Reduce Value",
        description=docstrings.ReduceValueDocstring_KO,
        ge=1,
        le=255,
        default=170,
    )
    SmoothingDim: PositiveInt = Field(
        title="Smoothing Dim",
        description=docstrings.SmoothingDimDocstring_KO,
        default=5,
    )
    MultiplyValue: PositiveInt = Field(
        title="Multiply Value",
        description=docstrings.MultiplyValueDocstring_KO,
        default=3,
    )
    HipassFilterDim: PositiveInt = Field(
        title="Hipass Filter Dim",
        description=docstrings.HipassFilterDimDocstring_KO,
        ge=1,
        le=255,
        default=9,
        json_schema_extra={"not": {"multipleOf": 2}},
    )
    OZFThreshold: PositiveInt = Field(
        title="OZF Threshold",
        description=docstrings.OZFThresholdDocstring_KO,
        # ge=1, le=255,
        default=3,
    )
    BinaryThreshold: PositiveInt = Field(
        title="Binary Threshold",
        description=docstrings.BinaryThresholdDocstring_KO,
        ge=1,
        le=255,
        default=80,
    )
    DetectionThreshold: int = Field(
        title="Detection Threshold",
        description=docstrings.DetectionThresholdDocstring_KO,
        default=10,
    )
    DetectionArea: int = Field(
        title="Detection Area",
        description=docstrings.DetectionAreaDocstring_KO,
    )
    MaskValue: conlist(confloat(strict=True, ge=0.0, lt=1.0), min_length=4, max_length=4) = Field(
        title="Mask Value",
        description=docstrings.MaskValueDocstring_KO,
    )


RuleDetectParamBase = Union[AlatHP, Al003e, Aldong1]


class RuleDetectSettingTemplate(BaseModel):
    exec_order: conint(gt=0, le=6)
    algorithm_name: Literal["AlatHP", "Al003e", "Aldong1"]
    parameters: RuleDetectParamBase


class SettingsProductParameter(BaseModel):
    setting_param_name: str
    authlevel: AuthLevel
    setting_template: RuleDetectSettingTemplate


@rule_router.put("/", response_model=SettingsProductParameter)
async def put_rule(input: dict) -> SettingsProductParameter:
    print(input)
    setting_param_name = input["setting_param_name"]
    authlevel = input["authlevel"]
    setting_template = input["setting_template"]
    algorithm_name = setting_template["algorithm_name"]
    parameters = setting_template["parameters"]

    match algorithm_name:
        case "AlatHP":
            await validate_input(parameters, AlatHP)
        case "Al003e":
            await validate_input(parameters, Al003e)
        case "Aldong1":
            await validate_input(parameters, Aldong1)

    await validate_input(input, SettingsProductParameter)

    return SettingsProductParameter(
        setting_param_name=setting_param_name,
        authlevel=authlevel,
        setting_template=setting_template,
    )


# Preproc.AIDetect
# Preproc.Contour

# RuleDetect


@rule_router.post("/alathp/", response_model=AlatHP)
async def create_alathp(input: dict) -> AlatHP:
    print(input)
    await validate_input(input, AlatHP)
    return AlatHP(**input)


@rule_router.post("/al003e/", response_model=Al003e)
async def create_al003e(input: dict) -> Al003e:
    print(input)
    await validate_input(input, Al003e)
    return Al003e(**input)


@rule_router.post("/aldong1/", response_model=Aldong1)
async def create_aldong1(input: dict) -> Aldong1:
    print(input)
    await validate_input(input, Aldong1)
    return Aldong1(**input)
