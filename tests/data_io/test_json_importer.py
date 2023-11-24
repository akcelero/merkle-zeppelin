import json

from merkle_zeppelin import MerkleTree, MerkleTreeJSONImporter

from ..utils import remove_0x
from .example import json_dump, leafs


def test_json_import() -> None:
    # given
    tree_input = json.loads(json_dump)

    # when
    tree = MerkleTree.import_tree(json_dump, MerkleTreeJSONImporter, validate=True)

    # then
    assert tree.root.hex() == remove_0x(tree_input["tree"][0])
    assert len(tree._nodes) == (len(leafs) * 2) - 1
