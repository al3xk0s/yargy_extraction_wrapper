from yargy.tokenizer import RULES, MorphTokenizer, EOL, Tokenizer


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
