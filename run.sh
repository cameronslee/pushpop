#!/bin/bash

python3 pp.py source.pp

set -xe

nasm -felf64 out.asm
ld -o out out.o



