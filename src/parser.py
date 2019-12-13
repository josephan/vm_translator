class Parser:
    def __init__(self, path_to_vm_file):
        self.vm_code = self.__sanitized_vm_file(path_to_vm_file)
        self.line_number = 0
        self.filename = self.__sanitized_filename(path_to_vm_file)
        self.__reset()

    def has_more_commands(self):
        return len(self.vm_code) > 0

    def advance(self):
        self.line_number = self.line_number + 1
        self.__reset()
        code = self.vm_code.pop(0)
        self.current_command = code
        self.__set_command_attrs(code)

    def __reset(self):
        self.current_command = None
        self.command_type = None
        self.arg1 = None
        self.arg2 = None

    def __sanitized_vm_file(self, path_to_vm_file):
        sanitized_lines = []
        for line in self.__open_file(path_to_vm_file):
            sanitized_line = self.__remove_whitespace_and_comments(line)
            if sanitized_line:
                sanitized_lines.append(sanitized_line)
        return sanitized_lines

    def __sanitized_filename(self, path_to_vm_file):
        return path_to_vm_file.split("/")[-1].replace('.vm', '')
    
    def __open_file(self, path_to_vm_file):
        f = open(path_to_vm_file, 'r')
        vm_code = f.readlines()
        f.close()
        return vm_code

    def __remove_whitespace_and_comments(self, line):
        return line.strip().split("//")[0]

    def __set_command_attrs(self, code):
        if code in ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]:
            self.command_type = "C_ARITHMETIC"
            self.arg1 = code
        elif code.startswith("push"):
            self.command_type = "C_PUSH"
            args = code.split(" ")
            self.arg1 = args[1]
            self.arg2 = int(args[2])
        elif code.startswith("pop"):
            self.command_type = "C_POP"
            args = code.split(" ")
            self.arg1 = args[1]
            self.arg2 = int(args[2])
        else:
            raise "%s is not a supported command yet..." % code
