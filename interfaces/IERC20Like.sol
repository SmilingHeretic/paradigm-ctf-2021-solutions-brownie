pragma solidity 0.8.0;

interface IERC20Like {
    function transfer(address dst, uint256 qty) external returns (bool);

    function transferFrom(
        address src,
        address dst,
        uint256 qty
    ) external returns (bool);

    function approve(address dst, uint256 qty) external returns (bool);

    function balanceOf(address who) external view returns (uint256);
}
