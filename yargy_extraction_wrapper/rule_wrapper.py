import dataclasses
from typing import Sequence, Callable

from yargy.rule import Rule
from yargy.tokenizer import TokenRule, RUSSIAN, RULES, MorphTokenizer, EOL

OLD_RUSSIAN_TOKEN_RULE = TokenRule(RUSSIAN, r'[а-яёіѣѳv]+')
OLD_RUSSIAN_TOKEN_RULES = [OLD_RUSSIAN_TOKEN_RULE, *RULES[1:]]


def get_morph_tokenizer(rules: Sequence[TokenRule]):
    return MorphTokenizer(rules=rules).remove_types(EOL)


@dataclasses.dataclass(frozen=True)
class RuleWrapper:
    root: Rule
    rules_to_tokenize: Sequence[Rule] | None = None
    tokenizer_rules: Sequence[TokenRule] = dataclasses.field(default_factory=lambda: OLD_RUSSIAN_TOKEN_RULES)
    tokenizer_factory: Callable = get_morph_tokenizer
