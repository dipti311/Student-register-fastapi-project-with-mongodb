import json
import logging

import jwt
from fastapi import Request
from jwt.exceptions import (
    DecodeError,
    ExpiredSignatureError,
    InvalidSignatureError,
    MissingRequiredClaimError,
)
from starlette.middleware.base import BaseHTTPMiddleware

from scripts.config import Service
from scripts.constants.secrets import Secrets

ENFORCE_DOMAIN_WILDCARD = "Domain wildcard patterns must be like '*.example.com'."

protect_hosts = Service.protected_hosts
if not protect_hosts:
    protect_hosts = ["*"]

for _pattern in protect_hosts:
    assert "*" not in _pattern[1:], ENFORCE_DOMAIN_WILDCARD
    if _pattern.startswith("*") and _pattern != "*":
        assert _pattern.startswith("*."), ENFORCE_DOMAIN_WILDCARD


class SignatureVerificationMiddleware(BaseHTTPMiddleware):
    async def set_body(self, request: Request):
        async def verify_signature():
            receive_ = await request.receive()
            signature = bytearray()
            signature.extend(receive_.get("body"))
            while receive_["more_body"]:
                receive_ = await request.receive()
                signature.extend(receive_["body"])

            signature = bytes(signature)
            try:
                signature = jwt.decode(
                    signature.decode(), Secrets.signature_key, algorithms=["HS256"]
                )
            except (
                InvalidSignatureError,
                ExpiredSignatureError,
                MissingRequiredClaimError,
                DecodeError,
            ) as inv_exp:
                logging.error(inv_exp)
                signature = {}
            signature = json.dumps(signature).encode()
            return {"type": receive_["type"], "body": signature, "more_body": False}

        if request.headers.get("Content-Type") == "application/json":
            host = request.headers.get("host", "").split(":")[0]
            is_protected_host = False
            for pattern in protect_hosts:
                if host == pattern or (
                    pattern.startswith("*") and host.endswith(pattern[1:])
                ):
                    is_protected_host = True
                    break
            if is_protected_host:
                return Request(request.scope, verify_signature, request._send)
        return request

    async def dispatch(self, request, call_next):
        request = await self.set_body(request)
        response = await call_next(request)
        return response
