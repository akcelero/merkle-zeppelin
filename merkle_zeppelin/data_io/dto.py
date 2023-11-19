from typing import Any

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

Leaf = tuple[Any, ...]


class LeafValueDTO(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    value: Leaf
    tree_index: int


class MerkleTreeDTO(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    format: str = Field("standard-v1", frozen=True)
    tree: list[str]
    values: list[LeafValueDTO]
    leaf_encoding: list[str]
