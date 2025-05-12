from abc import ABC, abstractmethod
from typing import Any

from .dto import MerkleTreeDTO


class MerkleTreeImporter(ABC):
    @staticmethod
    @abstractmethod
    def import_tree(data: Any) -> MerkleTreeDTO: ...
