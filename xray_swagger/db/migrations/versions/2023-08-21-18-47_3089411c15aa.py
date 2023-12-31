"""Filling fixture

Revision ID: 3089411c15aa
Revises: 633298a57b8a
Create Date: 2023-08-21 18:47:02.613344

"""
import uuid
import sqlalchemy as sa
from alembic import op

from datetime import datetime
from pydantic_extra_types.phone_numbers import PhoneNumber

from xray_swagger.db.models.settings import SettingsGlobal, SettingsProductParameter
from xray_swagger.db.models.user import User, AuthLevel
from xray_swagger.db.models.peripherals import Device
from xray_swagger.db.models.mmap_session import MmapSession

from xray_swagger.db.models.product import Product, InspectionSession
from xray_swagger.db.models.defect import Defect, DefectCategory

from xray_settings.routers.emitter import (
    WatchDogTimerEnable,
    XrayEmitterVoltage,
    XrayEmitterCurrent,
)
from xray_settings.routers.conveyor import ConveyorDirection, ConveyorVelocity
from xray_settings.routers.inspections import (
    InspectionMode,
    InspectionMethod,
    InspectionItemMultiselect,
)
from xray_settings.routers.contaminant.ai import AISettingContaminantDetection
from xray_settings.routers.contaminant.rule import RuleDetectSettingTemplate
from xray_settings.routers.rejector import RejectorDelayMS, RejectorOpenMS
from xray_settings.routers.image import (
    ImageGenerationSettings,
    ImageStoringOptionMultiselect,
    ImageInspectionPreviewPostprocessing,
)
from xray_settings.routers.preprocessor import PreprocessorCascadingFunctionSet
from xray_settings.routers.contour import ContourDetectionSetting


# revision identifiers, used by Alembic.
revision = "3089411c15aa"
down_revision = "633298a57b8a"
branch_labels = None
depends_on = None

