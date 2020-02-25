"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
HLT = 0b00000001

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256   
        self.pc = 0
        self.dispatch_table = {
            LDI: self.LDI_op,
            PRN: self.PRN_op,
            MUL: self.MUL_op,
            HLT: self.HLT_op
        }

    def LDI_op(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b
        self.pc += 3

    def PRN_op(self, operand_a, operand_b):
        print(self.reg[operand_a])
        self.pc += 2

    def MUL_op(self, operand_a, operand_b):
        self.reg[operand_a] = self.reg[operand_a] * self.reg[operand_b]
        self.pc += 3

    def HLT_op(self, operand_a, operand_b):
        sys.exit(0)

    def ram_read(self, mar):
        mdr = self.ram[mar]
        return mdr

    def ram_write(self, mar, value):
        self.ram[mar] = value

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        with open(sys.argv[1]) as f:
            for line in f:
                comment_split = line.split("#")
                num = comment_split[0].strip()

                if num == "":
                    continue

                instruction = int(num, 2)
                self.ram[address] = instruction
                address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while True:
            op = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if int(bin(op), 2) in self.dispatch_table:
                self.dispatch_table[op](operand_a, operand_b)
            else:
                print("Unrecognized operation.")
                sys.exit(1)
