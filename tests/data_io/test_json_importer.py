from utils import remove_0x

from merkle_zeppelin import MerkleTree, MerkleTreeJSONImporter

from .example import json_dump, leafs


def test_json_import():
    # when
    tree = MerkleTree.import_tree(json_dump, MerkleTreeJSONImporter, validate=True)

    # then
    assert tree.root.hex() == remove_0x(json_dump["tree"][0])
    assert len(tree._nodes) == (len(leafs) * 2) - 1
