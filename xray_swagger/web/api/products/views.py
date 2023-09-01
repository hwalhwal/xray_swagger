from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends
from loguru import logger

from xray_swagger.db.dao.products_dao import DefectDAO, InspectionSessionDAO, ProductDAO
from xray_swagger.db.models.defect import DefectCategory
from xray_swagger.db.models.user import User
from xray_swagger.web.dependencies.users import get_current_active_user

from .schema import (
    DefectCreateDTO,
    DefectDTO,
    InspectionSessionCreateDTO,
    InspectionSessionDTO,
    ProductDTO,
)

router = APIRouter()


@router.post(path="/", status_code=status.HTTP_201_CREATED, response_model=ProductDTO)
async def create_product(
    product_name: str,
    user: Annotated[User, Depends(get_current_active_user)],
    dao: ProductDAO = Depends(),
):
    new_product_payload = ProductDTO(
        name=product_name,
        creator_id=user.id,
        last_editor_id=user.id,
    )
    new_product = await dao.create(new_product_payload)
    return new_product


@router.get(path="/", response_model=list[ProductDTO])
async def get_all_products(
    dao: ProductDAO = Depends(),
):
    d = await dao.get_all()
    if not d:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Nothing.")
    logger.debug(d[0].__dict__)
    return d


@router.get(path="/{product_id}", response_model=ProductDTO)
async def get_product_by_id(
    product_id: int,
    dao: ProductDAO = Depends(),
):
    d = await dao.get(product_id)
    if not d:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Product <id: {product_id} Not Found")
    return d


@router.patch(path="/{product_id}", response_model=ProductDTO)
async def update_product(
    product_id: int,
    product_name: str,
    user: Annotated[User, Depends(get_current_active_user)],
    dao: ProductDAO = Depends(),
):
    product = await dao.get(product_id)
    if not product:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Product <id: {product_id} Not Found")
    update_product_payload = ProductDTO(
        name=product_name,
        last_editor_id=user.id,
        modified_at=datetime.utcnow(),
    )
    await dao.update(product, update_product_payload)
    return product


@router.post(
    path="/{product_id}/inspection-sessions",
    status_code=status.HTTP_201_CREATED,
    tags=["inspection-sessions"],
)
async def create_inspection_session(
    product_id: int,
    payload: InspectionSessionCreateDTO,
    isp_sess_dao: InspectionSessionDAO = Depends(),
) -> InspectionSessionDTO:
    # if isp_sess_dupl := await isp_sess_dao.get_sess(product_id, payload.image_s3_key):
    #     logger.warning(f"User name: {isp_sess_dupl.username} Fullname: {isp_sess_dupl.fullname}")
    #     raise HTTPException(
    #         status_code=status.HTTP_409_CONFLICT,
    #         detail="A user with that username already exists.",
    #     )
    payload.product_id = product_id
    new_isp_sess = await isp_sess_dao.create(payload)
    logger.info(new_isp_sess.__dict__)
    return new_isp_sess


@router.get(
    path="/{product_id}/inspection-sessions",
    tags=["inspection-sessions"],
)
async def get_inspection_sessions(
    product_id: int,
    page: int = 0,
    size: int = 20,
    dao: InspectionSessionDAO = Depends(),
) -> list[InspectionSessionDTO]:
    d = await dao.get_all(product_id, offset=page, limit=size)
    return d


# TODO: 인조키가 아닌 식별 가능한 복합키를 고안할 것.
@router.get(
    path="/{product_id}/inspection-sessions/{isp_sess_id}",
    tags=["inspection-sessions"],
)
async def get_inspection_session_by_id(
    product_id: int,
    isp_sess_id: int,
    dao: InspectionSessionDAO = Depends(),
) -> InspectionSessionDTO:
    d = await dao.get_by_id(product_id, isp_sess_id)
    if not d:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Product <id: {product_id} Not Found")
    logger.debug(d.image_s3_key)
    # DTO에서 기본적으로 relationship field를 집어넣으려면 selectinload or joinedload를 사용해서 미리 넣어둔다.
    # 그렇지 않고 때때로 쓰거나 쓰지 않으면 AsyncAttrs Mixin에 의해 lazyload하도록 둔다.
    # https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#preventing-implicit-io-when-using-asyncsession
    # prd = await d.awaitable_attrs.product
    # logger.debug(prd)
    return d


@router.post(
    path="/{product_id}/defects",
    status_code=status.HTTP_201_CREATED,
    tags=["product-defects"],
)
async def create_defect(
    product_id: int,
    payload: DefectCreateDTO,
    isp_sess_dao: DefectDAO = Depends(),
) -> DefectDTO:
    # TODO: integrity check
    payload.product_id = product_id
    new_defect = await isp_sess_dao.create(payload)
    logger.info(new_defect.__dict__)
    return new_defect


@router.get(
    path="/{product_id}/defects",
    tags=["product-defects"],
)
async def get_defects(
    product_id: int,
    isp_sess_id: int | None = None,
    defect_category: int | None = None,
    dao: DefectDAO = Depends(),
) -> list[DefectDTO]:
    defect_category = DefectCategory(defect_category)
    print(defect_category)
    d = await dao.filter(product_id, isp_sess_id, defect_category)
    return d
