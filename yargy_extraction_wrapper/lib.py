from typing import Sequence

from yargy import *
from yargy.predicates import is_title
from yargy.tokenizer import *
from yargy.interpretation import *
from yargy.rule import *

from yargy_extraction_wrapper.rule_wrapper import RuleWrapper


class IdTokenizer(Tokenizer):
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def split(self, text):
        return self.tokenizer.split(text)

    def check_type(self, t):
        return self.tokenizer.check_type(t)

    @property
    def morph(self):
        return self.tokenizer.morph

    def __call__(self, tokens):
        return tokens

    @staticmethod
    def default(rules=RULES):
        TOKENIZER = MorphTokenizer(rules=rules).remove_types(EOL)
        return IdTokenizer(TOKENIZER)


def _is_inside_span(token, span):
    token_span = token.span
    return span.start <= token_span.start and token_span.stop <= span.stop


def _select_span_tokens(tokens, spans):
    for token in tokens:
        if any(_is_inside_span(token, _) for _ in spans):
            yield token


def _get_needed_tokens(text: str, t: IdTokenizer, rules: Sequence[Rule]):
    ID_TOKENIZER = t
    TOKENIZER = t.tokenizer

    Proxy = fact(
        'Proxy',
        ['value'],
    )

    r = or_(*rules).interpretation(Proxy.value).interpretation(Proxy)
    tokens = list(TOKENIZER(text))
    matches = Parser(r, tokenizer=ID_TOKENIZER).findall(tokens)
    spans = [m.span for m in matches]

    return list(_select_span_tokens(tokens, spans))


OLD_RUSSIAN_TOKEN_RULE = TokenRule(RUSSIAN, r'[а-яёіѣѳv]+')
OLD_RUSSIAN_TOKEN_RULES = [OLD_RUSSIAN_TOKEN_RULE, *RULES[1:]]


def parse(text: str, rule_wrapper: RuleWrapper, token_rules: Sequence[TokenRule] | None = None):
    token_rules = token_rules if token_rules is not None else OLD_RUSSIAN_TOKEN_RULES
    ID_TOKENIZER = IdTokenizer.default(token_rules)
    if rule_wrapper.rules_to_tokenize is not None:
        needed_tokens = _get_needed_tokens(text, ID_TOKENIZER, rule_wrapper.rules_to_tokenize)
        print([t.value for t in needed_tokens])
        return Parser(rule_wrapper.root, tokenizer=ID_TOKENIZER).findall(needed_tokens)

    return Parser(rule_wrapper.root, tokenizer=ID_TOKENIZER.tokenizer).findall(text)
