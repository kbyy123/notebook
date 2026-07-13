# Chap 8: Exceptional Control Flow

CPU 执行的指令地址序列称为 **control flow**．正常控制流主要由两类机制形成：

+ 顺序执行下一条指令．
+ 通过 `call`、`ret`、`jmp`、条件跳转等指令改变下一条指令地址．

但程序并不总是只沿着这些显式指令转移执行．当内部异常、外部中断、进程上下文切换、信号等事件打断原来的执行序列时，就形成了 **Exceptional Control Flow, ECF**．

ECF 可以分布在不同层次：

+ **硬件层**：异常和中断．
+ **操作系统层**：进程调度与上下文切换．
+ **应用层**：信号、非本地跳转．

本章的主线是：操作系统如何借助硬件异常机制，在进程之间切换控制流，并向用户进程暴露 `fork`、`execve`、`waitpid`、`signal` 等接口．

## Processes

### Program vs Process

**Program** 是代码和数据的静态集合，通常对应一个可执行文件．

**Process** 是程序的一次运行过程，是操作系统对正在执行的程序的抽象．同一个程序可以被加载运行多次，对应多个不同进程．

进程提供两个重要假象：

+ **独立的逻辑控制流**：每个进程看起来像独占 CPU．
+ **私有的虚拟地址空间**：每个进程看起来像独占内存．

这些假象让程序员可以按顺序程序的方式编写代码，而把真正的 CPU 分时复用、地址空间隔离、资源回收交给操作系统处理．

### Logical Control Flow

对于给定输入，一个进程执行过的指令地址序列称为它的 **logical control flow**．

在单处理器系统中，多个进程的逻辑控制流会在时间上交错执行．这种交错称为 **concurrency**（并发）．如果多个控制流在同一时刻真正运行在不同处理器核上，则称为 **parallelism**（并行）．

逻辑控制流被打断后，只要操作系统保存并恢复好现场，进程仍然可以回到原来的断点继续执行．

### Context Switch

进程的 **context** 是恢复该进程运行所需的全部状态，主要包括：

+ **User-level context**：代码、数据、堆、用户栈、共享库等用户地址空间内容．
+ **System-level context**：进程描述符、页表、内核栈、打开文件表等内核维护的信息．
+ **Register context**：通用寄存器、程序计数器、栈指针、状态寄存器等硬件现场．

**Context switch** 指操作系统保存当前进程的上下文，恢复另一个进程的上下文，让 CPU 改为运行另一个进程．

需要区分两件事：

+ 异常或中断处理时，CPU 进入内核态，执行的是当前进程的一段 **kernel control path**．此时不一定切换到另一个进程．
+ 上下文切换后，CPU 执行的是另一个用户进程．这才是真正从一个进程切换到另一个进程．

## Exceptions

### Basic Mechanism

从处理器视角看，**exception** 是控制流中的突变．当处理器检测到某个事件后，会通过异常表跳转到操作系统内核中的处理程序．

基本流程：

1. CPU 检测到事件，并确定对应的异常号或中断向量号．
2. CPU 根据异常表或 IDT 找到对应 handler 的入口地址．
3. CPU 保存断点和处理器状态，必要时从用户态切换到内核态并切换到内核栈．
4. 内核 handler 处理事件．
5. handler 根据事件类型选择返回当前指令、返回下一条指令，或者终止当前进程．

### Exception Classes

异常类别的核心区别在于：事件是否由当前指令引起，以及 handler 结束后返回到哪里．

| 类别 | 来源 | 同步性 | 典型例子 | 返回行为 |
| --- | --- | --- | --- | --- |
| 中断 Interrupt | 外部 I/O 设备事件 | 异步 | 定时器、网络包到达、键盘输入、DMA 完成 | 返回下一条指令 |
| 陷阱 Trap | 当前指令有意触发 | 同步 | 系统调用、断点、单步调试 | 返回下一条指令 |
| 故障 Fault | 当前指令导致错误 | 同步 | 缺页、保护违例、除零、非法指令 | 可恢复则返回当前指令重新执行，否则终止进程 |
| 终止 Abort | 严重硬件错误 | 同步 | 机器检查、内存硬件故障 | 不返回，通常终止进程或重启系统 |

异步和同步的区别是异常产生的原因来自 CPU 外部还是内部．

+ **Interrupt** 和当前正在执行的指令无关，处理完后继续执行下一条指令．
+ **Trap** 是程序主动“陷入”内核，常用于系统调用和调试，处理完后也继续执行下一条指令．
+ **Fault** 是当前指令执行不下去了，内核若能补救，就回到同一条指令重新执行．
+ **Abort** 表示系统已经无法可靠恢复，断点通常没有意义．

### Interrupts

Interrupt 由 CPU 外部事件触发，因此是异步的．典型事件包括定时器中断、键盘输入、网络数据到达、打印机缺纸、DMA 传输完成等．

