import sys
import os
from src.parser import Parser
from src.code_writer import CodeWriter

def main():
    vm_file_or_dir = sys.argv[1]
    output_file_path = vm_file_or_directory_to_output_file_path(vm_file_or_dir)

    if os.path.exists(output_file_path):
        os.remove(output_file_path)

    if os.path.isdir(vm_file_or_dir):
        write_bootstrap_code(output_file_path)
        for vm_file in [f for f in os.listdir(vm_file_or_dir) if f.endswith('.vm')]:
            path_to_vm_file = os.path.join(vm_file_or_dir, vm_file)
            parse_vm_file_and_append_to_asm_file(path_to_vm_file, output_file_path)
    elif os.path.isfile(vm_file_or_dir):
        parse_vm_file_and_append_to_asm_file(vm_file_or_dir, output_file_path)


def vm_file_or_directory_to_output_file_path(path):
    if os.path.isdir(path):
        return os.path.join(path, os.path.basename(path) + '.asm')
    elif os.path.isfile(path):
        return path.replace(".vm", ".asm")

def parse_vm_file_and_append_to_asm_file(vm_file, output_file_path):
    parser = Parser(vm_file)
    code_writer = CodeWriter(output_file_path)
    while parser.has_more_commands():
        parser.advance()
        code_writer.write(parser)
    code_writer.close()

def write_bootstrap_code(output_file_path):
    code_writer = CodeWriter(output_file_path)
    code_writer.write_bootstrap_code()
    code_writer.close()

main()

def __sanitize_vm_file_or_directory(self, path):
    if os.path.isdir(path):
        return self.__sanitized_vm_directory(path)
    elif os.path.isfile(path):
        return self.__sanitized_vm_file(path)
    else:
        raise Exception("Specified path is a special file (socket, FIFO, device file)")

def __sanitized_vm_directory(self, path_to_vm_directory):
    sanitized_lines = ['SP=256','call Sys.init 0']
    for vm_file in [f for f in os.listdir(path_to_vm_directory) if f.endswith('.vm')]:
        sanitized_lines += self.__sanitized_vm_file(os.path.join(path_to_vm_directory, vm_file))
    return sanitized_lines


def __sanitized_filename_or_directory(self, path):
    if os.path.isdir(path):
        head, tail = os.path.split(path)
        return tail or os.path.basename(head)
    elif os.path.isfile(path):
        return os.path.basename(path).replace('.vm', '')
    else:
        raise Exception("Specified path is a special file (socket, FIFO, device file)")

