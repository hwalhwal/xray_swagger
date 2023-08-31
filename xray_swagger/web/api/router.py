from fastapi.routing import APIRouter

from xray_swagger.web.api import mmap_session, monitoring, products, settings, users

api_router = APIRouter()
api_router.include_router(monitoring.router)

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(settings.router, prefix="/settings", tags=["settings"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(mmap_session.router, prefix="/mmap", tags=["mmap"])
