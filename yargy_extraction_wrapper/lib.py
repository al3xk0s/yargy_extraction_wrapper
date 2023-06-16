import gzip
from typing import Sequence

import cloudpickle
from yargy import *
from yargy.interpretation import *
from yargy.rule import *

from yargy_extraction_wrapper.id_tokenizer import IdTokenizer
from yargy_extraction_wrapper.rule_wrapper import RuleWrapper


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

    Proxy = fact('Proxy', ['value'])

    r = or_(*rules).interpretation(Proxy.value).interpretation(Proxy)
    tokens = list(TOKENIZER(text))
    matches = Parser(r, tokenizer=ID_TOKENIZER).findall(tokens)
    spans = [m.span for m in matches]

    return spans, list(_select_span_tokens(tokens, spans))


def _parse_rules_to_tokenize(text: str, rule_wrapper: RuleWrapper, t: IdTokenizer):
    spans, needed_tokens = _get_needed_tokens(text, t, rule_wrapper.rules_to_tokenize)
    return spans, Parser(rule_wrapper.root, tokenizer=t).findall(needed_tokens)


def _get_tokenizer(rule_wrapper: RuleWrapper):
    return IdTokenizer(rule_wrapper.tokenizer)


def parse(text: str, rule_wrapper: RuleWrapper) -> tuple[Sequence, Sequence]:
    ID_TOKENIZER = _get_tokenizer(rule_wrapper)
    if rule_wrapper.rules_to_tokenize is not None:
        return _parse_rules_to_tokenize(text, rule_wrapper, t=ID_TOKENIZER)
    ms = list(Parser(rule_wrapper.root, tokenizer=ID_TOKENIZER.tokenizer).findall(text))
    return [_.span for _ in ms], ms


def serialize(rule_wrapper: RuleWrapper):
    if not isinstance(rule_wrapper, RuleWrapper):
        raise ValueError('value is not RuleWrapper')
    return gzip.compress(cloudpickle.dumps(rule_wrapper))
