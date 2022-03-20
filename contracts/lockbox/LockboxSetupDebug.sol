pragma solidity 0.4.24;

import "./LockboxDebug.sol";

contract LockboxSetupDebug {
    EntrypointDebug public entrypoint;

    constructor() public {
        entrypoint = new EntrypointDebug();
    }

    function isSolved() public view returns (bool) {
        return entrypoint.solved();
    }
}
