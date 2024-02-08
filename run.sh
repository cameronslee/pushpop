#!/bin/bash

python3 pp.py

set -xe

nasm -felf64 out.asm
ld -o out out.o



