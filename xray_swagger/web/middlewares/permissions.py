from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Annotated

from fastapi import HTTPException, Request, status
from fastapi.param_functions import Depends
from loguru import logger

from xray_swagger.db.models.user import AuthLevel
from xray_swagger.web.api.deps import get_current_active_user

if TYPE_CHECKING:
    from xray_swagger.web.api.users.schema import UserModelDTO


class BasePermission(ABC):
    """
    Abstract permission that all other Permissions must be inherited from.

    Defines basic error message, status & error codes.

    Upon initialization, calls abstract method  `has_required_permissions`
    which will be specific to concrete implementation of Permission class.

    You would write your permissions like this:

    .. code-block:: python

        class TeapotUserAgentPermission(BasePermission):

            def has_required_permissions(self, request: Request) -> bool:
                return request.headers.get('User-Agent') == "Teapot v1.0"

    """

    error_msg = "Forbidden."
    status_code = status.HTTP_403_FORBIDDEN
    error_code = status.HTTP_403_FORBIDDEN

    @abstractmethod
    def has_required_permissions(self, request: Request, user: "UserModelDTO") -> bool:
        ...

    def __init__(self, request: Request, user: "UserModelDTO"):
        if not self.has_required_permissions(request, user):
            raise HTTPException(
                status_code=self.status_code,
                detail=self.error_msg,
            )


class IsAuthenticated(BasePermission):
    """
    Permission that checks if the user has been authenticated (by middleware)
        @app.get(
            "/user/",
            dependencies=[Depends(PermissionsDependency([IsAuthenticated]))]
        )
        async def user(request: Request) -> dict:
            return request.scope["user"].dict()

    """

    error_msg = "Not authenticated."
    status_code = status.HTTP_401_UNAUTHORIZED

    def has_required_permissions(self, request: Request, user: "UserModelDTO") -> bool:
        logger.debug("=== Is Authenticated?")
        logger.debug(user)
        logger.debug(user.authlevel)
        logger.debug(type(request))
        logger.debug(request.state.__dict__)
        return user is not None


class IsSupervisor(BasePermission):
    error_msg = "Your permission is not enough to execute this operation"
    status_code = status.HTTP_403_FORBIDDEN

    def has_required_permissions(self, request: Request, user: "UserModelDTO") -> bool:
        logger.debug("=== Is Supervisor?")
        logger.debug(user)
        logger.debug(f"{user.authlevel} = {user.authlevel.value}")
        logger.debug(f"{AuthLevel.SUPERVISOR} = {AuthLevel.SUPERVISOR.value}")
        logger.debug(f"{user.authlevel.value >= AuthLevel.SUPERVISOR.value=}")
        return user.authlevel.value >= AuthLevel.SUPERVISOR.value


class IsEngineer(BasePermission):
    error_msg = "Your permission is not enough to execute this operation"
    status_code = status.HTTP_403_FORBIDDEN

    def has_required_permissions(self, request: Request, user: "UserModelDTO") -> bool:
        logger.debug("=== Is Engineer?")
        logger.debug(f"{user.authlevel} = {user.authlevel.value}")
        return user.authlevel.value >= AuthLevel.ENGINEER.value


class PermissionsDependency:
    """
    Permission dependency that is used to define and check all the permission
    classes from one place inside route definition.
    """

    def __init__(self, permissions_classes: list):
        logger.debug("=== Permission List", permissions_classes)
        self.permissions_classes = permissions_classes

    def __call__(
        self,
        request: Request,
        user: Annotated["UserModelDTO", Depends(get_current_active_user)],
    ):
        logger.debug("Permission deps resolving".center(100, "#"))
        for permission_class in self.permissions_classes:
            permission_class(request=request, user=user)
        return True
