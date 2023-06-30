from fastapi import APIRouter

router = APIRouter()


@router.post("/signup")
async def singup():
    return


@router.post("/signin")
async def signin():
    return


@router.post("/signout")
async def signout():
    return


@router.get("/me")
async def me():
    return


@router.post("/update_profile")
async def update_profile() -> int:
    return 0


# @router.get("/", response_model=List[DummyModelDTO])
# async def get_dummy_models(
#     limit: int = 10,
#     offset: int = 0,
#     dummy_dao: DummyDAO = Depends(),
# ) -> List[DummyModel]:
#     """
#     Retrieve all dummy objects from the database.

#     :param limit: limit of dummy objects, defaults to 10.
#     :param offset: offset of dummy objects, defaults to 0.
#     :param dummy_dao: DAO for dummy models.
#     :return: list of dummy objects from database.
#     """
#     return await dummy_dao.get_all_dummies(limit=limit, offset=offset)


# @router.put("/")
# async def create_dummy_model(
#     new_dummy_object: DummyModelInputDTO,
#     dummy_dao: DummyDAO = Depends(),
# ) -> None:
#     """
#     Creates dummy model in the database.

#     :param new_dummy_object: new dummy model item.
#     :param dummy_dao: DAO for dummy models.
#     """
#     await dummy_dao.create_dummy_model(**new_dummy_object.dict())
