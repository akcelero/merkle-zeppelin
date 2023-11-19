import pytest

from merkle_zeppelin import MerkleTree


@pytest.mark.parametrize(
    "leaves, encoded_leaves",
    [
        (
            [(1,), (2,), (3,), (4,), (5,)],
            [
                "c167b0e3c82238f4f2d1a50a8b3a44f96311d77b148c30dc0ef863e1a060dcb6",
                "b5d9d894133a730aa651ef62d26b0ffa846233c74177a591a4a896adfda97d22",
                "2584db4a68aa8b172f70bc04e2e74541617c003374de6eb4b295e823e5beab01",
                "1ab0c6948a275349ae45a06aad66a8bd65ac18074615d53676c09b67809099e0",
                "16db2e4b9f8dc120de98f8491964203ba76de27b27b29c2d25f85a325cd37477",
            ],
        ),
        ([(1,)], ["b5d9d894133a730aa651ef62d26b0ffa846233c74177a591a4a896adfda97d22"]),
    ],
)
def test_leaves_hashes(leaves: list[tuple[int]], encoded_leaves: list[bytes]) -> None:
    # when
    merkle = MerkleTree(leaves, ["int256"])

    # then
    assert [
        leaf.hex() for leaf in merkle.leaves[: len(encoded_leaves)]
    ] == encoded_leaves


@pytest.mark.parametrize(
    "leaves_number, duplication_number", [(3, 1), (5, 3), (1, 0), (9, 7)]
)
def check_last_leaf_duplication(leaves_number: int, duplication_number: int) -> None:
    # given
    leaves = [(1,) * (leaves_number - 1)] + [(2,)]
    encoded_duplicate = (
        "1ab0c6948a275349ae45a06aad66a8bd65ac18074615d53676c09b67809099e0"
    )

    # when
    merkle = MerkleTree(leaves, ["int256"])

    # then
    assert all(encoded_duplicate == leaf.hex() for leaf in merkle.leaves[len(leaves) :])


@pytest.mark.parametrize(
    "proofs, leaves, leaf_to_get_proof",
    [
        (
            [
                "e0dc9f9896b930abf99b0dc6f27786fb16feda8ef139b7adaae3b470c907c116",
                "9385965ba65029c2cbdb3782f35b755a76788ef236602b98118ef535cca36e5c",
            ],
            [(123, True), (71254, False), (42386, True), (52342, False)],
            0,
        ),
        (
            [
                "85a249a14aa3de1fe84ded5d136b81ad5840b98df7dd2499e503b4c0c0ffe0bc",
                "aa703a7581435317f02af31a3e3fdd413260475bc61516500e610b94860ede1b",
                "d8484219986b351fc0b8c13ce5d1100819fceadab72e652da542b5720975329f",
            ],
            [
                (123, True),
                (71254, False),
                (42386, True),
                (52342, False),
                (92342431, True),
                (53245, True),
                (1, True),
                (9876, False),
                (10000, False),
            ],
            8,
        ),
    ],
)
def test_proofs(
    proofs: list[str], leaves: list[tuple[int, bool]], leaf_to_get_proof: int
) -> None:
    # given
    types = ["int256", "bool"]
    tree = MerkleTree(leaves, types)

    # when
    retrieved_proofs = tree.get_proofs(leaves[leaf_to_get_proof])

    # then
    assert [proof.hex() for proof in retrieved_proofs] == proofs


def test_one_node() -> None:
    # given
    leaves = [(1,)]
    encoded_leaf = "b5d9d894133a730aa651ef62d26b0ffa846233c74177a591a4a896adfda97d22"

    # when
    tree = MerkleTree(leaves, ["int256"])

    # then
    assert tree.root.hex() == encoded_leaf
    assert [leaf.hex() for leaf in tree.leaves] == [encoded_leaf]


def test_empty_nodes() -> None:
    # given
    leaf = (1,)

    # when
    tree = MerkleTree([], ["int256"])
    validation = tree.validate()
    with pytest.raises(Exception) as proof_exception:
        tree.get_proofs(leaf)

    # then
    assert validation
    assert tree.root is None
    assert tree.leaves == []
    assert proof_exception.value.args[0] == leaf
