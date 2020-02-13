import textwrap

class CodeWriter:
    def __init__(self, output_file_path):
        self.output_file = open(output_file_path, "a")

    def write(self, parser):
        asm_code = self.__vm_code_to_asm_code(parser)
        formatted_asm_code = textwrap.dedent(asm_code)
        self.output_file.write(formatted_asm_code)

    def write_bootstrap_code(self):
        self.output_file.write(textwrap.dedent(self.__bootstrap_code()))
        self.output_file.write(textwrap.dedent(self.__call_code(1, "Sys.init", 0)))

    def __vm_code_to_asm_code(self, parser):
        if parser.command_type == "C_ARITHMETIC":
            return self.__arithmetic_code(parser)
        elif parser.command_type == "C_BOOTSTRAP_SP":
            return self.__bootstrap_code()
        elif parser.command_type == "C_PUSH":
            return self.__push_code(parser)
        elif parser.command_type == "C_POP":
            return self.__pop_code(parser)
        elif parser.command_type == "C_LABEL":
            return self.__label_code(parser)
        elif parser.command_type == "C_GOTO":
            return self.__goto_code(parser)
        elif parser.command_type == "C_IF":
            return self.__if_code(parser)
        elif parser.command_type == "C_FUNCTION":
            return self.__function_code(parser)
        elif parser.command_type == "C_RETURN":
            return self.__return_code(parser)
        elif parser.command_type == "C_CALL":
            return self.__call_code(parser.line_number, parser.arg1, parser.arg2)

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

    def __label_code(self, parser):
        return """
               // label {label}
               ({label})
               """.format(label=parser.arg1)

    def __goto_code(self, parser):
        return """
               // goto {label}
               @{label}
               0;JMP
               """.format(label=parser.arg1)

    def __if_code(self, parser):
        return """
               // if-goto {label}
               @SP
               M=M-1
               A=M
               D=M
               @{label}
               D;JNE
               """.format(label=parser.arg1)

    def __function_code(self, parser):
        push_0 = """
                 @SP
                 A=M
                 M=0
                 @SP
                 M=M+1 // push 0
                 """ * parser.arg2
        return """
               // function {function_name} {n_vars}
               ({function_name})
               {initialize_local_vars}
               """.format(function_name=parser.arg1, n_vars=parser.arg2, initialize_local_vars=push_0)

    def __return_code(self, parser):
        return """
               // return
               @LCL
               D=M
               @frame
               M=D // FRAME = LCL
               @5
               D=D-A
               A=D
               D=M
               @return_address
               M=D // RET = *(FRAME-5)
               @SP
               M=M-1
               A=M
               D=M
               @ARG
               A=M
               M=D // *ARG = pop()
               @ARG
               D=M+1
               @SP
               M=D // SP = ARG+1
               @frame
               D=M-1
               A=D
               D=M
               @THAT
               M=D // THAT = *(FRAME-1)
               @2
               D=A
               @frame
               D=M-D
               A=D
               D=M
               @THIS
               M=D // THIS = *(FRAME-2)
               @3
               D=A
               @frame
               D=M-D
               A=D
               D=M
               @ARG
               M=D // ARG = *(FRAME-3)
               @4
               D=A
               @frame
               D=M-D
               A=D
               D=M
               @LCL
               M=D // LCL = *(FRAME-4)
               @return_address
               A=M
               0;JMP // goto RET
               """
        pass

    def __call_code(self, line_number, function_name, n_args):
        return """
               // call {function_name} {n_args}
               // push return-address
               @{function_name}$ret.{line_number}
               D=A
               @SP
               A=M
               M=D
               @SP
               M=M+1
               // push LCL
               @LCL
               D=M
               @SP
               A=M
               M=D
               @SP
               M=M+1
               // push ARG
               @ARG
               D=M
               @SP
               A=M
               M=D
               @SP
               M=M+1
               // push THIS
               @THIS
               D=M
               @SP
               A=M
               M=D
               @SP
               M=M+1
               // push THAT
               @THAT
               D=M
               @SP
               A=M
               M=D
               @SP
               M=M+1
               // ARG = SP-n-5
               @SP
               D=M
               @{n_args}
               D=D-A
               @5
               D=D-A
               @ARG
               M=D
               // LCL = SP
               @SP
               D=M
               @LCL
               M=D
               // goto f
               @{function_name}
               0;JMP
               // (return-address)
               ({function_name}$ret.{line_number})
               """.format(line_number=line_number, function_name=function_name, n_args=n_args)

    def __bootstrap_code(self):
        return """
               // bootstrap code
               @256
               D=A
               @SP
               M=D
               """

    def close(self):
        self.output_file.close()
