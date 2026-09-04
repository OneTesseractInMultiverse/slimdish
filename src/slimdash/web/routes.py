"""FastAPI routes for application use cases."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse

from slimdash.dashboard.application.list_widgets import ListWidgets
from slimdash.dashboard.ports.widget_repository import WidgetRepository
from slimdash.identity.ports.identity_provider import IdentityProvider
from slimdash.web.schemas import UserResponse, WidgetResponse


def create_api_router(
    list_widgets: ListWidgets,
    repository: WidgetRepository,
) -> APIRouter:
    """Create API routes with explicit use-case dependencies."""
    router = APIRouter(prefix="/api")

    def provide_list_widgets() -> ListWidgets:
        return list_widgets

    @router.get("/health/live", include_in_schema=False)
    def liveness() -> dict[str, str]:
        return {"status": "ok"}

    @router.get("/health/ready", include_in_schema=False)
    def readiness() -> dict[str, str]:
        if not repository.is_ready():
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
        return {"status": "ready"}

    @router.get("/widgets", response_model=list[WidgetResponse])
    def widgets(use_case: Annotated[ListWidgets, Depends(provide_list_widgets)]) -> object:
        return use_case.execute()

    return router


def create_auth_router(
    provider: IdentityProvider | None,
    public_url: str,
) -> APIRouter:
    """Create authentication routes without exposing tokens to the browser."""
    router = APIRouter(prefix="/auth")

    @router.get("/me")
    def current_user(request: Request) -> UserResponse:
        user = request.session.get("user")
        if not isinstance(user, dict):
            return UserResponse(authenticated=False)
        return UserResponse(
            authenticated=True,
            display_name=user.get("display_name"),
            email=user.get("email"),
        )

    @router.get("/login")
    async def login(request: Request) -> object:
        if provider is None:
            raise HTTPException(status_code=501, detail="W3ID authentication is not configured")
        return await provider.begin_login(request, f"{public_url.rstrip('/')}/auth/callback")

    @router.get("/callback")
    async def callback(request: Request) -> RedirectResponse:
        if provider is None:
            raise HTTPException(status_code=501, detail="W3ID authentication is not configured")
        try:
            user = await provider.complete_login(request)
        except (RuntimeError, TypeError, ValueError) as error:
            raise HTTPException(status_code=401, detail="Authentication failed") from error
        request.session.clear()
        request.session["user"] = {
            "subject": user.subject,
            "display_name": user.display_name,
            "email": user.email,
        }
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

    @router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
    def logout(request: Request) -> None:
        request.session.clear()

    return router
