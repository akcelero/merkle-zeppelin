from .base_exporter import MerkleTreeExporter
from .dto import MerkleTreeDTO


class MerkleTreeJSONExporter(MerkleTreeExporter):
    @staticmethod
    def export_tree(data: MerkleTreeDTO) -> str:
        return data.model_dump_json(by_alias=True)