conn = op.get_bind()
meta = sa.MetaData()
meta.reflect(bind=conn)


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###

    #  !!!!!!!!!!!!!!!   WARNINGS    !!!!!!!!!!!!!!!
    # `autoincrement` 필드에 대해서 삽입할 경우 해당 필드 지정하지 말 것.
    # Postgresql에서는 지정하는 경우 *_id_seq 값이 증가하지 않아 추후 duplicate 에러 발생.

    print(f"{User.__table__} bulk insert")
    op.bulk_insert(
        sa.Table(User.__table__, meta, autoload_with=conn),
        [
            {
                "username": "engineer",
                "password": "88946",
                "fullname": "Gobang Kim",
                "phone_number": PhoneNumber._validate("+821066214454", None),
                "company": "Soluray",
                "job_title": "Tech Lead",
                "joined_at": datetime.utcnow(),
                "authlevel": AuthLevel.ENGINEER.name,
            },
            {
                "username": "admin",
                "password": "1234",
                "fullname": "DaMent",
                "phone_number": PhoneNumber._validate("+821980126658", None),
                "company": "HeteroDoc",
                "job_title": "demand",
                "joined_at": datetime.utcnow(),
                "authlevel": AuthLevel.SUPERVISOR.name,
            },
            {
                "username": "operator",
                "password": "4321",
                "fullname": "김상용",
                "phone_number": PhoneNumber._validate("+821066458155", None),
                "company": "Siemens",
                "job_title": "worker",
                "joined_at": datetime.utcnow(),
                "authlevel": AuthLevel.OPERATOR.name,
            },
        ],
        multiinsert=False,
    )
    conn.commit()
    print(f"{SettingsGlobal.__table__} bulk insert")
    op.bulk_insert(
        sa.Table(SettingsGlobal.__table__, meta, autoload_with=conn),
        [
            {
                "setting_param_name": "Watchdog.Timer",
                "creator_id": 1,
                "last_editor_id": 1,
                "authlevel": AuthLevel.ENGINEER.name,
                "json_schema": WatchDogTimerEnable.model_json_schema(),
                "value": True,
            },
            {
                "setting_param_name": "Conveyor.Direction",
                "creator_id": 1,
                "last_editor_id": 1,
                "authlevel": AuthLevel.ENGINEER.name,
                "json_schema": ConveyorDirection.model_json_schema(),
                "value": 1,
            },
            {
                "setting_param_name": "Inspection.Mode",
                "creator_id": 1,
                "last_editor_id": 1,
                "authlevel": AuthLevel.SUPERVISOR.name,
                "json_schema": InspectionMode.model_json_schema(),
                "value": 1,
            },
        ],
    )
    print(f"{Device.__table__} bulk insert")
    op.bulk_insert(
        sa.Table(Device.__table__, meta, autoload_with=conn),
        [
            {
                "name": "Detector",
                "model_series": "X-scan 0.4C5-410-USB",
                "code": "XD410",
                "manufacturer": "Detection Technology",
                "specifications": {"wow": 0},
            },
            {
                "name": "Detector",
                "model_series": "X-scan 0.4C5-614-USB",
                "code": "XD614",
                "manufacturer": "Detection Technology",
                "specifications": {"wow": 0},
            },
            {
                "name": "Emitter",
                "model_series": "XRB80P&N100X5708 / 100W",
                "code": "XE5708W100",
                "manufacturer": "Spellman High Voltage",
                "specifications": None,
            },
            {
                "name": "Emitter",
                "model_series": "XRB80P&N200X3921 / 200W",
                "code": "XE3921W200",
                "manufacturer": "Spellman High Voltage",
                "specifications": None,
            },
            {
                "name": "Emitter",
                "model_series": "XRB160P&N480X4301 / 480W",
                "code": "XE4301W480",
                "manufacturer": "Spellman High Voltage",
                "specifications": None,
            },
        ],
    )
    print(f"{SettingsProductParameter.__table__} bulk insert")
    op.bulk_insert(
        sa.Table(SettingsProductParameter.__table__, meta, autoload_with=conn),
        [
            {
                "setting_param_name": "XrayEmitter.Voltage",
                "authlevel": AuthLevel.SUPERVISOR.name,
                "json_schema": XrayEmitterVoltage.model_json_schema(),
            },
            {
                "setting_param_name": "XrayEmitter.Current",
                "authlevel": AuthLevel.SUPERVISOR.name,
                "json_schema": XrayEmitterCurrent.model_json_schema(),
            },
            {
                "setting_param_name": "Conveyor.Velocity",
                "authlevel": AuthLevel.SUPERVISOR.name,
                "json_schema": ConveyorVelocity.model_json_schema(),
            },
            {
                "setting_param_name": "Rejector.DelayMS",
                "authlevel": AuthLevel.SUPERVISOR.name,
                "json_schema": RejectorDelayMS.model_json_schema(),
            },
            {
                "setting_param_name": "Rejector.OpenMS",
                "authlevel": AuthLevel.SUPERVISOR.name,
                "json_schema": RejectorOpenMS.model_json_schema(),
            },
            {
                "setting_param_name": "Inspection.Method",
                "authlevel": AuthLevel.SUPERVISOR.name,
                "json_schema": InspectionMethod.model_json_schema(),
            },
            {
                "setting_param_name": "Inspection.Item",
                "authlevel": AuthLevel.SUPERVISOR.name,
                "json_schema": InspectionItemMultiselect.model_json_schema(),
            },
            {
                "setting_param_name": "Inspection.Contaminant.AI",
                "authlevel": AuthLevel.SUPERVISOR.name,
                "json_schema": AISettingContaminantDetection.model_json_schema(),
            },
            {
                "setting_param_name": "Inspection.Contaminant.RuleBased",
                "authlevel": AuthLevel.SUPERVISOR.name,
                "json_schema": RuleDetectSettingTemplate.model_json_schema(),
            },
            {
                "setting_param_name": "Image.GenerationSettings",
                "authlevel": AuthLevel.SUPERVISOR.name,
                "json_schema": ImageGenerationSettings.model_json_schema(),
            },
            {
                "setting_param_name": "Image.StoringOption",
                "authlevel": AuthLevel.SUPERVISOR.name,
                "json_schema": ImageStoringOptionMultiselect.model_json_schema(),
            },
            {
                "setting_param_name": "Image.InspectionPreviewPostprocessing",
                "authlevel": AuthLevel.SUPERVISOR.name,
                "json_schema": ImageInspectionPreviewPostprocessing.model_json_schema(),
            },
            {
                "setting_param_name": "Preprocessor.Cascading",
                "authlevel": AuthLevel.SUPERVISOR.name,
                "json_schema": PreprocessorCascadingFunctionSet.model_json_schema(),
            },
            {
                "setting_param_name": "Contour",
                "authlevel": AuthLevel.SUPERVISOR.name,
                "json_schema": ContourDetectionSetting.model_json_schema(),
            },
        ],
    )
    print(f"{MmapSession.__table__} bulk insert")
    mmssuuid01 = uuid.uuid4()
    mmssuuid02 = uuid.uuid4()
    mmssuuid03 = uuid.uuid4()
    mmssuuid04 = uuid.uuid4()
    op.bulk_insert(
        sa.Table(MmapSession.__table__, meta, autoload_with=conn),
        [
            {
                "uuid": mmssuuid01, "image_s3_key": f"mmap/session/{mmssuuid01}",
                "session_started_at": datetime.fromisoformat("2023-08-29T00:00:00.000001"),
                "session_ended_at":   datetime.fromisoformat("2023-08-29T00:01:00.000001"),
                "is_preserved": True,
            },
            {
                "uuid": mmssuuid02, "image_s3_key": f"mmap/session/{mmssuuid02}",
                "session_started_at": datetime.fromisoformat("2023-08-29T00:01:00.000001"),
                "session_ended_at":   datetime.fromisoformat("2023-08-29T00:02:00.000001"),
                "is_preserved": True,
            },
            {
                "uuid": mmssuuid03, "image_s3_key": f"mmap/session/{mmssuuid03}",
                "session_started_at": datetime.fromisoformat("2023-08-29T00:02:00.000001"),
                "session_ended_at":   datetime.fromisoformat("2023-08-29T00:03:00.000001"),
                "is_preserved": True,
            },
            {
                "uuid": mmssuuid04, "image_s3_key": f"mmap/session/{mmssuuid04}",
                "session_started_at": datetime.fromisoformat("2023-08-29T00:03:00.000001"),
                "session_ended_at":   datetime.fromisoformat("2023-08-29T00:04:00.000001"),
                "is_preserved": True,
            },
        ]
    )
    ###############################################################
    print(f"{Product.__table__} bulk insert")
    op.bulk_insert(
        sa.Table(Product.__table__, meta, autoload_with=conn),
        [{"name": "닭가슴살팩", "creator_id": 2, "last_editor_id": 2},
         {"name": "육고기통조림", "creator_id": 2, "last_editor_id": 2},
         {"name": "곤약덩어리", "creator_id": 2, "last_editor_id": 2},],
    )
    print(f"{InspectionSession.__table__} bulk insert")
    op.bulk_insert(
        sa.Table(InspectionSession.__table__, meta, autoload_with=conn),
        [
            {"product_id": 1, "image_s3_key": "prod/inspect/000001",
             "session_started_at": datetime.fromisoformat("2023-08-29T00:00:00.000001"),
             "session_ended_at":   datetime.fromisoformat("2023-08-29T00:00:02.000001"),
             "start_mmap_session_uuid": mmssuuid01,
             "end_mmap_session_uuid": mmssuuid01,
             "start_mmap_session_ptr": 0,
             "end_mmap_session_ptr": 1000,
            },
            {"product_id": 1, "image_s3_key": "prod/inspect/000002",
             "session_started_at": datetime.fromisoformat("2023-08-29T00:00:02.000001"),
             "session_ended_at":   datetime.fromisoformat("2023-08-29T00:00:04.000001"),
             "start_mmap_session_uuid": mmssuuid01,
             "end_mmap_session_uuid": mmssuuid01,
             "start_mmap_session_ptr": 1000,
             "end_mmap_session_ptr": 1500,
            },
            {"product_id": 1, "image_s3_key": "prod/inspect/000003",
             "session_started_at": datetime.fromisoformat("2023-08-29T00:00:04.000001"),
             "session_ended_at":   datetime.fromisoformat("2023-08-29T00:00:06.000001"),
             "start_mmap_session_uuid": mmssuuid01,
             "end_mmap_session_uuid": mmssuuid01,
             "start_mmap_session_ptr": 1500,
             "end_mmap_session_ptr": 3000,
            },
            {"product_id": 1, "image_s3_key": "prod/inspect/000004",
             "session_started_at": datetime.fromisoformat("2023-08-29T00:00:06.000001"),
             "session_ended_at":   datetime.fromisoformat("2023-08-29T00:00:09.000001"),
             "start_mmap_session_uuid": mmssuuid01,
             "end_mmap_session_uuid": mmssuuid01,
             "start_mmap_session_ptr": 3000,
             "end_mmap_session_ptr": 6000,
            },
            {"product_id": 1, "image_s3_key": "prod/inspect/000005",
             "session_started_at": datetime.fromisoformat("2023-08-29T00:00:09.000001"),
             "session_ended_at":   datetime.fromisoformat("2023-08-29T00:00:12.000001"),
             "start_mmap_session_uuid": mmssuuid01,
             "end_mmap_session_uuid": mmssuuid01,
             "start_mmap_session_ptr": 6000,
             "end_mmap_session_ptr": 8000,
            },
            {"product_id": 1, "image_s3_key": "prod/inspect/000006",
             "session_started_at": datetime.fromisoformat("2023-08-29T00:00:12.000001"),
             "session_ended_at":   datetime.fromisoformat("2023-08-29T00:00:14.000001"),
             "start_mmap_session_uuid": mmssuuid01,
             "end_mmap_session_uuid": mmssuuid01,
             "start_mmap_session_ptr": 8000,
             "end_mmap_session_ptr": 9000,
            },
            {"product_id": 1, "image_s3_key": "prod/inspect/000007",
             "session_started_at": datetime.fromisoformat("2023-08-29T00:00:14.000001"),
             "session_ended_at":   datetime.fromisoformat("2023-08-29T00:00:18.000001"),
             "start_mmap_session_uuid": mmssuuid01,
             "end_mmap_session_uuid": mmssuuid01,
             "start_mmap_session_ptr": 9000,
             "end_mmap_session_ptr": 12000,
            },
            ###
            {"product_id": 2, "image_s3_key": "prod/inspect/000008",
             "session_started_at": datetime.fromisoformat("2023-08-29T00:01:00.000001"),
             "session_ended_at":   datetime.fromisoformat("2023-08-29T00:01:02.000001"),
             "start_mmap_session_uuid": mmssuuid02,
             "end_mmap_session_uuid": mmssuuid02,
             "start_mmap_session_ptr": 0,
             "end_mmap_session_ptr": 1000,
            },
            {"product_id": 2, "image_s3_key": "prod/inspect/000009",
             "session_started_at": datetime.fromisoformat("2023-08-29T00:01:02.000001"),
             "session_ended_at":   datetime.fromisoformat("2023-08-29T00:01:08.000001"),
             "start_mmap_session_uuid": mmssuuid02,
             "end_mmap_session_uuid": mmssuuid02,
             "start_mmap_session_ptr": 1000,
             "end_mmap_session_ptr": 3000,
            },
            {"product_id": 2, "image_s3_key": "prod/inspect/000010",
             "session_started_at": datetime.fromisoformat("2023-08-29T00:01:08.000001"),
             "session_ended_at":   datetime.fromisoformat("2023-08-29T00:01:14.000001"),
             "start_mmap_session_uuid": mmssuuid02,
             "end_mmap_session_uuid": mmssuuid02,
             "start_mmap_session_ptr": 3000,
             "end_mmap_session_ptr": 4000,
            },
            ##
            {"product_id": 3, "image_s3_key": "prod/inspect/000011",
             "session_started_at": datetime.fromisoformat("2023-08-29T00:02:08.000001"),
             "session_ended_at":   datetime.fromisoformat("2023-08-29T00:02:14.000001"),
             "start_mmap_session_uuid": mmssuuid03,
             "end_mmap_session_uuid": mmssuuid03,
             "start_mmap_session_ptr": 6000,
             "end_mmap_session_ptr": 9000,
            },
            {"product_id": 3, "image_s3_key": "prod/inspect/000012",
             "session_started_at": datetime.fromisoformat("2023-08-29T00:02:14.000001"),
             "session_ended_at":   datetime.fromisoformat("2023-08-29T00:02:20.000001"),
             "start_mmap_session_uuid": mmssuuid03,
             "end_mmap_session_uuid": mmssuuid03,
             "start_mmap_session_ptr": 9000,
             "end_mmap_session_ptr": 12000,
            },
            {"product_id": 3, "image_s3_key": "prod/inspect/000013",
             "session_started_at": datetime.fromisoformat("2023-08-29T00:02:56.000001"),
             "session_ended_at":   datetime.fromisoformat("2023-08-29T00:03:01.000001"),
             "start_mmap_session_uuid": mmssuuid03,
             "end_mmap_session_uuid": mmssuuid04,
             "start_mmap_session_ptr": 35600,
             "end_mmap_session_ptr": 300,
            },
        ]
    )
    print(f"{Defect.__table__} bulk insert")
    op.bulk_insert(
        sa.Table(Defect.__table__, meta, autoload_with=conn),
        [
            {"defect_category": DefectCategory.CONTAMINANT.name, "inspection_module": "RULE", "coordinates": [23, 44, 27 ,77], "product_id": 1, "inspection_session_id": 1},
            {"defect_category": DefectCategory.CONTAMINANT.name, "inspection_module": "RULE", "coordinates": [50, 60, 60 ,80], "product_id": 1, "inspection_session_id": 1},
            {"defect_category": DefectCategory.CONTAMINANT.name, "inspection_module": "RULE", "coordinates": [100, 120, 120 ,140], "product_id": 1, "inspection_session_id": 1},
            {"defect_category": DefectCategory.CONTAMINANT.name, "inspection_module": "RULE", "coordinates": [77, 99, 99 ,121], "product_id": 1, "inspection_session_id": 1},
        ]
    )
    conn.commit()
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    print("Downgrade Start")
    queries = (
        sa.text(f'TRUNCATE TABLE "{User.__tablename__}" CASCADE;'),
        sa.text(f'TRUNCATE TABLE "{SettingsGlobal.__tablename__}" CASCADE;'),
        sa.text(f'TRUNCATE TABLE "{Device.__tablename__}" CASCADE;'),
        sa.text(f'TRUNCATE TABLE "{SettingsProductParameter.__tablename__}" CASCADE;'),
        sa.text(f'TRUNCATE TABLE "{MmapSession.__tablename__}" CASCADE;'),
        ####################################
        sa.text(f'TRUNCATE TABLE "{Product.__tablename__}" CASCADE;'),
        sa.text(f'TRUNCATE TABLE "{Defect.__tablename__}" CASCADE;'),
    )
    for q in queries:
        print(q)
        op.execute(q)

    print("Downgrade Done")
    # ### end Alembic commands ###
