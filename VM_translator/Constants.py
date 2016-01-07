# Command types
ARITHMETIC_CMD = 0
PUSH_CMD = 1
POP_CMD = 2
LABEL_CMD = 3
IF_CMD = 4
GOTO_CMD = 5
FUNC_CMD = 6
RET_CMD = 7
CALL_CMD = 8

# Memory segments
SEG_CONSTANT = 'constant'
SEG_LOCAL = 'local'
SEG_THIS = 'this'
SEG_THAT = 'that'
SEG_ARGUMENT = 'argument'
SEG_STATIC = 'static'
SEG_TEMP = 'temp'
SEG_POINTER = 'pointer'
SEG_REG = 'reg'

# Registers
R0 = R_SP = 0
R1 = R_LCL = 1
R2 = R_ARG = 2
R3 = R_THIS = R_PTR = 3
R4 = R_THAT = 4
R5 = R_TEMP = 5
R6 = 6
R7 = 7
R8 = 8
R9 = 9
R10 = 10
R11 = 11
R12 = 12
R13 = 13
R14 = R_FRAME = 14
R15 = 15
