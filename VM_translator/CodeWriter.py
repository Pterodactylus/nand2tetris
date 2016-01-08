from Constants import *
import os


class CodeWriter(object):
    
    def __init__(self, output_file):
        self.out = open(output_file, 'w')
        self.vm_file = None
        self.label_num = 0

    def write_init(self):
        self.write_a_command('256')
        self.write_c_command('D', 'A')
        self.comp_to_reg('D', R_SP)
        self.write_call('Sys.init', 0)

    def set_file_name(self, input_file):
        self.vm_file, ext = os.path.splitext(input_file)

    def write_push_pop(self, command, segment, index):
        if command == PUSH_CMD:
            self.gen_push(segment, index)
        elif command == POP_CMD:
            self.gen_pop(segment, index)

    def gen_push(self, segment, index):
        if self.is_constant_segment(segment):
            self.constant_to_stack(str(index))
        elif self.is_memory_segment(segment):
            seg = self.segment_to_asm_label(segment)
            self.mem_to_stack(seg, index)
        elif self.is_static_segment(segment):
            static_name = self.gen_static_name(index)
            self.static_to_stack(static_name)
        elif self.is_reg_segment(segment):
            self.reg_to_stack(segment, index)
        self.increment_sp()

    def gen_pop(self, segment, index):
        self.decrement_sp()
        if self.is_memory_segment(segment):
            seg = self.segment_to_asm_label(segment)
            self.stack_to_mem(seg, index)
        elif self.is_static_segment(segment):
            static_name = self.gen_static_name(index)
            self.stack_to_static(static_name)
        elif self.is_reg_segment(segment):
            self.stack_to_reg(segment, index)

    def constant_to_stack(self, index):
        self.write_a_command(index)
        self.write_c_command('D', 'A')
        self.comp_to_stack('D')

    def mem_to_stack(self, segment, index):
        self.load_segment(segment, index)
        self.write_c_command('D', 'M')
        self.comp_to_stack('D')

    def stack_to_mem(self, segment, index):
        self.load_segment(segment, index)
        self.comp_to_reg('D', R15)
        self.stack_to_dest('D')
        self.reg_to_dest(R15, 'A')
        self.write_c_command('M', 'D')

    def static_to_stack(self, static_name):
        self.write_a_command(static_name)
        self.write_c_command('D', 'M')
        self.comp_to_stack('D')

    def stack_to_static(self, static_name):
        self.stack_to_dest('D')
        self.write_a_command(static_name)
        self.write_c_command('M', 'D')

    def stack_to_reg(self, segment, index):
        self.stack_to_dest('D')
        self.comp_to_reg('D', self.get_reg_index(segment, index))

    def reg_to_stack(self, segment, index):
        self.reg_to_dest(self.get_reg_index(segment, index), 'D')
        self.comp_to_stack('D')

    def is_constant_segment(self, segment):
        return segment == SEG_CONSTANT

    def is_memory_segment(self, segment):
        return segment in [SEG_LOCAL, SEG_ARGUMENT, SEG_THIS, SEG_THAT]

    def is_static_segment(self, segment):
        return segment == SEG_STATIC

    def is_reg_segment(self, segment):
        return segment in [SEG_TEMP, SEG_POINTER, SEG_REG]

    def write_arithmetic(self, cmd_type):
        if cmd_type == 'not':
            self.gen_unary('!D')
        elif cmd_type == 'neg':
            self.gen_unary('-D')
        elif cmd_type == 'add':
            self.gen_binary('D+A')
        elif cmd_type == 'sub':
            self.gen_binary('A-D')
        elif cmd_type == 'and':
            self.gen_binary('D&A')
        elif cmd_type == 'or':
            self.gen_binary('D|A')
        elif cmd_type == 'eq':
            self.gen_compare('JEQ')
        elif cmd_type == 'gt':
            self.gen_compare('JGT')
        elif cmd_type == 'lt':
            self.gen_compare('JLT')

    def write_label(self, label):
        self.write_l_command(label)

    def write_goto(self, label):
        self.write_a_command(label)
        self.write_c_command(None, '0', 'JMP')

    def write_if(self, label):
        self.pop_to_dest('D')
        self.write_a_command(label)
        self.write_c_command(None, 'D', 'JNE')

    def write_call(self, function_name, num_args):
        ret_address = self.gen_label()
        self.gen_push(SEG_CONSTANT, ret_address)
        self.gen_push(SEG_REG, R_LCL)
        self.gen_push(SEG_REG, R_ARG)
        self.gen_push(SEG_REG, R_THIS)
        self.gen_push(SEG_REG, R_THAT)
        self.load_sp_offset(-num_args - 5)
        self.comp_to_reg('D', R_ARG)
        self.reg_to_reg(R_SP, R_LCL)
        self.write_goto(function_name)
        self.write_l_command(ret_address)

    def load_sp_offset(self, offset):
        self.load_segment(self.gen_asm_reg(R_SP), offset)

    def write_return(self):
        self.reg_to_reg(R_LCL, R_FRAME)
        self.write_a_command('5')
        self.write_c_command('A', 'D-A')
        self.write_c_command('D', 'M')
        self.comp_to_reg('D', R_RETURN)
        self.gen_pop(SEG_ARGUMENT, 0)
        self.reg_to_dest(R_ARG, 'D')
        self.comp_to_reg('D+1', R_SP)
        self.frame_to_reg(R_THAT)
        self.frame_to_reg(R_THIS)
        self.frame_to_reg(R_ARG)
        self.frame_to_reg(R_LCL)
        self.reg_to_dest(R_RETURN, 'A')
        self.write_c_command(None, '0', 'JMP')

    def frame_to_reg(self, segment):
        self.reg_to_dest(R_FRAME, 'D')
        self.write_c_command('D', 'D-1')
        self.comp_to_reg('D', R_FRAME)
        self.write_c_command('A', 'D')
        self.write_c_command('D', 'M')
        self.comp_to_reg('D', segment)

    def write_function(self, function_name, num_locals):
        self.write_l_command(function_name)
        for i in range(num_locals):
            self.gen_push(SEG_CONSTANT, 0)

    def gen_unary(self, comp):
        self.decrement_sp()
        self.stack_to_dest('D')
        self.write_c_command('D', comp)
        self.comp_to_stack('D')
        self.increment_sp()

    def gen_binary(self, comp):
        self.decrement_sp()
        self.stack_to_dest('D')
        self.decrement_sp()
        self.stack_to_dest('A')
        self.write_c_command('D', comp)
        self.comp_to_stack('D')
        self.increment_sp()

    def gen_compare(self, jump):
        self.decrement_sp()
        self.stack_to_dest('D')
        self.decrement_sp()
        self.stack_to_dest('A')
        self.write_c_command('D', 'A-D')
        eq_label = self.gen_label_and_jump('D', jump)
        self.comp_to_stack('0')
        neq_label = self.gen_label_and_jump('0', 'JMP')
        self.write_l_command(eq_label)
        self.comp_to_stack('-1')
        self.write_l_command(neq_label)
        self.increment_sp()

    def stack_to_dest(self, dest):
        self.load_sp()
        self.write_c_command(dest, 'M')

    def comp_to_stack(self, comp):
        self.load_sp()
        self.write_c_command('M', comp)

    def comp_to_reg(self, comp, reg):
        self.write_a_command(self.gen_asm_reg(reg))
        self.write_c_command('M', comp)

    def reg_to_dest(self, reg, dest):
        self.write_a_command(self.gen_asm_reg(reg))
        self.write_c_command(dest, 'M')

    def reg_to_reg(self, src, dest):
        self.reg_to_dest(src, 'D')
        self.comp_to_reg('D', dest)

    def pop_to_dest(self, dest):
        self.decrement_sp()
        self.stack_to_dest(dest)

    def load_sp(self):
        self.write_a_command('SP')
        self.write_c_command('A', 'M')

    def load_segment(self, segment, index):
        comp = 'D+A'
        if index < 0:
            index = -index
            comp = 'A-D'
        self.write_a_command(str(index))
        self.write_c_command('D', 'A')
        self.write_a_command(segment)
        self.write_c_command('A', 'M')
        self.write_c_command('AD', comp)

    def increment_sp(self):
        self.write_a_command('SP')
        self.write_c_command('M', 'M+1')

    def decrement_sp(self):
        self.write_a_command('SP')
        self.write_c_command('M', 'M-1')

    def write_a_command(self, address):
        self.out.write('@' + address + '\n')

    def write_c_command(self, dest, comp, jump=None):
        if dest is not None:
            self.out.write(dest + '=')
        self.out.write(comp)
        if jump is not None:
            self.out.write(';' + jump)
        self.out.write('\n')

    def write_l_command(self, label):
        self.out.write('(' + label + ')' + '\n')

    def gen_label_and_jump(self, comp, jump):
        label = self.gen_label()
        self.write_a_command(label)
        self.write_c_command(None, comp, jump)
        return label

    def gen_label(self):
        self.label_num += 1
        return 'LABEL' + str(self.label_num)

    def segment_to_asm_label(self, segment):
        asm_labels = {
            SEG_LOCAL: 'LCL', SEG_THIS: 'THIS',
            SEG_THAT: 'THAT', SEG_ARGUMENT: 'ARG'
        }
        return asm_labels[segment]

    def gen_static_name(self, index):
        return self.vm_file + '.' + str(index)

    def gen_asm_reg(self, reg_num):
        return 'R' + str(reg_num)

    def get_reg_index(self, segment, index):
        return self.get_base_address(segment) + index

    def get_base_address(self, segment):
        base_addresses = {
            'reg': R0, 'pointer': R_PTR, 'temp': R_TEMP
        }
        return base_addresses[segment]

    def close(self):
        """
        Close the file.
        """
        self.out.close()