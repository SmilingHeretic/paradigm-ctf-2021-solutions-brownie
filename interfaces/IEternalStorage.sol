pragma solidity 0.7.0;

interface IEternalStorage {
    // mint a new token with the given token id, display name, and owner
    // restricted to: token
    function mint(
        bytes32 tokenId,
        bytes32 name,
        address owner
    ) external;

    // update the name of the given token
    // restricted to: token or token owner
    function updateName(bytes32 tokenId, bytes32 name) external;

    // update the owner of the given token
    // restricted to: token or token owner
    function updateOwner(bytes32 tokenId, address newOwner) external;

    // update the approved user of the given token
    // restricted to: token or token owner
    function updateApproval(bytes32 tokenId, address approved) external;

    // update the address which holds the metadata of the given token
    // restricted to: token or token owner
    function updateMetadata(bytes32 tokenId, address metadata) external;

    // get the name of the token
    function getName(bytes32 tokenId) external view returns (bytes32);

    // get the owner of the token
    function getOwner(bytes32 tokenId) external view returns (address);

    // get the approved user of the token
    function getApproval(bytes32 tokenId) external view returns (address);

    // get the metadata contract associated with the token
    function getMetadata(bytes32 tokenId) external view returns (address);

    // transfers ownership of this storage contract to a new owner
    // restricted to: token
    function transferOwnership(address newOwner) external;

    // accepts ownership of this storage contract
    function acceptOwnership() external;
}
