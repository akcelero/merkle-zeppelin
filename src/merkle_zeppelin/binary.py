from abc import ABC, abstractmethod
from functools import cached_property
from typing import Generic, TypeVar, Union

T = TypeVar("T")


class BinaryTree(ABC, Generic[T]):
    def __init__(self, leaves: list[T]) -> None:
        self._nodes = leaves
        self._build_tree()

    @abstractmethod
    def _calculate_parent_value(self, left_child: T, right_child: T) -> T: ...

    @property
    def _inner_nodes_number(self) -> int:
        return self._leaves_number - 1

    @property
    def root(self) -> Union[T, None]:
        return self._nodes[0] if self._nodes else None

    @property
    def leaves(self) -> list[T]:
        return self._nodes[-self._leaves_number :]

    @cached_property
    def _leaves_number(self) -> int:
        return (len(self._nodes) + 1) // 2

    def _get_node_index(self, leaf_index) -> int:
        return leaf_index + self._inner_nodes_number

    def _build_tree(self) -> None:
        reversed_tree = self._nodes[::-1]
        i = 0

        while i < len(reversed_tree) - 1:
            reversed_tree.append(
                self._calculate_parent_value(
                    left_child=reversed_tree[i], right_child=reversed_tree[i + 1]
                )
            )
            i += 2

        self._nodes = reversed_tree[::-1]

    def _get_left_child_index(self, node_index: int) -> int:
        return ((node_index + 1) * 2) - 1

    def _get_right_child_index(self, node_index: int) -> int:
        return (node_index + 1) * 2

    def _get_neighbor_index(self, node_index: int) -> int:
        return ((node_index + 1) ^ 1) - 1

    def _get_parent_index(self, node_index: int) -> int:
        return ((node_index + 1) // 2) - 1
