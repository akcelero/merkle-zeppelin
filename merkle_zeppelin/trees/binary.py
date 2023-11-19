from abc import ABC, abstractmethod
from functools import cached_property
from typing import Generic, TypeVar

T = TypeVar("T")


class BinaryTree(ABC, Generic[T]):
    _nodes: list[T]
    _leafs_number: int

    def __init__(self, leafs: list[T]) -> None:
        self._nodes = leafs
        self._build_tree()

    @property
    def _inner_nodes_number(self) -> int:
        return self._leafs_number - 1

    @property
    def root(self) -> T:
        return self._nodes[0] if len(self._nodes) else None

    @property
    def leafs(self) -> list[T]:
        return self._nodes[-self._leafs_number :]

    @abstractmethod
    def _calculate_parent_value(self, left_children: T, right_children: T) -> T:
        pass

    @cached_property
    def _leafs_number(self) -> int:
        return (len(self._nodes) + 1) // 2

    def _get_node_index(self, leaf_index) -> int:
        return leaf_index + self._inner_nodes_number

    def _build_tree(self) -> None:
        reversed_tree = self._nodes[::-1]
        i = 0

        while i < len(reversed_tree) - 1:
            reversed_tree.append(
                self._calculate_parent_value(
                    left_children=reversed_tree[i], right_children=reversed_tree[i + 1]
                )
            )
            i += 2

        self._nodes = reversed_tree[::-1]

    def _get_left_children_index(self, node_index: int) -> int:
        return ((node_index + 1) * 2) - 1

    def _get_right_children_index(self, node_index: int) -> int:
        return (node_index + 1) * 2

    def _get_neighbor_index(self, node_index: int) -> int:
        return ((node_index + 1) ^ 1) - 1

    def _get_parent_index(self, node_index: int) -> int:
        return ((node_index + 1) // 2) - 1
