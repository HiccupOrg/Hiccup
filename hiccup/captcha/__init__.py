from typing import Any, Union, Awaitable, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.websockets import WebSocket
from strawberry import BasePermission, Info

from hiccup import SETTINGS
from hiccup.captcha.turnstile import Turnstile
from hiccup.db import AuthToken


class IsPassedCaptcha(BasePermission):
    message = "User must finish captcha challenge"

    async def has_permission(
        self, source: Any, info: Info, **kwargs: Any
    ) -> bool:
        if not SETTINGS.captcha_enabled:
            return True

        request: Union[Request, WebSocket] = info.context["request"]
        if "X-Hiccup-Captcha" in request.headers:
            return await Turnstile(secret_key=SETTINGS.captcha_turnstile_secret).verify(request.headers.get("X-Hiccup-Captcha"))

        return False


class HasPermission(BasePermission):
    message = "Access denied"

    async def has_permission(
            self, source: Any, info: Info, **kwargs: Any
    ) -> bool:
        request: Union[Request, WebSocket] = info.context["request"]
        if "X-Hiccup-Token" in request.headers:
            access_token = request.headers.get("X-Hiccup-Token")
            async with AsyncSession() as session:
                db_token: Optional[AuthToken] = (await session.scalars(select(AuthToken).where(AuthToken.token == access_token).limit(1))).one_or_none()
                if db_token is not None:
                    db_token.classic_user_id

        return False


__all__ = ['Turnstile', 'IsPassedCaptcha']
