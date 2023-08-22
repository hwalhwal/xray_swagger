from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from xray_settings.routers.contaminant.ai import router as ai_router
from xray_settings.routers.contaminant.rule import rule_router
from xray_settings.routers.contour import router as contour_router
from xray_settings.routers.conveyor import conveyor_router
from xray_settings.routers.emitter import emitter_router
from xray_settings.routers.image import image_router
from xray_settings.routers.inspections import inspection_router
from xray_settings.routers.preprocessor import preprocessor_router
from xray_settings.routers.rejector import rejector_router

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"api": "XrayXray"}


contaminant_router = APIRouter(prefix="/contaminant", tags=[])
contaminant_router.include_router(ai_router)
contaminant_router.include_router(rule_router)

inspection_router.include_router(contaminant_router)
app.include_router(inspection_router)
app.include_router(emitter_router)
app.include_router(conveyor_router)
app.include_router(rejector_router)
app.include_router(image_router)
app.include_router(preprocessor_router)
app.include_router(contour_router)
