section .data
  newline: db 10             ; \n
  negative: db 45            ; -
  zero: db 48                ; 0

section .text
strlen:
  mov rdx, 0
  call strloop

stradd:
  add rdx, 1 
  add rdi, 1 

strloop:
  cmp byte [rdi], 0
  jne stradd

  mov rax, rdx
  ret

print_newline:
  mov rsi, newline
  mov rdx, 1
  mov rax, 1
  mov rdi, 1
  syscall
  ret


printint:                     ; num in edi
  push rbp                    ; save base pointer
  mov rbp, rsp                ; place base pointer on stack
  sub rsp, 20                 ; align stack to keep 20 bytes for buffering
  cmp edi, 0                  ; compare num to 0
  je _printint_zero           ; 0 is special case
  cmp edi, 0
  jg _printint_pos            ; don't print negative sign if positive

  call _print_negative        ; print a negative sign 

  xor edi, 1                  ; convert into positive integer FIXME
  add edi, 1

_printint_pos:
  mov rbx, rsp                ; set rbx to point to the end of the buffer
  add rbx, 17
  mov qword [rsp+8], 0        ; clear the buffer
  mov word [rsp+16], 0        ; 10 bytes from [8,18)

_printint_loop:
  cmp edi, 0                  ; compare edi to 0
  je _printint_done           ; if edi == 0 then we are done
  xor edx, edx                ; prepare eax and edx for division
  mov eax, edi
  mov ecx, 10
  div ecx                     ; divide and remainder by 10
  mov edi, eax                ; move quotient back to edi
  add dl, 48                  ; convert remainder to ascii
  mov byte [rbx], dl          ; move remainder to buffer
  dec rbx                     ; shift 1 position to the left in buffer
  jmp _printint_loop

_printint_done:
  mov rdi, rbx
  call strlen

  ; print the buffer 
  mov rdx, rax                ; len of buffer from strlen
  mov rsi, rbx
  mov rax, 1
  mov rdi, 1
  syscall

  mov rsp, rbp                ; restore stack and base pointers
  pop rbp
  ret

_printint_zero:
  mov rsi, zero
  mov rdx, 1
  mov rax, 1
  mov rdi, 1
  syscall
  ret

_print_negative:
  mov rsi, negative 
  mov rdx, 1
  mov rax, 1
  mov rdi, 1
  syscall
  ret

global _start
_start:
  mov edi, 69
  call printint
  call print_newline

  mov edi, 420
  call printint
  call print_newline

