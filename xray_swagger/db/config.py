from typing import List

from xray_swagger.settings import settings

MODELS_MODULES: List[str] = ["xray_swagger.db.models.dummy_model"]  # noqa: WPS407

TORTOISE_CONFIG = {  # noqa: WPS407
    "connections": {
        "default": str(settings.db_url),
    },
    "apps": {
        "models": {
            "models": MODELS_MODULES + ["aerich.models"],
            "default_connection": "default",
        },
    },
}
