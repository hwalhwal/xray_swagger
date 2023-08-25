from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends
from loguru import logger

from xray_swagger.db.dao.products_dao import InspectionSessionDAO, ProductDAO

from .schema import InspectionSessionCreateDTO, InspectionSessionDTO, ProductDTO

router = APIRouter()

sample_product = ProductDTO(
    name="asdas",
    inspection_sessions="aasd",
    settings="aaa",
    creator_id=1,
    last_editor_id=1,
)


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
    return d
