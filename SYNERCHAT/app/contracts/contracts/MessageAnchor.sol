// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title MessageAnchor
 * @notice Stores batches of message hashes for proof-of-existence/ordering without content.
 */
contract MessageAnchor {
    event BatchAnchored(uint256 indexed batchId, bytes32 merkleRoot, uint256 count, uint256 timestamp);

    uint256 public batchCount;

    struct Batch {
        bytes32 merkleRoot;
        uint256 count;
        uint256 timestamp;
    }

    mapping(uint256 => Batch) public batches;

    function anchorBatch(bytes32 merkleRoot, uint256 count) external returns (uint256 batchId) {
        require(merkleRoot != bytes32(0), "root zero");
        require(count > 0, "count zero");
        batchId = ++batchCount;
        batches[batchId] = Batch({ merkleRoot: merkleRoot, count: count, timestamp: block.timestamp });
        emit BatchAnchored(batchId, merkleRoot, count, block.timestamp);
    }

    function getBatch(uint256 batchId) external view returns (Batch memory) {
        return batches[batchId];
    }
}