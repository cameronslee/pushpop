#!/bin/bash

set -xe

nasm -felf64 test.asm
ld -o test test.o



