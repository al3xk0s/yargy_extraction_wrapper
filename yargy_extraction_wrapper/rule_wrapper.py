import dataclasses
from typing import Sequence, Callable

from yargy.rule import Rule
from yargy.tokenizer import TokenRule, RUSSIAN, RULES, MorphTokenizer, EOL

OLD_RUSSIAN_TOKEN_RULE = TokenRule(RUSSIAN, r'[а-яёіѣѳv]+')
OLD_RUSSIAN_TOKEN_RULES = [OLD_RUSSIAN_TOKEN_RULE, *RULES[1:]]


def get_morph_tokenizer():
    return MorphTokenizer(rules=OLD_RUSSIAN_TOKEN_RULES).remove_types(EOL)


@dataclasses.dataclass(frozen=True)
class RuleWrapper:
    root: Rule
    rules_to_tokenize: Sequence[Rule] | None = None
    tokenizer: Sequence[TokenRule] = dataclasses.field(default_factory=get_morph_tokenizer)
