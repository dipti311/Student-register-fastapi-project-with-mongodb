import jwt
from jwt.exceptions import (
    ExpiredSignatureError,
    InvalidSignatureError,
    MissingRequiredClaimError,
)

from scripts.config import KeyPath
from scripts.constants.secrets import Secrets
from scripts.errors import AuthenticationError, ErrorMessages
from scripts.logging import logger


class JWT:
    def __init__(self):
        self.max_login_age = Secrets.LOCK_OUT_TIME_MINS
        self.issuer = Secrets.issuer
        self.alg = Secrets.alg
        self.public = KeyPath.public
        self.private = KeyPath.private

    def encode(self, payload):
        try:
            with open(self.private, "r") as f:
                key = f.read()
            return jwt.encode(payload, key, algorithm=self.alg)
        except Exception as e:
            logger.exception(f"Exception while encoding JWT: {str(e)}")
            raise
        finally:
            f.close()

    def validate(self, token):
        try:
            with open(self.public, "r") as f:
                key = f.read()
            payload = jwt.decode(
                token,
                key,
                algorithms=self.alg,
                leeway=Secrets.leeway_in_mins,
                options={"require": ["exp", "iss"]},
            )
            return payload
        except InvalidSignatureError:
            raise AuthenticationError(ErrorMessages.ERROR003)
        except ExpiredSignatureError:
            raise AuthenticationError(ErrorMessages.ERROR002)
        except MissingRequiredClaimError:
            raise AuthenticationError(ErrorMessages.ERROR002)
        except Exception as e:
            logger.exception(f"Exception while validating JWT: {str(e)}")
            raise
        finally:
            f.close()

    def decode(self, token):
        try:
            with open(self.public, "r") as f:
                key = f.read()
            return jwt.decode(token, key, algorithms=self.alg)
        except Exception as e:
            logger.exception(f"Exception while encoding JWT: {str(e)}")
            raise
        finally:
            f.close()
