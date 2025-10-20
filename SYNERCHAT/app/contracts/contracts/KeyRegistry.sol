// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title KeyRegistry
 * @notice Maps an EOA to device public encryption/signing keys. Device keys are meant to be rotated or revoked.
 */
contract KeyRegistry {
    struct DeviceKey {
        bytes32 deviceId; // client-generated identifier
        bytes pubEncKey;  // e.g., X25519 pubkey
        bytes pubSigKey;  // optional
        uint256 registeredAt;
        bool active;
    }

    // address => deviceId => key
    mapping(address => mapping(bytes32 => DeviceKey)) private keys;

    event DeviceKeyRegistered(address indexed owner, bytes32 indexed deviceId, bytes pubEncKey, bytes pubSigKey);
    event DeviceKeyRotated(address indexed owner, bytes32 indexed deviceId, bytes newPubEncKey, bytes newPubSigKey);
    event DeviceKeyRevoked(address indexed owner, bytes32 indexed deviceId);

    function registerDeviceKey(bytes32 deviceId, bytes calldata pubEncKey, bytes calldata pubSigKey) external {
        require(deviceId != bytes32(0), "invalid deviceId");
        require(pubEncKey.length > 0, "missing enc key");
        DeviceKey storage existing = keys[msg.sender][deviceId];
        require(!existing.active, "already exists");
        keys[msg.sender][deviceId] = DeviceKey({
            deviceId: deviceId,
            pubEncKey: pubEncKey,
            pubSigKey: pubSigKey,
            registeredAt: block.timestamp,
            active: true
        });
        emit DeviceKeyRegistered(msg.sender, deviceId, pubEncKey, pubSigKey);
    }

    function rotateDeviceKey(bytes32 deviceId, bytes calldata newPubEncKey, bytes calldata newPubSigKey) external {
        DeviceKey storage existing = keys[msg.sender][deviceId];
        require(existing.active, "not found");
        require(newPubEncKey.length > 0, "missing enc key");
        existing.pubEncKey = newPubEncKey;
        existing.pubSigKey = newPubSigKey;
        emit DeviceKeyRotated(msg.sender, deviceId, newPubEncKey, newPubSigKey);
    }

    function revokeDeviceKey(bytes32 deviceId) external {
        DeviceKey storage existing = keys[msg.sender][deviceId];
        require(existing.active, "not found");
        existing.active = false;
        emit DeviceKeyRevoked(msg.sender, deviceId);
    }

    function getDeviceKey(address owner, bytes32 deviceId) external view returns (DeviceKey memory) {
        return keys[owner][deviceId];
    }
}