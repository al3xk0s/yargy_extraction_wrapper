from yargy import rule
from yargy.interpretation import fact
from yargy.pipelines import morph_pipeline
from yargy.predicates import type as type_

from yargy_extraction_wrapper import RuleWrapper, parse


def main():
    src = 'Это число рабочих 43 или число рабочих 53, но это не точно'

    CountFact = fact('CountFact', ['value'])
    PREFIX = morph_pipeline(['число рабочих'])

    COUNT = rule(PREFIX, type_('INT').interpretation(CountFact.value)).interpretation(CountFact)

    CountsFact = fact('CountsFact', ['first', 'second'])

    ROOT = rule(
        COUNT.interpretation(CountsFact.first),
        COUNT.interpretation(CountsFact.second)
    ).interpretation(CountsFact)

    w = RuleWrapper(root=ROOT, rules_to_tokenize=(COUNT,))
    s, ms = parse(src, w)
    print(s)
    print([_.fact for _ in ms])


if __name__ == '__main__':
    main()
