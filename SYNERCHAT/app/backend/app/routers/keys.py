import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from web3 import Web3


router = APIRouter()

POLYGON_RPC = os.getenv("POLYGON_RPC") or os.getenv("AMOY_RPC") or ""
KEYREGISTRY_ADDRESS = os.getenv("KEYREGISTRY_ADDRESS", "")

ABI_KEYREGISTRY = [
    {
        "inputs": [
            {"internalType": "address", "name": "owner", "type": "address"},
            {"internalType": "bytes32", "name": "deviceId", "type": "bytes32"},
        ],
        "name": "getDeviceKey",
        "outputs": [
            {
                "components": [
                    {"internalType": "bytes32", "name": "deviceId", "type": "bytes32"},
                    {"internalType": "bytes", "name": "pubEncKey", "type": "bytes"},
                    {"internalType": "bytes", "name": "pubSigKey", "type": "bytes"},
                    {"internalType": "uint256", "name": "registeredAt", "type": "uint256"},
                    {"internalType": "bool", "name": "active", "type": "bool"}
                ],
                "internalType": "struct KeyRegistry.DeviceKey",
                "name": "",
                "type": "tuple"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]


class DeviceKeyResponse(BaseModel):
    deviceId: str
    pubEncKey: str
    pubSigKey: str
    registeredAt: int
    active: bool


@router.get("/{address}", response_model=DeviceKeyResponse)
async def get_device_key(address: str, deviceId: str):
    if not POLYGON_RPC or not KEYREGISTRY_ADDRESS:
        raise HTTPException(status_code=500, detail="RPC or contract address not configured")
    w3 = Web3(Web3.HTTPProvider(POLYGON_RPC))
    contract = w3.eth.contract(address=Web3.to_checksum_address(KEYREGISTRY_ADDRESS), abi=ABI_KEYREGISTRY)
    device_id_bytes32 = bytes.fromhex(deviceId[2:]) if deviceId.startswith("0x") else bytes.fromhex(deviceId)
    res = contract.functions.getDeviceKey(Web3.to_checksum_address(address), device_id_bytes32).call()
    return DeviceKeyResponse(
        deviceId="0x" + res[0].hex(),
        pubEncKey="0x" + res[1].hex(),
        pubSigKey="0x" + res[2].hex(),
        registeredAt=int(res[3]),
        active=bool(res[4])
    )