# VM Translator
![](https://github.com/josephan/vm_translator/workflows/Python%20package/badge.svg)

A Jack VM code to HACK assembly translator (from NAND2Tetris) written in python3.

## Usage

```bash
$ python3 VMTranslator.py BasicTest.vm
# => creates BasicTest.asm file
```

## VM Language Translations:

* arithmetic/logic commands:
  * `add`
  * `sub`
  * `neg`
  * `eq`
  * `gt`
  * `lt`
  * `and`
  * `or`
  * `not`
* memory segment commands:
  * `push/pop <segment> i` for:
    * `local`
    * `argument`
    * `this`
    * `that`
    * `constant`
    * `static`
    * `pointer`
    * `temp`
* branching commands:
  * `goto <label>`
  * `if-goto <label>`
  * `label <label>`
* function commands:
  * `call <functionName> <nVars>`
  * `function <functionName> <nArgs>`
  * `return`


## Example

Turns:

```
// Pushes and adds two constants.
push constant 7
push constant 8
add
```

Into:

```
// push constant 7
@7
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 8
@8
D=A
@SP
A=M
M=D
@SP
M=M+1

// add
@SP
M=M-1
A=M
D=M
A=A-1
D=D+M
M=D
```
