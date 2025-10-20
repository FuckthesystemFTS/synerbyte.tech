import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from web3 import Web3

router = APIRouter()

POLYGON_RPC = os.getenv("POLYGON_RPC") or os.getenv("AMOY_RPC") or ""
FTS_ADDRESS = os.getenv("FTS_ADDRESS", "0xCc12Ea927F6E8d3919010498Ef8736d4612FD83e")

ABI_ERC20 = [
    {"constant": True, "inputs": [{"name": "account", "type": "address"}], "name": "balanceOf", "outputs": [{"name": "", "type": "uint256"}], "type": "function"},
    {"constant": True, "inputs": [{"name": "owner", "type": "address"}, {"name": "spender", "type": "address"}], "name": "allowance", "outputs": [{"name": "", "type": "uint256"}], "type": "function"},
    {"constant": True, "inputs": [], "name": "decimals", "outputs": [{"name": "", "type": "uint8"}], "type": "function"}
]


class BalanceResponse(BaseModel):
    token: str
    address: str
    balance: str
    decimals: int


class AllowanceResponse(BaseModel):
    token: str
    owner: str
    spender: str
    allowance: str


@router.get("/balance/{address}", response_model=BalanceResponse)
async def balance(address: str):
    if not POLYGON_RPC:
        raise HTTPException(status_code=500, detail="RPC not configured")
    w3 = Web3(Web3.HTTPProvider(POLYGON_RPC))
    erc20 = w3.eth.contract(address=Web3.to_checksum_address(FTS_ADDRESS), abi=ABI_ERC20)
    bal = erc20.functions.balanceOf(Web3.to_checksum_address(address)).call()
    decimals = erc20.functions.decimals().call()
    return BalanceResponse(token=FTS_ADDRESS, address=address, balance=str(bal), decimals=decimals)


@router.get("/allowance/{owner}/{spender}", response_model=AllowanceResponse)
async def allowance(owner: str, spender: str):
    if not POLYGON_RPC:
        raise HTTPException(status_code=500, detail="RPC not configured")
    w3 = Web3(Web3.HTTPProvider(POLYGON_RPC))
    erc20 = w3.eth.contract(address=Web3.to_checksum_address(FTS_ADDRESS), abi=ABI_ERC20)
    value = erc20.functions.allowance(Web3.to_checksum_address(owner), Web3.to_checksum_address(spender)).call()
    return AllowanceResponse(token=FTS_ADDRESS, owner=owner, spender=spender, allowance=str(value))