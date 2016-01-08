class SymbolTable(object):

    def __init__(self):
        self.symbols = {
            'R0': 0, 'R1': 1, 'R2': 2,
            'R3': 3, 'R4': 4, 'R5': 5,
            'R6': 6, 'R7': 7, 'R8': 8,
            'R9': 9, 'R10': 10, 'R11': 11,
            'R12': 12, 'R13': 13, 'R14': 14,
            'R15': 15,

            'SP': 0, 'LCL': 1, 'ARG': 2,
            'THIS': 3, 'THAT': 4, 'SCREEN': 16384,
            'KBD': 24576
        }

    def contains(self, sym):
        """
        Returns true if symbol is in symol table.
        """
        return sym in self.symbols

    def insert_entry(self, sym, addr):
        """
        Stores address in symbol table.
        """
        self.symbols[sym] = addr

    def get_address(self, sym):
        """
        Gets address associated with sym from symbol table.
        """
        return self.symbols[sym]
