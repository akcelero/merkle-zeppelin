from typing import Any, Callable

from Crypto.Hash import keccak
from eth_abi import encode

from .binary import BinaryTree
from .exceptions import MerkleTreeValidationFailed, ValueNotFoundInTree

Leaf = tuple[Any, ...]


def keccak256(v: bytes) -> bytes:
    return keccak.new(data=v, digest_bits=256).digest()


class MerkleTree(BinaryTree[bytes]):
    _raw_leafs_index: dict[Leaf, int]
    _hashing_function: Callable[[bytes], bytes]
    _types: list[str]

    def __init__(
        self,
        leafs: list[Leaf],
        types: list[str],
        hashing_function: Callable[[bytes], bytes] = None,
    ) -> None:
        self._hashing_function = hashing_function or keccak256
        self._types = types

        hash_leaf_pairs = self._get_hash_leaf_pairs(leafs)
        hash_leaf_pairs.sort(reverse=True)

        ordered_hashed_leafs = [leaf_hash for leaf_hash, _ in hash_leaf_pairs]
        ordered_leafs = [leaf for _, leaf in hash_leaf_pairs]

        super().__init__(ordered_hashed_leafs)

        self._raw_leafs_index = self._get_raw_leafs_index(ordered_leafs)

    @property
    def hashed_leafs(self) -> list[bytes]:
        return self._nodes[self._inner_nodes_number :]

    def validate(self, raise_exception: bool = True) -> bool:
        for i in range(1, self._inner_nodes_number):
            left_node_index = self._get_left_children_index(i)
            right_node_index = self._get_right_children_index(i)
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
            node_index = self._raw_leafs_index[value]
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

    def _get_hash_leaf_pairs(self, input_leafs: list[Leaf]) -> list[tuple[bytes, Leaf]]:
        return [(self._calculate_leaf_hash(leaf), leaf) for leaf in input_leafs]

    def _get_raw_leafs_index(self, hash_leaf_pairs: list[Leaf]) -> dict[Leaf, int]:
        return {leaf: self._get_node_index(i) for i, leaf in enumerate(hash_leaf_pairs)}

    def _calculate_parent_value(
        self, left_children: bytes, right_children: bytes
    ) -> bytes:
        children_1, children_2 = sorted([left_children, right_children])
        return self._hashing_function(children_1 + children_2)
