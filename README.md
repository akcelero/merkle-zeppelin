# merkle-zeppelin
Yet another MerkleTree library with implementation aligned to openzeppelin implementation

### How Tree is constructed
Animations shows how algorithm builds tree for later checking or counting proofs.
Letters on the bottom represents list of numbers in program memory.

![Constructing tree](images/tree_construction.gif)

Notice that each node number in final tree when divided by 2 (without rest) gives its parent number. That's why `None` is needed there, otherwise there is no such a rule.

Each element represented by single or few letters is hashed value.
let's assume `a, ..., e` are given values, then `A = hash(a), ..., E = hash(e)` and `AB = hash(A + B) = hash(hash(a) + hash(b))` and so on...

Using this library you can choose which hash function is used, default `keccak256` is used (as in [original implementation](https://github.com/OpenZeppelin/merkle-tree]))
