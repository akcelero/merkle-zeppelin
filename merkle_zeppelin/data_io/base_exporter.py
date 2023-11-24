from abc import ABC, abstractmethod
from typing import Any

from .dto import MerkleTreeDTO


class MerkleTreeExporter(ABC):
    @staticmethod
    @abstractmethod
    def export_tree(data: MerkleTreeDTO) -> Any:
        ...
