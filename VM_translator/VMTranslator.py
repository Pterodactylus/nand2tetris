import Parser
import CodeWriter
import os
import glob
import sys
from Constants import *


class VMTranslator(object):

    def __init__(self):
        pass

    def convert_all_files(self, input_files, output_file):
        """
        For each input file, commands contained in it are
        converted to assembly and written into one output
        file.
        """
        if input_files != []:
            code_writer = CodeWriter.CodeWriter(output_file)
            code_writer.write_init()
            for input_file in input_files:
                self.convert(input_file, code_writer)
            code_writer.close()

    def convert(self, input_file, code_writer):
        """
        An input file is processed command by command.
        """
        p = Parser.Parser(input_file)
        code_writer.set_file_name(os.path.basename(input_file))
        while p.has_more_commands():
            p.advance()
            self.generate_code(p, code_writer)

    def generate_code(self, p, code_writer):
        cmd_type = p.command_type()
        if cmd_type == ARITHMETIC_CMD:
            code_writer.write_arithmetic(p.get_arg1())
        elif cmd_type == PUSH_CMD or cmd_type == POP_CMD:
            code_writer.write_push_pop(cmd_type, p.get_arg1(), p.get_arg2())
        elif cmd_type == LABEL_CMD:
            code_writer.write_label(p.get_arg1())
        elif cmd_type == GOTO_CMD:
            code_writer.write_goto(p.get_arg1())
        elif cmd_type == IF_CMD:
            code_writer.write_if(p.get_arg1())
        elif cmd_type == FUNC_CMD:
            code_writer.write_function(p.get_arg1(), p.get_arg2())
        elif cmd_type == CALL_CMD:
            code_writer.write_call(p.get_arg1(), p.get_arg2())
        elif cmd_type == RET_CMD:
            code_writer.write_return()


def main():
    if len(sys.argv) != 2:
        print("Usage: VMTranslator input_file_dir")
    else:
        input_files, output_file = get_files(sys.argv[1])
        vm_translator = VMTranslator()
        vm_translator.convert_all_files(input_files, output_file)


def get_files(input_files):
    if input_files.endswith('.vm'):
        return [input_files], input_files.replace('.vm', '.asm')
    else:
        input = glob.glob(input_files + '/*.vm')
        basename = os.path.basename(input[0])
        output_file = input_files + '//' + basename.replace('.vm', '.asm')
        return input, output_file

main()