每执行完一条指令，CPU 会检查是否存在外部中断请求．如果需要响应中断，CPU 会保存下一条指令地址和当前状态，转入对应的中断服务程序．服务程序完成后，控制流回到原程序的下一条指令．

### Traps

Trap 是程序主动执行某条特殊指令触发的异常，也叫自陷．它像普通函数调用一样，为用户程序提供进入内核的受控入口．

最典型的 trap 是 **system call**．例如用户程序调用 `open`、`read`、`fork`、`execve` 时，库函数会把系统调用号和参数放到约定寄存器中，然后执行 `syscall`、`sysenter` 或旧式 `int $0x80` 指令，陷入内核执行系统调用服务例程．

Trap 的返回点是 trap 指令的下一条指令．

调试器中的断点和单步也依赖 trap：

+ 断点通常通过插入特殊 trap 指令实现．
+ 单步跟踪可以让每条指令执行后都触发调试异常．

### Faults

Fault 是当前指令执行过程中产生的异常．它的断点是发生 fault 的那条指令．

Fault 的关键是是否可恢复：

+ **可恢复 fault**：内核补救后，返回发生 fault 的指令重新执行．典型例子是缺页．
+ **不可恢复 fault**：内核无法补救，通常向进程发送信号并终止进程．典型例子是访问越权、非法指令、除零等．

Page fault 是最重要的 fault 例子．如果访问的虚拟页合法但当前不在主存，内核可以把页面从磁盘调入内存，然后让引起缺页的指令重新执行．如果地址非法或权限不匹配，内核通常向进程发送 `SIGSEGV`，默认行为是终止进程并显示 `Segmentation fault`．

需要注意：C 语言数组越界本身不一定立刻触发 fault．如果越界地址仍然落在进程可访问页面内，硬件不会知道这是数组越界，只会按普通内存访问执行．

### Aborts

Abort 表示严重且通常不可恢复的错误，例如机器检查、内存硬件错误等．这类事件发生后，handler 不会把控制流交还给应用程序，系统通常会终止当前进程，严重时需要重启操作系统．

Abort 的特点是：它不一定能精确对应到某条可恢复指令，因此“返回到哪里”通常没有意义．

## Process Control

### Process States

从程序员视角看，进程通常处于三种状态之一：

+ **Running**：正在 CPU 上运行，或等待被调度运行．
+ **Stopped**：执行被挂起，不会被调度，直到收到 `SIGCONT` 等信号．
+ **Terminated**：进程已经终止，但可能还没被父进程回收．

进程终止的常见原因：

+ 从 `main` 返回．
+ 调用 `exit`．
+ 收到默认行为为终止进程的信号．

