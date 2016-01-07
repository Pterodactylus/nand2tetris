import Lexer
from Constants import *


class Parser(object):

    commands = {
        'add': ARITHMETIC_CMD, 'sub': ARITHMETIC_CMD, 'eq': ARITHMETIC_CMD,
        'neg': ARITHMETIC_CMD, 'lt': ARITHMETIC_CMD, 'gt': ARITHMETIC_CMD,
        'and': ARITHMETIC_CMD, 'or': ARITHMETIC_CMD, 'not': ARITHMETIC_CMD,

        'if-goto': IF_CMD, 'goto': GOTO_CMD, 'label': LABEL_CMD,

        'function': FUNC_CMD, 'call': CALL_CMD, 'return': RET_CMD,

        'push': PUSH_CMD, 'pop': POP_CMD
    }

    zero = \
        ['add', 'sub', 'eq', 'neg', 'gt', 'lt', 'and', 'or', 'not', 'return']
    one = ['if-goto', 'goto', 'label']
    two = ['push', 'pop', 'function', 'call']

    def __init__(self, file_name):
        self.lexer = Lexer.Lexer(file_name)
        self.init_cmd_params()

    def init_cmd_params(self):
        self.cmd_type = None
        self.arg1 = None
        self.arg2 = 0

    def has_more_commands(self):
        return self.lexer.has_more_commands()

    def advance(self):
        self.init_cmd_params()
        self.lexer.next_command()
        token, value = self.lexer.cur_tkn
        if value in self.zero:
            self.process_zero_arg_command(value)
        elif value in self.one:
            self.process_one_arg_command(value)
        elif value in self.two:
            self.process_two_arg_command(value)
        else:
            raise ValueError("An unrecognized command was detected: ", value)

    def process_zero_arg_command(self, value):
        """
        As per slides, arg1 is set to arithmetic operation
        type only when op type is ARITHMETIC_CMD.
        """
        self.set_cmd_type(value)
        if self.commands[value] == ARITHMETIC_CMD:
            self.arg1 = value

    def process_one_arg_command(self, value):
        """
        When command has an argument, then arg1
        is set to second token value.
        """
        self.process_zero_arg_command(value)
        tok, val = self.lexer.next_token()
        self.arg1 = val

    def process_two_arg_command(self, value):
        """
        When command has two arguments, then arg1
        is set to second token value and third token's
        value is converted to integer and assigned to
        arg2.
        """
        self.process_one_arg_command(value)
        tok, val = self.lexer.next_token()
        self.arg2 = int(val)

    def set_cmd_type(self, val):
        self.cmd_type = self.commands[val]

    def command_type(self):
        return self.cmd_type

    def get_arg1(self):
        return self.arg1

    def get_arg2(self):
        return self.arg2
