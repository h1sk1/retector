pragma solidity ^0.5.7;

contract Test {
	mapping(address => uint) public balances;
	
	function deposit() public payable {
		balances[msg.sender] += msg.value;
	}

	function withdraw(uint amount) public {
		require(balances[msg.sender] >= amount);

		(bool sent, ) = msg.sender.call.value(amount)("");
		require(sent, "Failed to send Ether");

		balances[msg.sender] -= amount;
	}

	function getBalance() public view returns (uint) {
		return address(this).balance;
	}
}
