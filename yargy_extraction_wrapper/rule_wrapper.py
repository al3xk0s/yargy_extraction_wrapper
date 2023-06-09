import dataclasses
from typing import Sequence

from yargy.rule import Rule


@dataclasses.dataclass(frozen=True)
class RuleWrapper:
    root: Rule
    rules_to_tokenize: Sequence[Rule] | None = None
