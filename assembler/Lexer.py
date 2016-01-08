import re

NUMBER = 1  # e.g. 1, 123, 32567
SYMBOL = 2  # e.g. M, AD, loop
OP = 3  # e.g. +, -, !, |, &
ERROR = 4


class Lexer(object):

    def __init__(self, file_name):
        file = open(file_name, 'r')
        self.lines = file.read()
        self.tokens = self.tokenize(self.lines.split('\n'))
        self.cur_cmd = []
        self.cur_tkn = (ERROR, 0)

    def tokenize(self, lines):
        """
        Returns a tokenized list of commands.
        """
        tokenized_lines = [self.tokenize_line(line) for line in lines]
        return [t for t in tokenized_lines if t != []]

    def tokenize_line(self, line):
        """
        Tokenized a command.
        """
        _line = self.remove_comments(line)
        return [self.make_token(tok) for tok in self.split(_line)]

    num_re = r'\d+'
    sym_re = '[' + r'\w.$' + '][' + r'\w.$' + '\d]*'
    op_re = r'[=;()@+\-&|!]'
    tokens_separator = re.compile(num_re + '|' + sym_re + '|' + op_re)

    def split(self, line):
        """
        Separates a command into tokens.
        """
        return self.tokens_separator.findall(line)

    comment_regex = re.compile('//.*$')

    def remove_comments(self, line):
        """
        Removes all characters after //
        """
        return self.comment_regex.sub('', line)

    def make_token(self, token):
        """
        Creates a token tuple of the form (token_type, token)
        """
        if self.is_number(token):
            return (NUMBER, token)
        elif self.is_sym(token):
            return (SYMBOL, token)
        elif self.is_op(token):
            return (OP, token)
        else:
            return (ERROR, 0)

    def next_token(self):
        """
        Returns a next token in the tokenized command
        and removes it from the list.
        """
        if self.has_more_tokens():
            self.cur_tkn = self.cur_cmd.pop(0)
        else:
            self.cur_tkn = (ERROR, 0)
        return self.cur_tkn

    def has_more_commands(self):
        """
        Returns true if all commands were not consumed yet.
        """
        return self.tokens != []

    def has_more_tokens(self):
        """
        Returns true if all tokens were not consumed yet.
        """
        return self.cur_cmd != []

    def next_command(self):
        """
        Returns a next command.
        """
        if self.has_more_commands():
            self.cur_cmd = self.tokens.pop(0)
            self.next_token()
        else:
            self.cur_cmd = []
        return self.cur_cmd

    def inspect_token(self):
        """
        Returns a next token in the tokenized command
        and does not remove it from the list.
        """
        if self.has_more_tokens():
            self.cur_tkn = self.cur_cmd[0]
        else:
            self.cur_tkn = (ERROR, 0)
        return self.cur_tkn

    def is_number(self, token):
        """
        Returns true if token is a number.
        """
        return self.match(self.num_re, token)

    def is_sym(self, token):
        """
        Returns true if token is a symbol.
        """
        return self.match(self.sym_re, token)

    def is_op(self, token):
        """
        Returns true if token is an operator.
        """
        return self.match(self.op_re, token)

    def match(self, regex, token):
        """
        Returns true if regex matches a token.
        """
        return re.match(regex, token)
