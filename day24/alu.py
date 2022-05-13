from collections import defaultdict
from copy import deepcopy

"""
The ALU is a four-dimensional processing unit: it has integer variables w, x, y, and z. These variables all start with the value 0. The ALU also supports six instructions:

inp a - Read an input value and write it to variable a.
add a b - Add the value of a to the value of b, then store the result in variable a.
mul a b - Multiply the value of a by the value of b, then store the result in variable a.
div a b - Divide the value of a by the value of b, truncate the result to an integer, then store the result in variable a. (Here, "truncate" means to round the value toward zero.)
mod a b - Divide the value of a by the value of b, then store the remainder in variable a. (This is also called the modulo operation.)
eql a b - If the value of a and b are equal, then store the value 1 in variable a. Otherwise, store the value 0 in variable a.
"""

# existing registers
registers = {"w", "x", "y", "z"}


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


class OpInp(object):
    def __init__(self, reg_data, inp_stream, dst):
        assert dst in registers
        self.reg_data = reg_data
        self.inp_stream = inp_stream
        self.dst = dst

    def compute(self):
        assert len(self.inp_stream) > 0
        val = self.inp_stream.pop(0)
        self.reg_data[self.dst] = int(val)


class OpAdd(object):
    def __init__(self, reg_data, dst, b):
        assert dst in registers
        assert b in registers or is_number(b)
        self.reg_data = reg_data
        self.dst = dst
        self.b = b

    def compute(self):
        if is_number(self.b):
            self.reg_data[self.dst] += int(self.b)
        else:
            self.reg_data[self.dst] += self.reg_data[self.b]


class OpMul(object):
    def __init__(self, reg_data, dst, b):
        assert dst in registers
        assert b in registers or is_number(b)
        self.reg_data = reg_data
        self.dst = dst
        self.b = b

    def compute(self):
        if is_number(self.b):
            self.reg_data[self.dst] *= int(self.b)
        else:
            self.reg_data[self.dst] *= self.reg_data[self.b]


class OpDiv(object):
    def __init__(self, reg_data, dst, b):
        assert dst in registers
        assert b in registers or is_number(b)
        self.reg_data = reg_data
        self.dst = dst
        self.b = b

    def compute(self):
        if is_number(self.b):
            self.reg_data[self.dst] /= int(self.b)
        else:
            self.reg_data[self.dst] /= self.reg_data[self.b]

        self.reg_data[self.dst] = int(self.reg_data[self.dst])


class OpMod(object):
    def __init__(self, reg_data, dst, b):
        assert dst in registers
        assert b in registers or is_number(b)
        self.reg_data = reg_data
        self.dst = dst
        self.b = b

    def compute(self):
        if is_number(self.b):
            self.reg_data[self.dst] %= int(self.b)
        else:
            self.reg_data[self.dst] %= self.reg_data[self.b]


class OpEql(object):
    def __init__(self, reg_data, dst, b):
        assert dst in registers
        assert b in registers or is_number(b)
        self.reg_data = reg_data
        self.dst = dst
        self.b = b

    def compute(self):
        if is_number(self.b):
            self.reg_data[self.dst] = int(self.reg_data[self.dst] == int(self.b))
        else:
            self.reg_data[self.dst] = int(
                self.reg_data[self.dst] == self.reg_data[self.b]
            )


class ALU(object):
    def __init__(self):
        self.input_stream = []
        self.program = []
        self.reg_data = defaultdict(int)

    def reset(self):
        self.input_stream.clear()
        self.reg_data.clear()

    def choose_op(self, op_raw):
        op_name, args = op_raw.strip().split(" ", maxsplit=1)
        if len(args.split()) == 1:
            # only input can have one argument all the others have two
            return OpInp(self.reg_data, self.input_stream, args)

        arg1, arg2 = args.split()
        if op_name == "add":
            return OpAdd(self.reg_data, arg1, arg2)
        elif op_name == "mul":
            return OpMul(self.reg_data, arg1, arg2)
        elif op_name == "div":
            return OpDiv(self.reg_data, arg1, arg2)
        elif op_name == "mod":
            return OpMod(self.reg_data, arg1, arg2)
        elif op_name == "eql":
            return OpEql(self.reg_data, arg1, arg2)

        assert False, "Operator not recognized: {}".format(op_raw)

    # returns prefix which includes split point from the beginning
    # and suffix which includes everything else
    def split_program(self, split_at):
        digit_no = 0
        head, tail = [], []
        cur_part = head

        for op in self.program:
            if isinstance(op, OpInp):
                digit_no += 1
            if digit_no >= split_at + 1:
                cur_part = tail
            cur_part.append(op)

        head_alu = ALU()
        head_alu.set_program(head)

        tail_alu = ALU()
        tail_alu.set_program(tail)

        return head_alu, tail_alu

    def parse_program(self, lines):
        for line in lines:
            op = self.choose_op(line)
            self.program.append(op)

    def set_program(self, program):
        for op in program:
            op_new = deepcopy(op)
            op_new.reg_data = self.reg_data
            op_new.inp_stream = self.input_stream
            self.program.append(op_new)

    def run_program(self):
        for op in self.program:
            op.compute()

    def set_input_stream(self, *input_stream):
        self.input_stream.extend(input_stream)
