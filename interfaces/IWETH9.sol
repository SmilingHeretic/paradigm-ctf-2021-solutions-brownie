pragma solidity 0.8.0;

import "./IERC20Like.sol";

interface IWETH9 is IERC20Like {
    function deposit() external payable;

    function withdraw(uint256 wad) external;
}
