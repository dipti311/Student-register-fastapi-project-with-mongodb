from secrets import compare_digest

from fastapi import HTTPException, Request, Response
from fastapi.openapi.models import APIKey, APIKeyIn
from fastapi.security import APIKeyCookie
from fastapi.security.api_key import APIKeyBase

from scripts.config import Service
from scripts.constants.secrets import Secrets
from scripts.db.redis_connections import login_db
from scripts.utils.security_utils.apply_encryption_util import create_token
from scripts.utils.security_utils.jwt_util import JWT


class CookieAuthentication(APIKeyBase):
    """
    Authentication backend using a cookie.
    Internally, uses a JWT token to store the data.
    """

    scheme: APIKeyCookie
    cookie_name: str
    cookie_secure: bool

    def __init__(
        self,
        cookie_name: str = "login-token",
    ):
        super().__init__()
        self.model: APIKey = APIKey(**{"in": APIKeyIn.cookie}, name=cookie_name)
        self.scheme_name = self.__class__.__name__
        self.cookie_name = cookie_name
        self.scheme = APIKeyCookie(name=self.cookie_name, auto_error=False)
        self.login_redis = login_db
        self.jwt = JWT()

    async def __call__(self, request: Request, response: Response) -> str:
        cookies = request.cookies
        login_token = cookies.get("login-token")
        if not login_token:
            login_token = request.headers.get("login-token")

        if not login_token:
            raise HTTPException(status_code=401)

        jwt_token = self.login_redis.get(login_token)
        if not jwt_token:
            raise HTTPException(status_code=401)

        try:
            decoded_token = self.jwt.validate(token=jwt_token)
            if not decoded_token:
                raise HTTPException(status_code=401)
        except Exception as e:
            raise HTTPException(status_code=401, detail=e.args)

        user_id = decoded_token.get("user_id")
        cookie_user_id = request.cookies.get(
            "user_id",
            request.cookies.get(
                "userId", request.headers.get("userId", request.headers.get("user_id"))
            ),
        )
        project_id = decoded_token.get("project_id")
        cookie_project_id = request.cookies.get(
            "projectId", request.headers.get("projectId")
        )

        _token = decoded_token.get("token")
        _age = int(decoded_token.get("age", Secrets.LOCK_OUT_TIME_MINS))

        if any(
            [
                not compare_digest(Secrets.token, _token),
                login_token != decoded_token.get("uid"),
                cookie_user_id and not compare_digest(user_id, cookie_user_id),
                project_id
                and cookie_project_id
                and not compare_digest(project_id, cookie_project_id),
            ]
        ):
            raise HTTPException(status_code=401)
        try:
            new_token = create_token(
                user_id=user_id,
                ip=request.client.host,
                token=Secrets.token,
                age=_age,
                login_token=login_token,
                project_id=project_id,
            )
        except Exception as e:
            raise HTTPException(status_code=401, detail=e.args)
        response.set_cookie(
            "login-token",
            new_token,
            samesite="strict",
            httponly=True,
            max_age=Secrets.LOCK_OUT_TIME_MINS * 60,
            secure=Service.secure_cookie,
        )

        response.headers["login-token"] = new_token

        return user_id
