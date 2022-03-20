pragma solidity 0.4.24;

contract StageDebug {
    event LogCalldata(string where, bytes calldata);
    event Log(string what, uint256 something);
    event Log(string what, bytes32 something);
    event LogEntrypointArgs(bytes4 guess);
    event LogStage1Args(uint8 v, bytes32 r, bytes32 s);
    event LogStage2Args(uint16 a, uint16 b);
    event LogStage3Args(uint256 idx, uint256[4] keys, uint256[4] lock);
    event LogStage4Args(bytes32[6] choices, uint256 choice);

    StageDebug public next;

    constructor(StageDebug next_) public {
        next = next_;
    }

    function getSelector() public view returns (bytes4);

    modifier _() {
        _;

        assembly {
            let next := sload(next_slot)
            if iszero(next) {
                return(0, 0)
            }

            mstore(
                0x00,
                0x034899bc00000000000000000000000000000000000000000000000000000000
            )
            pop(call(gas(), next, 0, 0, 0x04, 0x00, 0x04))
            calldatacopy(0x04, 0x04, sub(calldatasize(), 0x04))
            switch call(gas(), next, 0, 0, calldatasize(), 0, 0)
            case 0 {
                returndatacopy(0x00, 0x00, returndatasize())
                revert(0x00, returndatasize())
            }
            case 1 {
                returndatacopy(0x00, 0x00, returndatasize())
                return(0x00, returndatasize())
            }
        }
    }
}

contract EntrypointDebug is StageDebug {
    constructor() public StageDebug(new Stage1Debug()) {}

    function getSelector() public view returns (bytes4) {
        return this.solve.selector;
    }

    bool public solved;

    function solve(bytes4 guess) public _ {
        // emit LogCalldata("entrypoint", msg.data);
        emit LogEntrypointArgs(guess);
        require(
            guess == bytes4(blockhash(block.number - 1)),
            "do you feel lucky?"
        );

        solved = true;
    }
}

contract Stage1Debug is StageDebug {
    constructor() public StageDebug(new Stage2Debug()) {}

    function getSelector() public view returns (bytes4) {
        return this.solve.selector;
    }

    function solve(
        uint8 v,
        bytes32 r,
        bytes32 s
    ) public _ {
        // emit LogCalldata("stage1", msg.data);
        emit LogStage1Args(v, r, s);
        emit Log('keccak256(stage1")', keccak256("stage1"));

        require(
            ecrecover(keccak256("stage1"), v, r, s) ==
                0x7E5F4552091A69125d5DfCb7b8C2659029395Bdf,
            "who are you?"
        );
    }
}

contract Stage2Debug is StageDebug {
    constructor() public StageDebug(new Stage3Debug()) {}

    function getSelector() public view returns (bytes4) {
        return this.solve.selector;
    }

    function solve(uint16 a, uint16 b) public _ {
        // emit LogCalldata("stage2", msg.data);
        emit LogStage2Args(a, b);
        require(a > 0 && b > 0 && a + b < a, "something doesn't add up");
    }
}

contract Stage3Debug is StageDebug {
    constructor() public StageDebug(new Stage4Debug()) {}

    function getSelector() public view returns (bytes4) {
        return this.solve.selector;
    }

    function solve(
        uint256 idx,
        uint256[4] memory keys,
        uint256[4] memory lock
    ) public _ {
        // emit LogCalldata("stage3", msg.data);
        emit LogStage3Args(idx, keys, lock);

        require(keys[idx % 4] == lock[idx % 4], "key did not fit lock");

        for (uint256 i = 0; i < keys.length - 1; i++) {
            require(keys[i] < keys[i + 1], "out of order");
        }

        for (uint256 j = 0; j < keys.length; j++) {
            require((keys[j] - lock[j]) % 2 == 0, "this is a bit odd");
        }
    }
}

contract Stage4Debug is StageDebug {
    constructor() public StageDebug(new Stage5Debug()) {}

    function getSelector() public view returns (bytes4) {
        return this.solve.selector;
    }

    function solve(bytes32[6] choices, uint256 choice) public _ {
        emit LogStage4Args(choices, choice);
        emit Log(
            'keccak256(abi.encodePacked("choose"))',
            keccak256(abi.encodePacked("choose"))
        );
        require(
            choices[choice % 6] == keccak256(abi.encodePacked("choose")),
            "wrong choice!"
        );
    }
}

contract Stage5Debug is StageDebug {
    constructor() public StageDebug(StageDebug(0x00)) {}

    function getSelector() public view returns (bytes4) {
        return this.solve.selector;
    }

    function solve() public _ {
        emit Log("stage 5 msg.data.length", msg.data.length);
        require(msg.data.length < 256, "a little too long");
    }
}
