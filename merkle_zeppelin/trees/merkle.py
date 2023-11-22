from __future__ import annotations

from operator import itemgetter
from typing import Any, Callable, Type, Union

from Crypto.Hash import keccak
from eth_abi import encode

from ..data_io.base_exporter import MerkleTreeExporter
from ..data_io.base_importer import MerkleTreeImporter
from ..data_io.dto import Leaf, LeafValueDTO, MerkleTreeDTO
from .binary import BinaryTree
from .exceptions import MerkleTreeValidationFailed, ValueNotFoundInTree


def keccak256(v: bytes) -> bytes:
    return keccak.new(data=v, digest_bits=256).digest()


class MerkleTree(BinaryTree[bytes]):
    def __init__(
        self,
        raw_elements: list[Leaf],
        types: list[str],
        hashing_function: Callable[[bytes], bytes] = None,
    ) -> None:
        self._hashing_function = hashing_function or keccak256
        self._types = types

        sorted_index_hash_pairs = self._get_sorted_index_hash_pairs(raw_elements)
        sorted_hashes = [hash_ for index, hash_ in sorted_index_hash_pairs]

        super().__init__(sorted_hashes)

        self._raw_to_leaves_index_mapping = self._get_raw_to_leaves_index_mapping(
            raw_elements, sorted_index_hash_pairs
        )

    @staticmethod
    def get_hash_from_string(hash_: str) -> bytes:
        if hash_.startswith("0x"):
            hash_ = hash_[2:]

        return bytes.fromhex(hash_)

    @classmethod
    def import_tree(
        cls,
        data: Any,
        importer: Type[MerkleTreeImporter],
        validate: bool = True,
        hashing_function: Callable[[bytes], bytes] = None,
    ) -> MerkleTree:
        imported_data = importer.import_tree(data)
        obj = cls.__new__(cls)
        obj._hashing_function = hashing_function or keccak256
        obj._nodes = [
            cls.get_hash_from_string(hash_str) for hash_str in imported_data.tree
        ]
        obj._types = imported_data.leaf_encoding
        obj._raw_to_leaves_index_mapping = {
            value.value: value.tree_index for value in imported_data.values
        }

        if validate:
            cls.validate(obj)

        return obj

    @property
    def dto(self) -> MerkleTreeDTO:
        return MerkleTreeDTO(
            tree=[f"0x{node.hex()}" for node in self._nodes],
            values=[
                LeafValueDTO(value=value, treeIndex=index)
                for value, index in self._raw_to_leaves_index_mapping.items()
            ],
            leafEncoding=self._types,
        )

    def export_tree(self, exporter: Type[MerkleTreeExporter]) -> Any:
        return exporter.export_tree(self.dto)

    def validate(self, raise_exception: bool = True) -> bool:
        calculated_leaves = sorted(
            [
                self._calculate_leaf_hash(value)
                for value in self._raw_to_leaves_index_mapping.keys()
            ],
            reverse=True,
        )
        if self.leaves != calculated_leaves:
            raise MerkleTreeValidationFailed()

        for checked, i in enumerate(range(len(self._nodes) - 1, 0, -2)):
            calculated_parent = self._calculate_parent_value(
                self._nodes[i], self._nodes[i - 1]
            )

            if self._nodes[self._inner_nodes_number - checked - 1] != calculated_parent:
                if not raise_exception:
                    return False

                raise MerkleTreeValidationFailed()

        return True

    # 1470,20 + 4965 = 6445.20

    def get_proofs(self, value: Leaf) -> Union[list[bytes], None]:
        try:
            node_index = self._raw_to_leaves_index_mapping[value]
        except ValueError:
            raise ValueNotFoundInTree(value)

        result = []
        while node_index != 0:
            print(node_index)
            neighbor_index = self._get_neighbor_index(node_index)
            result.append(self._nodes[neighbor_index])

            node_index = self._get_parent_index(node_index)

        return result

    def _get_sorted_index_hash_pairs(
        self, raw_elements: list[Leaf]
    ) -> list[tuple[int, bytes]]:
        hashes = [self._calculate_leaf_hash(el) for el in raw_elements]

        return sorted(
            enumerate(hashes),
            reverse=True,
            key=itemgetter(1),  # sort by hash (second position)
        )

    def _get_raw_to_leaves_index_mapping(
        self, raw_elements: list[Leaf], ordered_hashed_leaves: list[tuple[int, bytes]]
    ) -> dict[Leaf, int]:
        elements_number = len(raw_elements)

        related_indexed_when_sorted = sorted(
            range(elements_number), key=ordered_hashed_leaves.__getitem__
        )

        return {
            leaf: index_in_sorted_by_hash + self._inner_nodes_number
            for leaf, index_in_sorted_by_hash in zip(
                raw_elements, related_indexed_when_sorted
            )
        }

    def _calculate_leaf_hash(self, value: Leaf) -> bytes:
        return self._hashing_function(
            self._hashing_function(encode(self._types, value))
        )

    def _calculate_parent_value(self, left_child: bytes, right_child: bytes) -> bytes:
        child_1, child_2 = sorted([left_child, right_child])
        return self._hashing_function(child_1 + child_2)
