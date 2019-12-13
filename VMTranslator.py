import sys
from src.parser import Parser
from src.code_writer import CodeWriter

def main():
    vm_file = sys.argv[1]
    output_file_path = vm_file_to_output_file_path(vm_file)
    parser = Parser(vm_file)
    code_writer = CodeWriter(output_file_path)
    while parser.has_more_commands():
        parser.advance()
        code_writer.write(parser)
    code_writer.close()

def vm_file_to_output_file_path(vm_file):
    return vm_file.replace(".vm", ".asm")

main()
