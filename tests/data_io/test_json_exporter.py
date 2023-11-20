from merkle_zeppelin import MerkleTree, MerkleTreeJSONExporter

from ..utils import remove_whitespaces
from .example import json_dump, leafs


def test_json_export() -> None:
    # when
    exported_tree = MerkleTree(leafs, ["int256", "bool"]).export_tree(
        MerkleTreeJSONExporter
    )

    # then
    assert remove_whitespaces(exported_tree) == remove_whitespaces(json_dump)
