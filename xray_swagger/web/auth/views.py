from fastapi import APIRouter

router = APIRouter()


# @router.post("/signup")
# async def singup():
#     return


# @router.post("/signin")
# async def signin():
#     return


# @router.post("/signout")
# async def signout():
#     return


# @router.get("/me")
# async def me():
#     return


# @router.post("/update_profile")
# async def update_profile() -> int:
#     return 0

# @router.post("/token")
# async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
#     user_dict = fake_users_db.get(form_data.username)
#     if not user_dict:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     user = UserInDB(**user_dict)
#     hashed_password = fake_hash_password(form_data.password)
#     if not hashed_password == user.hashed_password:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")

#     return {"access_token": user.username, "token_type": "bearer"}
