import re

NUMBER = 1  # e.g. 1, 123, 32434
SYMBOL = 2  # push, pop, constant
ERROR = 3


class Lexer(object):

    def __init__(self, file_name):
        file = open(file_name, 'r')
        self.lines = file.read()
        self.tokens = self.tokenize(self.lines.split('\n'))
        self.cur_cmd = []
        self.cur_tkn = (ERROR, 0)

    def tokenize(self, lines):
        tokenized_lines = [self.tokenize_line(line) for line in lines]
        return [t for t in tokenized_lines if t != []]

    def tokenize_line(self, line):
        _line = self.remove_comments(line)
        return [self.make_token(tok) for tok in self.split(_line)]

    def has_more_tokens(self):
        return self.cur_cmd != []

    def next_token(self):
        if self.has_more_tokens():
            self.cur_tkn = self.cur_cmd.pop(0)
        else:
            self.cur_tkn = (ERROR, 0)
        return self.cur_tkn

    def has_more_commands(self):
        return self.tokens != []

    def next_command(self):
        if self.has_more_commands():
            self.cur_cmd = self.tokens.pop(0)
            self.next_token()
        else:
            self.cur_cmd = []
        return self.cur_cmd

    def inspect_token(self):
        if self.has_more_tokens():
            self.cur_tkn = self.cur_cmd[0]
        else:
            self.cur_tkn = (ERROR, 0)
        return self.cur_tkn

    num_re = r'\d+'
    sym_re = r'[\w\-.]+'
    tokens_separator = re.compile(num_re + '|' + sym_re)

    def split(self, line):
        return self.tokens_separator.findall(line)

    comment_regex = re.compile('//.*$')

    def remove_comments(self, line):
        return self.comment_regex.sub('', line)

    def make_token(self, token):
        if self.is_number(token):
            return (NUMBER, token)
        elif self.is_sym(token):
            return (SYMBOL, token)
        else:
            return (ERROR, 0)

    def is_number(self, token):
        return self.match(self.num_re, token)

    def is_sym(self, token):
        return self.match(self.sym_re, token)

    def match(self, regex, token):
        return re.match(regex, token)
