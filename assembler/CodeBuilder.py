class CodeBuilder(object):

    def __init__(self):
        self.comp_codes = {
            # a = 0
            '0': '0101010', '1': '0111111', '-1': '0111010',
            'D': '0001100', 'A': '0110000', '!D': '0001101',
            '!A': '0110001', '-D': '0001111', '-A': '0110011',
            'D+1': '0011111', 'A+1': '0110111', 'D-1': '0001110',
            'A-1': '0110010', 'D+A': '0000010', 'D-A': '0010011',
            'A-D': '0000111', 'D&A': '0000000', 'D|A': '0010101',
            # a = 1
            'M': '1110000', '!M': '1110001', '-M': '1110011',
            'M+1': '1110111', 'M-1': '1110010', 'D+M': '1000010',
            'D-M': '1010011', 'M-D': '1000111', 'D&M': '1000000',
            'D|M': '1010101'
        }
        self.dest_codes = [None, 'M', 'D', 'MD', 'A', 'AM', 'AD', 'AMD']
        self.j_codes = [None, 'JGT', 'JEQ', 'JGE', 'JLT', 'JNE', 'JLE', 'JMP']

    def gen_a(self, address):
        """
        Generates 16-bit a-instruction.
        If the address is not 16-bit length, then the rest of the
        length is padded by zeros from the left.
        """
        return '0' + self.bits(address).zfill(15)

    def gen_c(self, dest, comp, jump):
        """
        Generates 16-bit c-instruction.
        """
        return '111' + self.comp(comp) + self.dest(dest) + self.jump(jump)

    def comp(self, comp):
        """
        Gets a computation code from the table.
        """
        return self.comp_codes[comp]

    def dest(self, dest):
        """
        Gets a destination code.
        """
        return self.bits(self.dest_codes.index(dest)).zfill(3)

    def jump(self, jump):
        """
        Gets a jump code.
        """
        return self.bits(self.j_codes.index(jump)).zfill(3)

    def bits(self, address):
        """
        Converts decimal address to binary.
        """
        return '{0:b}'.format(address)
