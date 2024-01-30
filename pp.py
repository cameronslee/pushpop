#!/usr/bin/env python3

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

def push(x):
  return (OP_PUSH, x)

def add():
  return (OP_ADD, )

def sub():
  return (OP_SUB, )

def dump():
  return (OP_DUMP, )

program=[
  push(2),
  push(2),
  add(),
  dump(),
]

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
    elif op[0] == OP_DUMP:
      a = stack.pop()
      print(a)
    else:
      print("error: invalid operaion")
      exit(1)

output_file = "out.asm"
def com(program):
  pass

def usage():
  print("usage: pp")

if __name__ == '__main__':
  sim(program)
  com(program)
