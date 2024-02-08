#!/usr/bin/env python3
import sys

enum_counter=0
def enum(start=False):
  global enum_counter
  if start:
    enum_counter = 0
  res = enum_counter
  enum_counter += 1
  return res

OP_PUSH=enum(True)
OP_ADD=enum()
OP_SUB=enum()
OP_DUMP=enum()
OP_EMIT=enum()
OP_EXIT=enum()

def push(x):
  return (OP_PUSH, x)

def add():
  return (OP_ADD, )

def sub():
  return (OP_SUB, )

def dump():
  return (OP_DUMP, )

# Prints the top value of the stack
def emit():
  return (OP_EMIT, )

def sys_exit():
  return (OP_EXIT, )

###### COMPILER ######
def read_file(input_file):
  with open(input_file) as f:
    lines = f.readlines()

  return lines

# Builds list of op calls in the form of a stack
def parse(lines):
  program = [] # for whole program
  for l in lines:
    data = l.split()
    tokens = [] # for handle of each line
    for i in range(len(data)):
      # handle basic expression
      if data[i].isnumeric():
        tokens.append(push(int(data[i])))
      elif data[i] == 'ADD':
        tokens.append(add())
      elif data[i] == 'SUB':
        tokens.append(sub())
      elif data[i] == 'DUMP':
        tokens.append(dump())
      elif data[i] == 'QUIT':
        tokens.append(sys_exit())
      else:
        print("error: parser")
        exit(1)

    for t in tokens:
      program.append(t)

  print(program)
  return program
        

################

def sim(program):
  stack = []
  for op in program:
    if op[0] == OP_PUSH:
      stack.append(op[1])
    elif op[0] == OP_ADD:
      a = stack.pop()
      b = stack.pop()
      stack.append(a+b)
    elif op[0] == OP_SUB:
      a = stack.pop()
      b = stack.pop()
      stack.append(b-a)
    elif op[0] == OP_EMIT:
      a = stack[len(stack)-1]
      print(a)
    elif op[0] == OP_DUMP:
      a = stack.pop()
      print(a)
    elif op[0] == OP_EXIT:
      exit(0)
    else:
      print("error: invalid operation")
      exit(1)

