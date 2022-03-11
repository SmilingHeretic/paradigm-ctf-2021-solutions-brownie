pragma solidity 0.7.0;

import "./BabySandbox.sol";

contract BabySandboxSetup {
    BabySandbox public sandbox;

    constructor() {
        sandbox = new BabySandbox();
    }

    function isSolved() public view returns (bool) {
        uint256 size;
        assembly {
            size := extcodesize(sload(sandbox.slot))
        }
        return size == 0;
    }
}
