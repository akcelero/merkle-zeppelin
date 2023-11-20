from typing import Type, TypeVar

import pytest

from merkle_zeppelin import BinaryTree

T = TypeVar("T")


@pytest.fixture(scope="session")
def max_tree_class() -> Type[BinaryTree]:
    class TestTree(BinaryTree):
        def _calculate_parent_value(self, left_child: T, right_child: T) -> T:
            return max(left_child, right_child)

    return TestTree
