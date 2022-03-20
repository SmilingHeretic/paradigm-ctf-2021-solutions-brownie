pragma solidity 0.4.24;

import "./Lockbox.sol";

contract LockboxSetup {
    Entrypoint public entrypoint;

    constructor() public {
        entrypoint = new Entrypoint();
    }

    function isSolved() public view returns (bool) {
        return entrypoint.solved();
    }
}
