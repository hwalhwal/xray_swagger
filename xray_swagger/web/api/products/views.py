from datetime import datetime
from typing import Annotated, Sequence

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
    DefectUpdateDTO,
    InspectionSessionCreateDTO,
    InspectionSessionDTO,
    ProductCreateDTO,
    ProductDTO,
)

router = APIRouter()


@router.post(path="/", status_code=status.HTTP_201_CREATED)
async def create_product(
    product_name: str,
    user: Annotated[User, Depends(get_current_active_user)],
    dao: ProductDAO = Depends(),
) -> ProductDTO:
    new_product_payload = ProductCreateDTO(
        name=product_name,
        creator_id=user.id,
        last_editor_id=user.id,
    )
    new_product = await dao.create(new_product_payload)
    return new_product


@router.get(path="/")
async def get_all_products(
    dao: ProductDAO = Depends(),
) -> Sequence[ProductDTO]:
    # TODO: not deleted only

    d = await dao.get_all()
    if not d:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Nothing.")
    logger.debug(d[0].__dict__)
    return d


@router.get(path="/{product_id}")
async def get_product_by_id(
    product_id: int,
    dao: ProductDAO = Depends(),
) -> ProductDTO:
    # TODO: not deleted only

    d = await dao.get(product_id)
    if not d:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Product <id: {product_id}> Not Found")
    return d


@router.patch(path="/{product_id}")
async def update_product(
    product_id: int,
    product_name: str,
    user: Annotated[User, Depends(get_current_active_user)],
    dao: ProductDAO = Depends(),
) -> ProductDTO:
    product = await dao.get(product_id)
    if not product:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Product <id: {product_id}> Not Found")
    update_product_payload = ProductDTO(
        name=product_name,
        last_editor_id=user.id,
        modified_at=datetime.utcnow(),
    )
    await dao.update(product, update_product_payload, exclude_unset=True)
    return product


@router.delete(path="/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    dao: ProductDAO = Depends(),
) -> None:
    # TODO: not deleted only
    d = await dao.get(product_id)
    if not d:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Defect <id: {product_id} Not Found")
    await dao.delete(d)


########################################################################
TAG_INSPECTION_SESSION = ["inspection-sessions"]


@router.post(
    path="/{product_id}/inspection-sessions",
    status_code=status.HTTP_201_CREATED,
    tags=TAG_INSPECTION_SESSION,
)
async def create_inspection_session(
    product_id: int,
    payload: InspectionSessionCreateDTO,
    dao: InspectionSessionDAO = Depends(),
) -> InspectionSessionDTO:
    # if isp_sess_dupl := await isp_sess_dao.get_sess(product_id, payload.image_s3_key):
    #     logger.warning(f"User name: {isp_sess_dupl.username} Fullname: {isp_sess_dupl.fullname}")
    #     raise HTTPException(
    #         status_code=status.HTTP_409_CONFLICT,
    #         detail="A user with that username already exists.",
    #     )
    payload.product_id = product_id
    new_isp_sess = await dao.create(payload)
    logger.info(new_isp_sess.__dict__)
    return new_isp_sess


@router.get(
    path="/{product_id}/inspection-sessions",
    tags=TAG_INSPECTION_SESSION,
)
async def get_inspection_sessions(
    product_id: int,
    page: int = 0,
    size: int = 20,
    dao: InspectionSessionDAO = Depends(),
) -> Sequence[InspectionSessionDTO]:
    # TODO: pagination
    d = await dao.get_all(product_id, offset=page, limit=size)
    return d


# TODO: 인조키가 아닌 식별 가능한 복합키를 고안할 것.
@router.get(
    path="/{product_id}/inspection-sessions/{isp_sess_id}",
    tags=TAG_INSPECTION_SESSION,
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
    # DTO에서 기본적으로 relationship field를 집어넣으려면
    #          selectinload or joinedload를 사용해서 미리 넣어둔다.
    # 그렇지 않고 때때로 쓰거나 쓰지 않으면 AsyncAttrs Mixin에 의해 lazyload하도록 둔다.
    # https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#preventing-implicit-io-when-using-asyncsession
    # prd = await d.awaitable_attrs.product
    # logger.debug(prd)
    return d


########################################################################
TAG_PRODUCT_DEFECT = ["product-defects"]


@router.post(
    path="/{product_id}/defects",
    status_code=status.HTTP_201_CREATED,
    tags=TAG_PRODUCT_DEFECT,
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


@router.get(path="/{product_id}/defects", tags=TAG_PRODUCT_DEFECT)
async def filter_defects(
    product_id: int,
    isp_sess_id: int | None = None,
    defect_category: int | None = None,
    dao: DefectDAO = Depends(),
) -> Sequence[DefectDTO]:
    defect_category = DefectCategory(defect_category) if defect_category else None
    logger.debug(defect_category)
    d = await dao.filter(product_id, isp_sess_id, defect_category)
    return d


@router.get(path="/{product_id}/defects/{defect_id}", tags=TAG_PRODUCT_DEFECT)
async def get_defect(
    defect_id: int,
    dao: DefectDAO = Depends(),
) -> DefectDTO:
    d = await dao.get(defect_id)
    if not d:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Defect <id: {defect_id} Not Found")
    return d


@router.patch(
    path="/{product_id}/defects/{defect_id}",
    tags=TAG_PRODUCT_DEFECT,
)
async def update_defect(
    defect_id: int,
    payload: DefectUpdateDTO,
    dao: DefectDAO = Depends(),
) -> DefectDTO:
    logger.debug(payload)
    d = await dao.get(defect_id)
    if not d:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Defect <id: {defect_id} Not Found")
    await dao.update(d, payload, exclude_none=True)
    return d


@router.delete(
    path="/{product_id}/defects/{defect_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=TAG_PRODUCT_DEFECT,
)
async def delete_defect(
    defect_id: int,
    dao: DefectDAO = Depends(),
) -> None:
    d = await dao.get(defect_id)
    if not d:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Defect <id: {defect_id} Not Found")
    await dao.delete(d)
