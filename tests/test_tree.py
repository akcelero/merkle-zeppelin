from typing import Type

import pytest

from merkle_zeppelin import BinaryTree


@pytest.mark.parametrize("elements_number", [1, 2, 3, 4, 5, 6, 9, 1025, 2049])
def test_good_leafs_number(
    elements_number: int, max_tree_class: Type[BinaryTree]
) -> None:
    # given
    leafs = [x for x in range(elements_number)]

    # when
    tree = max_tree_class(leafs)

    # then
    assert tree._leafs_number == elements_number
    # assert len(tree.leafs) == leafs_number


@pytest.mark.parametrize(
    "leafs",
    [
        [1, 2, 5, 4, 3],
        [26472, 10667, 22111, 19925, 15135, 25522, 19383, 18057],
        [29715, 8094, 18041, 21052, 15250, 18438, 1879, 715],
        [20607, 10144, 10075, 61, 8197, 23269, 14590, 25693],
        [10898, 18333, 25450, 19457, 17669, 19407, 26586, 2095],
        [10171, 13737, 19959, 14751, 29357, 6577, 4135, 27798],
        [11849, 28493, 22446, 20890, 9573, 6113, 29817, 26202],
        [7441, 24459, 6555, 25589, 19987, 23087, 24115, 21862],
        [649, 1296, 9577, 21225, 681, 18841, 15450, 17768],
        [9370, 6598, 19794, 18938, 7393, 4704, 25252, 9960],
        [5564, 3366, 13713, 15915, 27151, 5527, 14180, 27597],
    ],
)
def test_tree_root(leafs: list[int], max_tree_class: Type[BinaryTree]) -> None:
    # when
    tree = max_tree_class(leafs)

    # then
    assert tree.root == max(leafs)


def test_one_node(max_tree_class: Type[BinaryTree]) -> None:
    # given
    leaf = 1
    leafs = [leaf]

    # when
    tree = max_tree_class(leafs)

    # then
    assert tree.root == leaf
    assert len(tree.leafs) == 1


def test_empty_nodes(max_tree_class: Type[BinaryTree]) -> None:
    # when
    tree = max_tree_class([])

    # then
    assert tree.root is None
    assert tree.leafs == []
