import textwrap

class CodeWriter:
    def __init__(self, output_file_path):
        self.output_file = open(output_file_path, "w+")

    def write(self, parser):
        asm_code = self.__vm_code_to_asm_code(parser)
        formatted_asm_code = textwrap.dedent(asm_code)
        self.output_file.write(formatted_asm_code)

    def __vm_code_to_asm_code(self, parser):
        if parser.command_type == "C_ARITHMETIC":
            return self.__arithmetic_code(parser)
        elif parser.command_type == "C_PUSH":
            return self.__push_code(parser)
        elif parser.command_type == "C_POP":
            return self.__pop_code(parser)

    def __arithmetic_code(self, parser):
        if parser.current_command == "add":
            return self.__add_command()
        elif parser.current_command == "sub":
            return self.__sub_command()
        elif parser.current_command == "neg":
            return self.__neg_command()
        elif parser.current_command == "eq":
            return self.__eq_command(parser)
        elif parser.current_command == "gt":
            return self.__gt_command(parser)
        elif parser.current_command == "lt":
            return self.__lt_command(parser)
        elif parser.current_command == "and":
            return self.__and_command()
        elif parser.current_command == "or":
            return self.__or_command()
        elif parser.current_command == "not":
            return self.__not_command()

    def __add_command(self):
        return """
               // add
               @SP
               M=M-1
               A=M
               D=M
               A=A-1
               D=D+M
               M=D
               """

    def __sub_command(self):
        return """
               // sub
               @SP
               M=M-1
               A=M
               D=M
               A=A-1
               D=M-D
               M=D
               """

    def __neg_command(self):
        return """
               // neg
               @SP
               A=M-1
               M=-M
               """

    def __eq_command(self, parser):
        return """
               // eq
               @SP
               M=M-1
               A=M
               D=M
               A=A-1
               D=M-D
               @EQ_{line_number}
               D;JEQ
               @SP
               A=M-1
               M=0
               @END_{line_number}
               0;JMP
               (EQ_{line_number})
               @SP
               A=M-1
               M=-1
               (END_{line_number})
               """.format(line_number=parser.line_number)

    def __gt_command(self, parser):
        return """
               // gt
               @SP
               M=M-1
               A=M
               D=M
               A=A-1
               D=M-D
               @GT_{line_number}
               D;JGT
               @SP
               A=M-1
               M=0
               @END_{line_number}
               0;JMP
               (GT_{line_number})
               @SP
               A=M-1
               M=-1
               (END_{line_number})
               """.format(line_number=parser.line_number)

    def __lt_command(self, parser):
        return """
               // lt
               @SP
               M=M-1
               A=M
               D=M
               A=A-1
               D=M-D
               @LT_{line_number}
               D;JLT
               @SP
               A=M-1
               M=0
               @END_{line_number}
               0;JMP
               (LT_{line_number})
               @SP
               A=M-1
               M=-1
               (END_{line_number})
               """.format(line_number=parser.line_number)

    def __and_command(self):
        return """
               // and
               @SP
               M=M-1
               A=M
               D=M
               A=A-1
               M=D&M
               """

    def __or_command(self):
        return """
               // or
               @SP
               M=M-1
               A=M
               D=M
               A=A-1
               M=D|M
               """

    def __not_command(self):
        return """
               // not
               @SP
               A=M-1
               M=!M
               """

    def __push_code(self, parser):
        if parser.arg1 == "constant":
            return """
                   // push constant {index}
                   @{index}
                   D=A
                   @SP
                   A=M
                   M=D
                   @SP
                   M=M+1
                   """.format(index=parser.arg2)
        elif parser.arg1 == "local":
            return """
                   // push local {index}
                   @LCL
                   D=M
                   @{index}
                   D=D+A
                   A=D
                   D=M
                   @SP
                   A=M
                   M=D
                   @SP
                   M=M+1
                   """.format(index=parser.arg2)
        elif parser.arg1 == "argument":
            return """
                   // push argument {index}
                   @ARG
                   D=M
                   @{index}
                   D=D+A
                   A=D
                   D=M
                   @SP
                   A=M
                   M=D
                   @SP
                   M=M+1
                   """.format(index=parser.arg2)
        elif parser.arg1 == "this":
            return """
                   // push this {index}
                   @THIS
                   D=M
                   @{index}
                   D=D+A
                   A=D
                   D=M
                   @SP
                   A=M
                   M=D
                   @SP
                   M=M+1
                   """.format(index=parser.arg2)
        elif parser.arg1 == "that":
            return """
                   // push that {index}
                   @THAT
                   D=M
                   @{index}
                   D=D+A
                   A=D
                   D=M
                   @SP
                   A=M
                   M=D
                   @SP
                   M=M+1
                   """.format(index=parser.arg2)
        elif parser.arg1 == "pointer":
            return """
                   // push pointer {index}
                   @3
                   D=A
                   @{index}
                   D=D+A
                   A=D
                   D=M
                   @SP
                   A=M
                   M=D
                   @SP
                   M=M+1
                   """.format(index=parser.arg2)
        elif parser.arg1 == "temp":
            return """
                   // push temp {index}
                   @5
                   D=A
                   @{index}
                   D=D+A
                   A=D
                   D=M
                   @SP
                   A=M
                   M=D
                   @SP
                   M=M+1
                   """.format(index=parser.arg2)
        elif parser.arg1 == "static":
            return """
                   // push static {index}
                   @{filename}.{index}
                   D=M
                   @SP
                   A=M
                   M=D
                   @SP
                   M=M+1
                   """.format(index=parser.arg2, filename=parser.filename)

    def __pop_code(self, parser):
        if parser.arg1 == "local":
            return """
                   // pop local {index}
                   @LCL
                   D=M
                   @{index}
                   D=D+A
                   @addr_{line_number}
                   M=D
                   @SP
                   M=M-1
                   A=M
                   D=M
                   @addr_{line_number}
                   A=M
                   M=D
                   """.format(index=parser.arg2, line_number=parser.line_number)
        elif parser.arg1 == "argument":
            return """
                   // pop argument {index}
                   @ARG
                   D=M
                   @{index}
                   D=D+A
                   @addr_{line_number}
                   M=D
                   @SP
                   M=M-1
                   A=M
                   D=M
                   @addr_{line_number}
                   A=M
                   M=D
                   """.format(index=parser.arg2, line_number=parser.line_number)
        elif parser.arg1 == "this":
            return """
                   // pop this {index}
                   @THIS
                   D=M
                   @{index}
                   D=D+A
                   @addr_{line_number}
                   M=D
                   @SP
                   M=M-1
                   A=M
                   D=M
                   @addr_{line_number}
                   A=M
                   M=D
                   """.format(index=parser.arg2, line_number=parser.line_number)
        elif parser.arg1 == "that":
            return """
                   // pop that {index}
                   @THAT
                   D=M
                   @{index}
                   D=D+A
                   @addr_{line_number}
                   M=D
                   @SP
                   M=M-1
                   A=M
                   D=M
                   @addr_{line_number}
                   A=M
                   M=D
                   """.format(index=parser.arg2, line_number=parser.line_number)
        elif parser.arg1 == "pointer":
            return """
                   // pop pointer {index}
                   @3
                   D=A
                   @{index}
                   D=D+A
                   @addr_{line_number}
                   M=D
                   @SP
                   M=M-1
                   A=M
                   D=M
                   @addr_{line_number}
                   A=M
                   M=D
                   """.format(index=parser.arg2, line_number=parser.line_number)
        elif parser.arg1 == "temp":
            return """
                   // pop temp {index}
                   @5
                   D=A
                   @{index}
                   D=D+A
                   @addr_{line_number}
                   M=D
                   @SP
                   M=M-1
                   A=M
                   D=M
                   @addr_{line_number}
                   A=M
                   M=D
                   """.format(index=parser.arg2, line_number=parser.line_number)
        elif parser.arg1 == "static":
            return """
                   // pop static {index}
                   @SP
                   M=M-1
                   A=M
                   D=M
                   @{filename}.{index}
                   M=D
                   """.format(index=parser.arg2, filename=parser.filename)






    def close(self):
        self.output_file.close()
