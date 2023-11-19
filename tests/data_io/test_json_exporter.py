import json

from merkle_zeppelin import MerkleTree, MerkleTreeJSONExporter

from .example import json_dump, leafs


def test_json_export():
    # when
    tree = MerkleTree(leafs, ["int256", "bool"])

    # then
    assert json.loads(tree.export_tree(MerkleTreeJSONExporter)) == json_dump
