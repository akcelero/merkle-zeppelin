from typing import TypeVar

import pytest

from merkle_zeppelin import BinaryTree

T = TypeVar("T")


@pytest.fixture
def max_tree_class():
    class TestTree(BinaryTree):
        def _calculate_parent_value(self, left_children: T, right_children: T) -> T:
            return max(left_children, right_children)

    return TestTree
