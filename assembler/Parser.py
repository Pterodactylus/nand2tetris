import Lexer


class Parser(object):

    A_CMD = 1
    C_CMD = 2
    L_CMD = 3

    def __init__(self, file_name):
        self.lexer = Lexer.Lexer(file_name)
        self.init_cmd_params()

    def init_cmd_params(self):
        self.cmd_type = None
        self.sym = None
        self.dest = None
        self.comp = None
        self.jump = None

    def _cmd_type(self):
        return self.cmd_type

    def _sym(self):
        return self.sym

    def _dest(self):
        return self.dest

    def _comp(self):
        return self.comp

    def _jump(self):
        return self.jump

    def has_more_comamnds(self):
        return self.lexer.has_more_commands()

    def process(self):
        """
        Selects a processing method for a command
        depending on it's type.
        """
        self.init_cmd_params()
        self.lexer.next_command()
        token_type, value = self.lexer.cur_tkn
        if token_type == Lexer.OP and value == '@':
            self.process_a_instruction()
        elif token_type == Lexer.OP and value == '(':
            self.process_label()
        else:
            self.process_c_instruction(token_type, value)

    def process_a_instruction(self):
        """
        Extracts a symbol from a-instruction.
        """
        self.cmd_type = self.A_CMD
        token_type, self.sym = self.lexer.next_token()

    def process_c_instruction(self, token_type, value):
        """
        C-instructions can take one of the following forms:
          1) dest=comp;jump
          2) dest=comp
          3) comp;jump
          4) comp
        Computation part is always present.
        """
        self.cmd_type = self.C_CMD
        comp_token, comp_value = self.get_dest(token_type, value)
        self.get_comp(comp_token, comp_value)
        self.get_jump()

    def get_dest(self, token_type, value):
        """
        Etracts destination part from the command and returns
        computation part for further processing.
        """
        token, val = self.lexer.inspect_token()
        if token == Lexer.OP and val == '=':
            self.lexer.next_token()
            self.dest = value
            comp_token, comp_value = self.lexer.next_token()
        else:
            comp_token, comp_value = token_type, value
        return (comp_token, comp_value)

    def get_comp(self, token_type, value):
        """
        Extracts computation part from the command.
        """
        if token_type == Lexer.OP and (value == '-' or value == '!'):
            comp_token, comp_value = self.lexer.next_token()
            self.comp = value + comp_value
        elif token_type == Lexer.NUMBER or token_type == Lexer.SYMBOL:
            self.comp = value
            tok, val = self.lexer.inspect_token()
            if tok == Lexer.OP and val != ';':
                self.lexer.next_token()
                tok1, val1 = self.lexer.next_token()
                self.comp += (val + val1)

    def get_jump(self):
        """
        Extracts the jump part from the command.
        """
        tok, val = self.lexer.next_token()
        if tok == Lexer.OP and val == ';':
            tok, val = self.lexer.next_token()
            self.jump = val

    def process_label(self):
        """
        Extracts label from the command.
        """
        self.cmd_type = self.L_CMD
        token_type, self.sym = self.lexer.next_token()
