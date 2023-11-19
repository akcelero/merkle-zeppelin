from typing import Any, Callable

from Crypto.Hash import keccak
from eth_abi import encode

from .binary import BinaryTree
from .exceptions import MerkleTreeValidationFailed, ValueNotFoundInTree

Leaf = tuple[Any, ...]


def keccak256(v: bytes) -> bytes:
    return keccak.new(data=v, digest_bits=256).digest()


class MerkleTree(BinaryTree[bytes]):
    def __init__(
        self,
        leaves: list[Leaf],
        types: list[str],
        hashing_function: Callable[[bytes], bytes] = None,
    ) -> None:
        self._hashing_function = hashing_function or keccak256
        self._types = types

        hash_leaf_pairs = self._get_hash_leaf_pairs(leaves)
        hash_leaf_pairs.sort(reverse=True)

        ordered_hashed_leaves = [leaf_hash for leaf_hash, _ in hash_leaf_pairs]
        ordered_leaves = [leaf for _, leaf in hash_leaf_pairs]

        super().__init__(ordered_hashed_leaves)

        self._raw_leaves_index = self._get_raw_leaves_index(ordered_leaves)

    def validate(self, raise_exception: bool = True) -> bool:
        for i in range(1, self._inner_nodes_number):
            left_node_index = self._get_left_child_index(i)
            right_node_index = self._get_right_child_index(i)
            calculated_parent = self._calculate_parent_value(
                self._nodes[left_node_index], self._nodes[right_node_index]
            )

            if self._nodes[i] != calculated_parent:
                if not raise_exception:
                    return False

                raise MerkleTreeValidationFailed()

        return True

    def get_proofs(self, value: Leaf) -> list[bytes] | None:
        try:
            node_index = self._raw_leaves_index[value]
        except ValueError:
            raise ValueNotFoundInTree(value)

        result = []
        while node_index != 0:
            neighbor_index = self._get_neighbor_index(node_index)
            result.append(self._nodes[neighbor_index])

            node_index = self._get_parent_index(node_index)

        return result

    def _calculate_leaf_hash(self, value: Leaf) -> bytes:
        return self._hashing_function(
            self._hashing_function(encode(self._types, value))
        )

    def _get_hash_leaf_pairs(
        self, input_leaves: list[Leaf]
    ) -> list[tuple[bytes, Leaf]]:
        return [(self._calculate_leaf_hash(leaf), leaf) for leaf in input_leaves]

    def _get_raw_leaves_index(self, hash_leaf_pairs: list[Leaf]) -> dict[Leaf, int]:
        return {leaf: self._get_node_index(i) for i, leaf in enumerate(hash_leaf_pairs)}

    def _calculate_parent_value(self, left_child: bytes, right_child: bytes) -> bytes:
        child_1, child_2 = sorted([left_child, right_child])
        return self._hashing_function(child_1 + child_2)
