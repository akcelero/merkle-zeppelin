from .base_importer import MerkleTreeImporter
from .dto import MerkleTreeDTO


class MerkleTreeJSONImporter(MerkleTreeImporter):
    @staticmethod
    def import_tree(data: str) -> MerkleTreeDTO:
        return MerkleTreeDTO.model_validate_json(data)
