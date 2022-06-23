This is a simple proxy-upgradeable smart contract!

Using OpenZeppelin proxy contracts that would allow to direct proxy contract to the new 
logic implementation smart contracts.

Note: Storage Collisions Between Implementation Versions may still happen, the unstructured storage proxy mechanism doesn’t safeguard against this situation. It is up to the user to have new versions of a logic contract extend previous versions, or otherwise guarantee that the storage hierarchy is always appended to but not modified. In any case of collisions, However, OpenZeppelin Upgrades detects such collisions and warns the developer appropriately. 

Technology used: Solidity, Python, Brownie, OpenZeppelin.