import CodeBuilder
import Parser
import SymbolTable
import sys


class Assembler(object):

    def __init__(self):
        self.symbol_table = SymbolTable.SymbolTable()
        # store variable values starting at index 16.
        self.var_addr_count = 16

    def process_labels(self, input_file):
        """
        This is a first pass over the assembly file.
        During it, a- and c- instruction are ignored
        and we only add labels to the symbol table.
        """
        p = Parser.Parser(input_file)
        current_line = 0
        while p.has_more_comamnds():
            p.process()
            cmd_type = p._cmd_type()
            if cmd_type == p.A_CMD or cmd_type == p.C_CMD:
                current_line += 1
            else:
                self.symbol_table.insert_entry(p._sym(), current_line)

    def gen_code(self, input_file, output_file):
        """
        This is a second pass over the assembly file.
        In this case, labels are ignored because they are already in
        the table and only a- and c- instructions are processed.
        """
        p = Parser.Parser(input_file)
        code = CodeBuilder.CodeBuilder()
        out = open(output_file, 'w')
        while p.has_more_comamnds():
            p.process()
            cmd_type = p._cmd_type()
            if cmd_type == p.A_CMD:
                out.write(code.gen_a(self.get_address(p._sym())) + '\n')
            elif cmd_type == p.C_CMD:
                out.write(code.gen_c(p._dest(), p._comp(), p._jump()) + '\n')
            else:
                # In case of a label, skip, because we already processed them.
                pass
        out.close()

    def assemble(self, input_file):
        """
        The starter of assembly process.
        Firstly, process labels followed by
        code generation for a and c instructions.
        """
        self.process_labels(input_file)
        self.gen_code(input_file, self.output(input_file))

    def output(self, output_file):
        """
        Assembly files ending with .asm should end up converted
        to hack machine code, hence output file should have .hack
        extension.
        """
        if output_file.endswith('.asm'):
            return output_file.replace('.asm', '.hack')
        else:
            return output_file + '.hack'

    def get_address(self, sym):
        """
        Add a variable to a symbol table if it is not present.
        """
        if sym.isdigit():
            return int(sym)
        else:
            if not self.symbol_table.contains(sym):
                self.symbol_table.insert_entry(sym, self.var_addr_count)
                self.var_addr_count += 1
            return self.symbol_table.get_address(sym)


def main():
    input_file = None
    if len(sys.argv) != 2:
        print("Usage: python Assembler.py file.asm")
        sys.exit(0)
    else:
        input_file = sys.argv[1]

    a = Assembler()
    a.assemble(input_file)
main()
