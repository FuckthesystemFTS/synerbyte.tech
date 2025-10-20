// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

interface IERC20 {
    function transfer(address to, uint256 amount) external returns (bool);
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
    function balanceOf(address account) external view returns (uint256);
    function allowance(address owner, address spender) external view returns (uint256);
}

/**
 * @title FTSPayments
 * @notice Lightweight helper contract to route tips and in-chat transfers using an existing FTS ERC-20 token.
 */
contract FTSPayments {
    IERC20 public immutable fts;

    event Tipped(address indexed from, address indexed to, uint256 amount);
    event TransferredOnChat(address indexed from, address indexed to, uint256 amount);

    constructor(address ftsToken) {
        require(ftsToken != address(0), "fts zero");
        fts = IERC20(ftsToken);
    }

    function tip(address to, uint256 amount) external {
        require(to != address(0), "to zero");
        require(amount > 0, "amount zero");
        bool ok = fts.transferFrom(msg.sender, to, amount);
        require(ok, "fts transferFrom failed");
        emit Tipped(msg.sender, to, amount);
    }

    function transferOnChat(address to, uint256 amount) external {
        require(to != address(0), "to zero");
        require(amount > 0, "amount zero");
        bool ok = fts.transferFrom(msg.sender, to, amount);
        require(ok, "fts transferFrom failed");
        emit TransferredOnChat(msg.sender, to, amount);
    }

    function balanceOfFTS(address account) external view returns (uint256) {
        return fts.balanceOf(account);
    }

    function allowanceFTS(address owner, address spender) external view returns (uint256) {
        return fts.allowance(owner, spender);
    }
}