### fork
见 [fork](Chap10.md#fork)

### Reaping Children

子进程终止后不会立刻从系统中完全消失．内核会保留它的退出状态，直到父进程回收它．

+ **Zombie process**：已经终止但尚未被父进程回收的子进程．
+ **Orphan process**：父进程先终止，子进程被 `init` 或系统服务进程接管．

父进程使用 `waitpid` 回收子进程：

```C
#include <sys/types.h>
#include <sys/wait.h>

pid_t waitpid(pid_t pid, int *wstatus, int options);
```

常见用法：

+ `waitpid(-1, &status, 0)`：等待任意一个子进程终止．
+ `waitpid(pid, &status, 0)`：等待指定 PID 的子进程终止．
+ `WNOHANG`：没有子进程结束时立即返回，不阻塞．

常用状态宏：

+ `WIFEXITED(status)`：子进程是否正常终止．
+ `WEXITSTATUS(status)`：正常终止时的退出状态．
+ `WIFSIGNALED(status)`：子进程是否因为未捕获信号而终止．
+ `WTERMSIG(status)`：导致子进程终止的信号编号．
+ `WIFSTOPPED(status)`：子进程是否被信号挂起．
+ `WSTOPSIG(status)`：导致子进程挂起的信号编号．

### execve

`execve` 在当前进程上下文中加载并运行一个新程序．

```C
#include <unistd.h>

int execve(const char *filename, char *const argv[], char *const envp[]);
```

如果 `execve` 成功，它不会返回到调用点，而是直接开始执行新程序的 `main`．如果失败，返回 `-1` 并设置 `errno`．

Shell 执行命令时通常是：

1. 解析命令行，构造 `argv` 和 `envp`．
2. 调用 `fork` 创建子进程．
3. 子进程调用 `execve` 加载目标程序．
4. 父进程用 `waitpid` 回收前台子进程．

## Signals

### Signal Model

Signal 是一种更高层的 ECF 机制，用于通知进程某类事件已经发生．

信号可能来自：

+ 内核检测到的异常，例如除零产生 `SIGFPE`，非法地址访问产生 `SIGSEGV`．
+ 外部事件，例如按下 `Ctrl-C` 产生 `SIGINT`，定时器到期产生 `SIGALRM`．
+ 其他进程调用 `kill` 请求内核发送信号．

信号模型中有几个基本概念：

+ **Sending**：内核向目标进程发送信号．
+ **Pending signal**：信号已经发送但尚未被接收．
+ **Blocked signal**：进程暂时屏蔽某类信号，使其保持 pending．
+ **Receiving**：进程对某个未阻塞 pending signal 采取动作．

对于传统 Unix 信号，同一种信号在一个进程中通常最多只保留一个 pending 实例．后续同类信号可能被合并，不会排队保存每一次发生．

### Common Signals

| 信号 | 典型原因 | 默认行为 |
| --- | --- | --- |
| `SIGINT` | 键盘 `Ctrl-C` | 终止进程 |
| `SIGTSTP` | 键盘 `Ctrl-Z` | 挂起进程 |
| `SIGCONT` | 恢复被挂起进程 | 继续运行 |
| `SIGKILL` | 强制终止 | 终止进程，不能捕获或忽略 |
| `SIGSTOP` | 强制挂起 | 挂起进程，不能捕获或忽略 |
| `SIGCHLD` | 子进程终止或停止 | 默认忽略 |
| `SIGSEGV` | 非法内存访问 | 终止进程 |
| `SIGFPE` | 算术异常，如整数除零 | 终止进程 |
| `SIGALRM` | `alarm` 定时器到期 | 终止进程 |

### Sending Signals

`kill` 可以请求内核向进程或进程组发送信号：

```C
#include <sys/types.h>
#include <signal.h>

int kill(pid_t pid, int sig);
```

+ `pid > 0`：发送给指定 PID 的进程．
+ `pid == 0`：发送给调用进程所在进程组中的所有进程．
+ `pid < 0`：发送给进程组 ID 为 `|pid|` 的所有进程．

`alarm` 会在指定秒数后向调用进程发送 `SIGALRM`：

```C
#include <unistd.h>

unsigned int alarm(unsigned int seconds);
```

Shell 中也可以用 `/bin/kill` 发送信号，例如 `kill -9 pid` 发送 `SIGKILL`．

### Receiving Signals

内核通常在从内核态返回用户态前，检查当前进程是否有未阻塞的 pending signal．如果存在，内核会让进程接收其中一个信号，并执行相应动作：

+ 忽略该信号．
+ 终止进程．
+ 挂起进程．
+ 调用用户注册的 signal handler．

`signal` 可以为某个信号注册 handler：

```C
#include <signal.h>

typedef void (*sighandler_t)(int);
sighandler_t signal(int signum, sighandler_t handler);
```

`handler` 可以是：

+ `SIG_IGN`：忽略该信号．
+ `SIG_DFL`：恢复默认行为．
+ 自定义函数地址：捕获信号并执行该 handler．

`SIGKILL` 和 `SIGSTOP` 不能被捕获，也不能被忽略．

> [!warning] Signal Handler
>
> Signal handler 会异步打断主程序控制流，因此应尽量短小，并避免调用不可重入或非 async-signal-safe 的函数．复杂逻辑通常应该通过设置全局标志位，让主控制流之后再处理．

## Nonlocal Jumps

普通函数调用遵循 call-return 结构，而 **nonlocal jump** 可以直接从一个函数跳到另一个正在执行的函数位置，不按正常返回链逐层返回．

C 语言提供 `setjmp` 和 `longjmp`：

```C
#include <setjmp.h>

int setjmp(jmp_buf env);
void longjmp(jmp_buf env, int retval);
```

`setjmp` 保存当前调用环境，并第一次返回 `0`．之后如果调用 `longjmp(env, retval)`，控制流会回到对应的 `setjmp` 位置，此时 `setjmp` 返回非零值 `retval`．如果 `retval` 为 `0`，实际返回值会被改成 `1`．

基本结构：

```C
jmp_buf env;

if (setjmp(env) == 0) {
    /* normal path */
} else {
    /* path reached by longjmp */
}
```

在信号处理中，应该使用可以保存信号屏蔽状态的版本：

```C
#include <setjmp.h>

int sigsetjmp(sigjmp_buf env, int savesigs);
void siglongjmp(sigjmp_buf env, int retval);
```

一个常见用法是：主程序用 `sigsetjmp` 建立恢复点，信号处理程序在捕获 `SIGFPE`、`SIGSEGV` 等信号后调用 `siglongjmp`，让控制流跳出出错位置，回到主程序的恢复分支．

但 nonlocal jump 会跳过中间函数的正常返回过程，因此也会跳过这些函数本该执行的清理逻辑．使用时需要非常克制．

## Summary

本章的核心可以压缩成一条链：

```text
exception event
    -> exception table / IDT
    -> kernel handler
    -> return to current instruction / return to next instruction / terminate
```

最重要的分类是：

+ **Interrupt**：外部异步事件，返回下一条指令．
+ **Trap**：主动陷入内核，返回下一条指令．
+ **Fault**：当前指令出错，可恢复则重试当前指令，不可恢复则终止进程．
+ **Abort**：严重不可恢复错误，不返回．

进程、信号和非本地跳转都是建立在这套异常控制流思想上的更高层抽象．
