import base64
import binascii

from fastapi import FastAPI
from fastapi.security.utils import get_authorization_scheme_param
from starlette.authentication import AuthenticationBackend, AuthenticationError
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import HTTPConnection


class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn: HTTPConnection):
        print("------------------------AUth BACKEND")
        print(conn.__dict__)

        auth: str = conn.headers.get("Authorization")
        if not auth:
            return False, None
        try:
            scheme, credentials = get_authorization_scheme_param(auth)
            print(f"{auth=}")
            print(f"{scheme=}")
            print(f"{credentials=}")
            if not (auth and scheme and credentials):
                print("not (auth and scheme and credentials)")
                raise AuthenticationError("Not authenticated")
            if scheme.lower() != "basic":
                raise AuthenticationError("Invalid authentication credentials")
            decoded = base64.b64decode(credentials).decode("ascii")
            print(f"{decoded=}")
        except (ValueError, UnicodeDecodeError, binascii.Error):
            raise AuthenticationError("Invalid basic auth credentials")

        return True, None


def register_basic_auth_backend(app: FastAPI) -> None:
    app.add_middleware(AuthenticationMiddleware, backend=BasicAuthBackend())
