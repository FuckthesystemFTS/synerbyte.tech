import os
import time
import secrets
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from eth_account import Account
from eth_account.messages import encode_defunct

from ..utils.jwt import issue_jwt


router = APIRouter()

NONCES: dict[str, str] = {}


class SiweStartResponse(BaseModel):
    nonce: str
    message: str
    issuedAt: int
    expiresAt: int


class SiweVerifyRequest(BaseModel):
    address: str
    deviceId: str
    nonce: str
    signature: str
    issuedAt: int
    expiresAt: int
    chainId: int


class SiweVerifyResponse(BaseModel):
    token: str
    expiresAt: int


@router.get("/siwe-start", response_model=SiweStartResponse)
async def siwe_start(address: str, deviceId: str, chainId: int = 137):
    issued_at = int(time.time())
    ttl = int(os.getenv("JWT_TTL_SECONDS", "600"))
    expires_at = issued_at + ttl
    nonce = secrets.token_hex(16)
    NONCES[f"{address.lower()}:{deviceId}"] = nonce
    message = (
        f"Synerchat Login\naddress:{address.lower()}\n"
        f"deviceId:{deviceId}\nnonce:{nonce}\nissuedAt:{issued_at}\n"
        f"expiresAt:{expires_at}\nchainId:{chainId}"
    )
    return SiweStartResponse(nonce=nonce, message=message, issuedAt=issued_at, expiresAt=expires_at)


@router.post("/siwe-verify", response_model=SiweVerifyResponse)
async def siwe_verify(req: SiweVerifyRequest):
    key = f"{req.address.lower()}:{req.deviceId}"
    expected_nonce = NONCES.get(key)
    if not expected_nonce or expected_nonce != req.nonce:
        raise HTTPException(status_code=400, detail="Invalid nonce")

    message = (
        f"Synerchat Login\naddress:{req.address.lower()}\n"
        f"deviceId:{req.deviceId}\nnonce:{req.nonce}\nissuedAt:{req.issuedAt}\n"
        f"expiresAt:{req.expiresAt}\nchainId:{req.chainId}"
    )

    recovered = Account.recover_message(encode_defunct(text=message), signature=req.signature)
    if recovered.lower() != req.address.lower():
        raise HTTPException(status_code=400, detail="Signature mismatch")

    now = int(time.time())
    if req.expiresAt <= now:
        raise HTTPException(status_code=400, detail="Expired payload")

    del NONCES[key]

    token = issue_jwt(subject=req.address.lower(), device_id=req.deviceId, expires_at=req.expiresAt)
    return SiweVerifyResponse(token=token, expiresAt=req.expiresAt)