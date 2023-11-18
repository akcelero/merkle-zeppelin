from typing import Any, Callable

from Crypto.Hash import keccak
from eth_abi import encode

from .binary import BinaryTree
from .exceptions import MerkleTreeValidationFailed, ValueNotFoundInTree


def keccak256(v: bytes) -> bytes:
    return keccak.new(data=v, digest_bits=256).digest()


class MerkleTree(BinaryTree[bytes]):
    _raw_leafs: list[list[Any]]
    _hashing_function: Callable[[bytes], bytes]
    _types: list[str]

    def __init__(
        self,
        leafs: list[list[Any]],
        types: list[str],
        hashing_function: Callable[[bytes], bytes] = None,
    ) -> None:
        self._hashing_function = hashing_function or keccak256
        self._types = types
        self._raw_leafs, hashed_leafs = self._get_leafs_data(leafs)

        super().__init__(hashed_leafs)

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

    def get_proofs(self, value: list[Any]) -> list[bytes] | None:
        encoded_leaf = self._calculate_leaf_hash(value)
        try:
            node_index = self._nodes.index(encoded_leaf)
        except ValueError:
            raise ValueNotFoundInTree(value)

        result = []
        while node_index != 0:
            neighbor_index = self._get_neighbor_index(node_index)
            result.append(self._nodes[neighbor_index])

            node_index = self._get_parent_index(node_index)

        return result

    def _calculate_leaf_hash(self, value: list[Any]) -> bytes:
        return self._hashing_function(
            self._hashing_function(encode(self._types, value))
        )

    def _get_leafs_data(self, leafs: list[list[Any]]) -> tuple[list[Any], list[bytes]]:
        if not leafs:
            return [], []

        leafs_with_hashes = [(self._calculate_leaf_hash(leaf), leaf) for leaf in leafs]
        leafs_with_hashes.sort(reverse=True)

        sorted_hashes, sorted_leafs = zip(*leafs_with_hashes)

        return list(sorted_leafs), list(sorted_hashes)

    def _calculate_parent_value(
        self, left_children: bytes, right_children: bytes
    ) -> bytes:
        if None in (left_children, right_children):
            return left_children or right_children
        children_1, children_2 = sorted([left_children, right_children])
        return self._hashing_function(children_1 + children_2)