def com(program, output_file):
  with open(output_file, 'w') as out:
    # TODO refactor to a "Standard Library"
    
    out.write("section .data\n")
    out.write("  newline: db 10\n")
    out.write("  negative: db 45\n")
    out.write("  zero: db 48\n")

    out.write("section .text\n")
    out.write("strlen:\n")
    out.write("  mov rdx, 0\n") 
    out.write("  call strloop\n") 
    
    out.write("stradd:\n")
    out.write("  add rdx, 1\n")
    out.write("  add rdi, 1\n")

    out.write("strloop:\n")
    out.write("  cmp byte [rdi], 0\n") 
    out.write("  jne stradd\n") 
    out.write("  mov rax, rdx\n") 
    out.write("  ret\n") 
    
    out.write("print_newline:\n")
    out.write("  mov rsi, newline\n") 
    out.write("  mov rdx, 1\n") 
    out.write("  mov rax, 1\n") 
    out.write("  mov rdi, 1\n") 
    out.write("  syscall\n") 
    out.write("  ret\n") 

    out.write("printint:            ; operates on value placed in edi \n") # TODO need a way to differentiate datatypes
    out.write("  push rbp            ; save base pointer \n") 
    out.write("  mov rbp, rsp        ; place bp on stack \n") 
    out.write("  sub rsp, 20         ; align stack, keep 20 bytes for buffering \n") 
    out.write("  cmp edi, 0          ; compare to 0 \n") 
    out.write("  je _print_zero      ; handle 0\n") 
    out.write("  cmp edi, 0          ; compare to 0 \n") 
    out.write("  jg _printint_pos; handle positive\n") 

    out.write("  ; handle negative\n") 
    out.write("  call _print_negative    ; print neg\n") 
    
    out.write("  xor edi, 1          ; convert to negative FIXME\n") 
    out.write("  add edi, 1          ; convert to negative FIXME\n") 

    out.write("_printint_pos:\n")
    out.write("  mov rbx, rsp\n")
    out.write("  add rbx, 17\n")
    out.write("  mov qword [rsp+8], 0\n")
    out.write("  mov word [rsp+16], 0\n")

    out.write("_printint_loop:\n")
    out.write("  cmp edi, 0\n")
    out.write("  je _printint_done\n")
    out.write("  xor edx, edx\n")
    out.write("  mov eax, edi\n")
    out.write("  mov ecx, 10\n")
    out.write("  div ecx\n")
    out.write("  mov edi, eax\n")
    out.write("  add dl, 48          ; convert remainder to ascii\n")
    out.write("  mov byte [rbx], dl\n")
    out.write("  dec rbx\n")
    out.write("  jmp _printint_loop\n")

    out.write("_printint_done:\n")
    out.write("  mov rdi, rbx\n")
    out.write("  call strlen\n")
    out.write("  ; print the buffer\n")
    out.write("  mov rdx, rax         ; len of buffer \n")
    out.write("  mov rsi, rbx         ; value to print \n")
    out.write("  mov rax, 1\n")
    out.write("  mov rdi, 1\n")
    out.write("  syscall\n")

    out.write("  mov rsp, rbp        ; restore stack and bp\n")
    out.write("  pop rbp\n")
    out.write("  ret\n")

    out.write("_print_zero:\n")
    out.write("  mov rsi, zero\n") 
    out.write("  mov rdx, 1\n") 
    out.write("  mov rax, 1\n") 
    out.write("  mov rdi, 1\n") 
    out.write("  syscall\n") 
    out.write("  ret\n") 

    out.write("_print_negative:\n")
    out.write("  mov rsi, negative\n") 
    out.write("  mov rdx, 1\n") 
    out.write("  mov rax, 1\n") 
    out.write("  mov rdi, 1\n") 
    out.write("  syscall\n") 
    out.write("  ret\n") 

    out.write("dump:\n")
    out.write("  mov r9, -3689348814741910323\n") 
    out.write("  sub rsp, 40\n") 
    out.write("  mov BYTE [rsp+31], 10\n") 
    out.write("  lea rcx, [rsp+30]\n") 
    out.write(".L2:\n")
    out.write("    mov     rax, rdi\n")
    out.write("    lea     r8, [rsp+32]\n")
    out.write("    mul     r9\n")
    out.write("    mov     rax, rdi\n")
    out.write("    sub     r8, rcx\n")
    out.write("    shr     rdx, 3\n")
    out.write("    lea     rsi, [rdx+rdx*4]\n")
    out.write("    add     rsi, rsi\n")
    out.write("    sub     rax, rsi\n")
    out.write("    add     eax, 48\n")
    out.write("    mov     BYTE [rcx], al\n")
    out.write("    mov     rax, rdi\n")
    out.write("    mov     rdi, rdx\n")
    out.write("    mov     rdx, rcx\n")
    out.write("    sub     rcx, 1\n")
    out.write("    cmp     rax, 9\n")
    out.write("    ja      .L2\n")
    out.write("    lea     rax, [rsp+32]\n")
    out.write("    mov     edi, 1\n")
    out.write("    sub     rdx, rax\n")
    out.write("    xor     eax, eax\n")
    out.write("    lea     rsi, [rsp+32+rdx]\n")
    out.write("    mov     rdx, r8\n")
    out.write("    mov     rax, 1\n")
    out.write("    syscall\n")
    out.write("    add     rsp, 40\n")
    out.write("    ret\n")

    out.write("emit:\n")
    out.write("  pop rax\n") 
    out.write("  mov edi, eax\n") 
    out.write("  call printint\n") 
    out.write("  call print_newline\n") 
    out.write("  ret\n") 

    out.write("_exit:\n")
    out.write("  mov rax, 60\n") 
    out.write("  mov rdi, 0\n") 
    out.write("  syscall\n") 
    out.write("  ret\n") 
    out.write("global _start\n")
    out.write("_start:\n")

    for op in program:
      if op[0] == OP_PUSH:
        out.write("  push %d\n" % op[1])
      elif op[0] == OP_ADD:
        out.write("  pop rax\n")
        out.write("  pop rbx\n")
        out.write("  add rax, rbx\n")
        out.write("  push rax\n")
      elif op[0] == OP_SUB:
        out.write("  pop rax\n")
        out.write("  pop rbx\n")
        out.write("  sub rbx, rax\n")
        out.write("  push rbx\n")
      elif op[0] == OP_DUMP:
        out.write("  pop rdi\n")
        out.write("  call dump\n")
      elif op[0] == OP_EMIT:
        out.write("  call emit\n")
      elif op[0] == OP_EXIT:
        out.write("  call _exit\n")
      else:
        print("error: invalid operation")
        exit(1)

    out.write("  mov rax, 60\n") # default call to exit 
    out.write("  mov rdi, 0\n")  
    out.write("  syscall\n")  
    out.write("  ret\n")  

def usage():
  print("usage: pp <input file>")

if __name__ == '__main__':
  output_file = "out.asm"

  #sim(program)

  if len(sys.argv) < 2:
    usage()
    exit(1)

  input_file = sys.argv[1]

  # Parser Entry Point
  lines = read_file(input_file)

  program = parse(lines)

  com(program, output_file)
