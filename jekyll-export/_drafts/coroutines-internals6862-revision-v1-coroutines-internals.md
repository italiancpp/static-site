---
id: 6951
title: coroutines-internals
date: 2016-10-27T10:26:11+02:00
author: Marco Alesiani
layout: revision
guid: http://www.italiancpp.org/2016/10/27/6862-revision-v1/
permalink: /2016/10/27/6862-revision-v1/
---
<a href="https://github.com/italiancpp/code" target="_blank"><img loading="lazy" src="http://www.italiancpp.org/wp-content/uploads/2016/10/github_available-1.png" alt="Article's code is available on Github" width="200" height="50" class="alignnone size-full wp-image-6930" /></a>

## What are coroutines and why should I care?

In _The Art of Computer Programming_ Donald Knuth introduced coroutines as an alternative to the usual function caller/callee idiom where two pieces of code were treated as cooperating equals.  
Coroutines can be thought of as language-level constructs that generalize subroutines by providing multiple exit/entry points. A normal subroutine usually has a starting point and one or more exit (return) points. A coroutine provides the ability to enter/exit its control flow at different spots therefore allowing for greater code expressiveness, preservation of automatic states across function calls and [nonpreemptive multitasking](https://en.wikipedia.org/wiki/Cooperative_multitasking).

It has to be noted that different programming languages can provide various levels of support for coroutines, e.g.

  * Languages supporting the _yield_ keyword
  * Languages providing full support for _async_, _await_, _yield_

In this article we&#8217;ll focus on the former.

Thoughtful use of coroutines can lead to cleaner and more maintainable code in a variety of situations. As a motivating example let&#8217;s take for instance the following pseudocode

<pre>function start_accepting() {

  socket.async_accept(accept_handler);

  start_accepting();

}

function accept_handler() {

  socket.async_read(read_handler);
 
}

function read_handler(data) {

  request = parse_data(data);

  switch(request) {

    case SEND_DATA: {

      data_to_send = prepare_data_for(request);

      socket.async_write(data_to_send, write_handler);

    } break;

  };

}

function write_handler() {

  ... // continue execution

}</pre>

Asynchronous programming is often the preferred way of accomplishing potentially blocking operations without stalling the thread on blocking calls. In the pseudocode above we&#8217;re assuming (and omitting for clarity&#8217;s sake) that all operations are queued and handled by an event loop manager (a common and powerful idiom in asynchronous applications programming, cfr. [boost::asio](http://www.boost.org/doc/libs/)).

Coroutines allow modeling the same behavior with more readable code

<pre>coroutine acceptor() {

  while(true) {

    socket.async_accept_connection(yield); // To event manager

    start_coroutine(serve_request);

  }

}

coroutine serve_request() {

  socket.async_read(data, yield);

  request = parse_data(data);

  switch(request) {

    case SEND_DATA: {

      data_to_send = prepare_data_for(request);

      socket.async_write(data_to_send, yield);

      ... // Continue execution

    } break;

  };

}</pre>

&nbsp;

The code in _serve_request()_ uses a sequential-looking paradigm

> Coroutines let you create a structure that mirrors the actual program logic. Asynchronous operations don’t split functions, because there are no handlers to define what should happen when an asynchronous operation completes. Instead of having handlers call each other, the program can use a sequential structure.
> 
> ([boost.asio-coroutines](http://theboostcpplibraries.com/boost.asio-coroutines))
> 
> &nbsp;

## Standard support

At the time of writing this article coroutines didn&#8217;t make it for the next standard version (C++17) although recent MSVC versions already ship with an _/await_ option to test experimental support for coroutines.

## Coroutines internals

It is important to understand the role of coroutines in providing a collaborative non-preemptive multitasking: spawning a coroutine **does not spawn a new thread** of execution but coroutines _waive_ execution by <a href="https://en.wikipedia.org/wiki/Yield_(multithreading)" target="_blank">yielding</a> to callers (_asymmetric coroutines_) or to other coroutines (_symmetric coroutines_) explicitly.

Since coroutines are concepts that have been known for a relatively long time many different techniques (both at language level and system level) have been devised (an interesting suggested reading: <a href="http://www.chiark.greenend.org.uk/~sgtatham/coroutines.html" target="_blank">Duff&#8217;s device based coroutines</a>).

Implementing basic support for asymmetric stackful coroutines can be a rewarding experience in terms of understanding the relationship between coroutines and the way these program flow constructs interact with callers and the underlying memory. Most of the code that will be presented is a pruned-down version of the coroutine implementation by Oliver Kowalke (cfr. <a href="http://www.boost.org/doc/libs/" target="_blank">boost::coroutine2</a>) available with the boost libraries.

### Abstracting away the execution context

In order to implement a coroutine context switch (in its simplest form from the callee to the caller) we need a mechanism to abstract the execution state of our routines and to save/restore stack, registers, CPU flags, etc.

A context switch between threads on x86_64 can be quite costly in terms of performances since it also involves a trip to kernel syscalls. Coroutines context switches in the same thread are far more lightweight and require no kernel interaction. The foundation bricks for userland context switches are contained in the <a href="https://github.com/boostorg/context" target="_blank">boost/context</a> library. These functionalities provide a solid abstraction that can provide ready-to-use stacks (either basic _malloc&#8217;d_ stack buffers or even <a href="https://gcc.gnu.org/wiki/SplitStacks" target="_blank">split stacks</a> on supported architectures) to store our context data or complement system-level constructs (e.g. _ucontext_ on Unix systems, _Fibers_ on Windows). It has to be noted that _boost::context_ used to support Windows fibers due to undocumented TEB-swapping related issues; after fixes were deployed support was dropped since the introduction of execution context v2.

In this article we&#8217;ll go for a _fcontext_ implementation in assembler on a x86_64 Unix system (no system calls involved).

### Saving the state

When a coroutine yields an _fcontext_ switch should occur, i.e. we should save whatever state the routine was at that point in time and _JMP_ to another context. On a recent Unix system calling conventions, object and executable file formats and other low-level ABI issues are defined by the <a href="http://wiki.osdev.org/System_V_ABI" target="_blank">System V ABI</a>. On a x86_64 architecture the stack grows downwards and parameters to functions are passed in registers _rdi, rsi, rcx, r8, r9_ + additional stack space if needed. The stack is always 16-byte aligned before a _call_ instruction is issued. Registers _rbx, rsp, rbp, r12, r13, r14,_ and _r15_ are preserved across function calls while _rax, rdi, rsi, rdx, rcx, r8, r9, r10, r11_ are scratch registers

<table>
  <tr>
    <th>
      Return value
    </th>
    
    <th>
      Parameter Registers
    </th>
    
    <th>
      Scratch Registers
    </th>
    
    <th>
      Preserved Registers
    </th>
  </tr>
  
  <tr>
    <td>
      rax, rdx
    </td>
    
    <td>
      rdi, rsi, rdx, rcx, r8, r9 + additional_stack
    </td>
    
    <td>
      rax, rdi, rsi, rdx, rcx, r8, r9, r10, r11
    </td>
    
    <td>
      rbx, rsp, rbp, r12, r13, r14, r15
    </td>
  </tr>
</table>

Therefore following in _boost::context_&#8216;s footsteps a reasonable memory layout is the following

<pre>/****************************************************************************************
 *                                                                                      *
 *  ----------------------------------------------------------------------------------  *
 *  |    0    |    1    |    2    |    3    |    4     |    5    |    6    |    7    |  *
 *  ----------------------------------------------------------------------------------  *
 *  |   0x0   |   0x4   |   0x8   |   0xc   |   0x10   |   0x14  |   0x18  |   0x1c  |  *
 *  ----------------------------------------------------------------------------------  *
 *  |        R12        |         R13       |         R14        |        R15        |  *
 *  ----------------------------------------------------------------------------------  *
 *  ----------------------------------------------------------------------------------  *
 *  |    8    |    9    |   10    |   11    |    12    |    13   |    14   |    15   |  *
 *  ----------------------------------------------------------------------------------  *
 *  |   0x20  |   0x24  |   0x28  |  0x2c   |   0x30   |   0x34  |   0x38  |   0x3c  |  *
 *  ----------------------------------------------------------------------------------  *
 *  |        RBX        |         RBP       |         RIP        |       EXIT        |  *
 *  ----------------------------------------------------------------------------------  *
 *                                                                                      *
 ****************************************************************************************/
</pre>

The _EXIT_ field is going to be left unused for our purposes but it will be left in place anyway.

The first thing we need is to allocate space to store the context data and make sure it has a valid alignment for the architecture we&#8217;re dealing with

<pre>// Allocate context-stack space
context_stack = (void*)malloc(64_Kb);

std::size_t space = UNIX_CONTEXT_DATA_SIZE + 64;
sp = static_cast&lt;char*&gt;(context_stack) + 64_Kb - space;

sp = std::align(64, UNIX_CONTEXT_DATA_SIZE, sp, space);
assert(sp != nullptr && space &gt;= UNIX_CONTEXT_DATA_SIZE);
</pre>

_boost::context_ offers both memory-efficient on-demand growing stacks or fixed stack allocations (cfr. <a href="http://www.boost.org/doc/libs/1_62_0/libs/context/doc/html/context/stack.html" target="_blank">boost docs</a>). In this example code we&#8217;ll go for a fixed stack allocation.  
Since we can&#8217;t deal with registers directly in C++ we&#8217;ll have to fallback on a pure assembly routine. The <a href="https://en.wikipedia.org/wiki/GNU_Assembler" target="_blank">GAS</a> backend seems the logical tool of choice for this work. We therefore define an external function to link against our executable with C linkage

<pre>extern "C" fcontext_t jump_to_context(fcontext_t context);
</pre>

What is an _fcontext_t_? In a x86_64 world it is just a register&#8217;s content

<pre>using fcontext_t = void*;
</pre>

Luckily for us _RIP_ will have already been set by the fact we&#8217;re invoking _jump\_to\_context_ with a _CALL_ instruction so we get an instruction pointer on the stack for free in our assembly code

<pre>.text
.globl jump_to_context
.type jump_to_context,@function
.align 16
jump_to_context:
    pushq  %rbp  /* save RBP */
    pushq  %rbx  /* save RBX */
    pushq  %r15  /* save R15 */
    pushq  %r14  /* save R14 */
    pushq  %r13  /* save R13 */
    pushq  %r12  /* save R12 */

    /* omissis */

    /* restore RSP (pointing to context-data) from RDI */
    movq  %rdi, %rsp

    popq  %r12  /* restore R12 */
    popq  %r13  /* restore R13 */
    popq  %r14  /* restore R14 */
    popq  %r15  /* restore R15 */
    popq  %rbx  /* restore RBX */
    popq  %rbp  /* restore RBP */

    /* continue... */

.size jump_to_context,.-jump_to_context

/* Mark that we don't need executable stack. */
.section .note.GNU-stack,"",%progbits
</pre>

Using <a href="https://cmake.org/cmake/help/v3.0/command/project.html" target="_blank">CMake</a> putting everything together becomes quite easy

<pre>project(simple_crts CXX ASM)
cmake_minimum_required(VERSION 2.8.12)
set (CMAKE_CXX_STANDARD 14)

set_source_files_properties(jump_to_context_x86_64_elf_gas.S 
                            PROPERTIES COMPILE_FLAGS "-x assembler-with-cpp")

add_executable(simple_crts simple_crts.cpp jump_to_context_x86_64_elf_gas.S)
target_link_libraries(simple_crts ${CONAN_LIBS} pthread)
</pre>

### Trampolines to coroutines

Something is missing at this point: we need a valid _RIP_ pointer to the coroutine to jump to. We could enter the coroutine and have another function store this information for us, but there&#8217;s a better way which avoids cluttering the coroutine code entirely: using a trampoline function.

Just as in <a href="https://github.com/boostorg/context/blob/2e5430fd27b963ffd72e7ee820ae81bb34c17a33/include/boost/context/execution_context_v2.hpp#L66" target="_blank">boost::context</a>, we define a trampoline function ourselves which, when jumped to, re-jumps to the caller and saves its context as a pre-stage for the coroutine

<pre>void trampoline(fcontext_t ctx) {

  yield_ctx = jump_to_context(ctx);

  wannabe_coroutine();
}
</pre>

What we have to do now is a simplified version of the _make_context_ routine to set the first _RIP_ towards the trampoline&#8217;s prologue

<pre>// Do make_context's work (simplified)
// Do *NOT* try this at home (or even worse in the office)
void** addr = reinterpret_cast&lt;void**&gt;(static_cast&lt;char*&gt;(sp) +
                                         UNIX_CONTEXT_DATA_RIP_OFFSET);
*addr = reinterpret_cast&lt;void*&gt;(&trampoline);

// In a more complex case there might be additional initialization and
// frame adjustments going on
coroutine_ctx = jump_to_context(sp);
</pre>

So right now we have a valid trampoline _RIP_ set in place

<pre>/****************************************************************************************
 *                                                                                      *
 *  ----------------------------------------------------------------------------------  *
 *  |    0    |    1    |    2    |    3    |    4     |    5    |    6    |    7    |  *
 *  ----------------------------------------------------------------------------------  *
 *  |   0x0   |   0x4   |   0x8   |   0xc   |   0x10   |   0x14  |   0x18  |   0x1c  |  *
 *  ----------------------------------------------------------------------------------  *
 *  |        R12        |         R13       |         R14        |        R15        |  *
 *  ----------------------------------------------------------------------------------  *
 *  ----------------------------------------------------------------------------------  *
 *  |    8    |    9    |   10    |   11    |    12    |    13   |    14   |    15   |  *
 *  ----------------------------------------------------------------------------------  *
 *  |   0x20  |   0x24  |   0x28  |  0x2c   |   0x30   |   0x34  |   0x38  |   0x3c  |  *
 *  ----------------------------------------------------------------------------------  *
 *  |        RBX        |         RBP       |         RIP        |       EXIT        |  *
 *  ----------------------------------------------------------------------------------  *
 *                                           ^^^^^^^^^^^^^^^^^^^^                       *
 ****************************************************************************************/
</pre>

This kickstarts the bouncing to/from the trampoline:

<pre>.text
.globl jump_to_context
.type jump_to_context,@function
.align 16
jump_to_context:
    pushq  %rbp
    pushq  %rbx 
    pushq  %r15 
    pushq  %r14 
    pushq  %r13 
    pushq  %r12 

    /* store RSP (pointing to context-data) in RAX */
    movq  %rsp, %rax

    movq  %rdi, %rsp

    popq  %r12 
    popq  %r13 
    popq  %r14 
    popq  %r15 
    popq  %rbx 
    popq  %rbp 

    /* restore return-address (must have been put on the new stack) */
    popq  %r8

    /*
       pass the old context as first parameter (if we're headed
       towards a landing function)
    */
    movq  %rax, %rdi

    /* indirect jump to new context */
    jmp  *%r8

.size jump_to_context,.-jump_to_context
.section .note.GNU-stack,"",%progbits
</pre>

It is important to note that we&#8217;re keeping the stack aligned during this entire process (recall that the stack has to be 16-bytes aligned before a _call_ instruction is issued).

The process roughly goes on like this  
[<img loading="lazy" class="alignnone size-full wp-image-6917" src="http://www.italiancpp.org/wp-content/uploads/2016/10/coroutines_graph1.png" alt="coroutines_graph1" width="900" height="300" srcset="http://192.168.64.2/wordpress/wp-content/uploads/2016/10/coroutines_graph1.png 900w, http://192.168.64.2/wordpress/wp-content/uploads/2016/10/coroutines_graph1-300x100.png 300w, http://192.168.64.2/wordpress/wp-content/uploads/2016/10/coroutines_graph1-768x256.png 768w, http://192.168.64.2/wordpress/wp-content/uploads/2016/10/coroutines_graph1-600x200.png 600w, http://192.168.64.2/wordpress/wp-content/uploads/2016/10/coroutines_graph1-250x83.png 250w" sizes="(max-width: 900px) 100vw, 900px" />](http://www.italiancpp.org/wp-content/uploads/2016/10/coroutines_graph1.png)

It has to be noted that the trampoline function might reserve stack space for its parameters as well. In the code above we allocated 64Kb of heap space to be used as stack space for context operations. So after the first jump the _sp_ automatic variable is no longer reliable. _coroutine_ctx_ should be used instead.

### Resuming fcontext

Resuming trampoline&#8217;s _fcontext_ requires another _call and rip-save_ and stack pointer adjustment to _coroutine_ctx_. Trampoline&#8217;s old _RIP_ will be available for free after we&#8217;ve restored the first 48 bytes of the _fcontext_.

Execution can afterwards continue to the designated coroutine. At this point the coroutine should be somehow encapsulated to be able to use the _yield_ctx_ context pointer: that is the gateway to our (in an asymmetric view) caller context.

Each time we want to yield execution back to the caller we&#8217;ll have to _jump\_to\_context_ to the _yield_ctx_

<pre>void yield() {
  yield_ctx = jump_to_context(yield_ctx);
}

void wannabe_coroutine() {
  std::cout &lt;&lt; "I wanna be a coroutine when I grow my stack space up\n";
  yield();
  std::cout &lt;&lt; "Hooray!\n";
  yield();
}
</pre>

Notice that we&#8217;re also reassigning the variable with the return value provided by _jump\_to\_context_. This assignment is not executed until the control flow comes back to the _yield()_ function

<pre>.. save

/* store RSP (pointing to context-data) in RAX */
movq  %rsp, %rax

.. restore
</pre>

This is a cooperative behavior example: each _jump\_to\_context()_ invocation from this point onward actually returns _fcontext_ data for the previous invocation.

The rest of the code bounces back and forth through the contexts resulting in the following sequence

[<img loading="lazy" class="alignnone size-full wp-image-6919" src="http://www.italiancpp.org/wp-content/uploads/2016/10/coroutines_graph2.png" alt="coroutines_graph2" width="697" height="1236" srcset="http://192.168.64.2/wordpress/wp-content/uploads/2016/10/coroutines_graph2.png 697w, http://192.168.64.2/wordpress/wp-content/uploads/2016/10/coroutines_graph2-169x300.png 169w, http://192.168.64.2/wordpress/wp-content/uploads/2016/10/coroutines_graph2-577x1024.png 577w, http://192.168.64.2/wordpress/wp-content/uploads/2016/10/coroutines_graph2-600x1064.png 600w, http://192.168.64.2/wordpress/wp-content/uploads/2016/10/coroutines_graph2-250x443.png 250w" sizes="(max-width: 697px) 100vw, 697px" />](http://www.italiancpp.org/wp-content/uploads/2016/10/coroutines_graph2.png)

At the end of the day the stack is freed (sounds weird to say) and the program terminates.

## Exercise: wrapping up

As a didactic exercise (i.e. **do not EVER use this code in a production environment**) we can use some metaprogramming to wrap our coroutines and avoid polluting our code with stack adjustments and cleanup boilerplate. Eventually we&#8217;d like to end up with code like this

<pre>int g_fib = -1;

void fibonacci_gen() {

  int first = 1;
  g_fib = first;
  yield();

  int second = 1;
  g_fib = second;
  yield();

  for (int i = 0; i &lt; 9; ++i) {

    int third = first + second;
    first = second;
    second = third;
    g_fib = third;
    yield();

  }

}

int main() {

  // Outputs the first 10 Fibonacci numbers

  coroutine&lt;void(void)&gt; coro(fibonacci_gen);

  for (int i = 0; i &lt;= 10; ++i) {
      coro.resume();

    if(i) std::cout &lt;&lt; g_fib &lt;&lt; " ";
  }

}
</pre>

To do this we create a templated wrapper class

<pre>template class coroutine;
</pre>

that will handle the stack and trampoline setup for us. One difference from the first example is the need for a wrapper that will handle the trampoline invocation (shields us from <a href="http://www.codeproject.com/Articles/7150/Member-Function-Pointers-and-the-Fastest-Possible" target="_blank">implementation-dependent</a> issues)

<pre>template 
void call_member_trampoline(coroutine *instance, fcontext_t ctx) {
  instance-&gt;trampoline(ctx);
}
</pre>

The trampoline is therefore modified as follows

<pre>void trampoline(fcontext_t ctx) {

  size_t index = yield_ctx.size() - 1;
  yield_ctx[index] = jump_to_context(this, ctx);

  this-&gt;m_fn();
}
</pre>

The only difference in the _jump\_to\_context()_ function is in handling its new arity

<pre>/* restore RSP (pointing to context-data) from RSI */
movq  %rsi, %rsp
</pre>

and the promotion of _%rdi_ from scratch-register to parameter-register (since we&#8217;re directly jumping to a destination context&#8217;s _RIP_).

The rest of the code remains largely unchanged.

## Back to boost::context

If you&#8217;ve followed through the entire article and you made it here, you should by now know what the following _boost::context2_ program does

[compiler]

<pre>#include &lt;boost/context/all.hpp&gt;
#include &lt;iostream&gt;
#include &lt;array&gt;

namespace ctx = boost::context::detail;

class Coroutine {
public:
  Coroutine() {
    my_context = ctx::make_fcontext(
      stack.data() + stack.size(),
      stack.size(),
      &Coroutine::dispatch
    );
  }
  virtual ~Coroutine() {}

  void operator()() {
    auto transfer_ctx = ctx::jump_fcontext(my_context, this);
    my_context = transfer_ctx.fctx;
  }

protected:
  void yield() {
    auto transfer_ctx = ctx::jump_fcontext(yield_context, 0);
    my_context = transfer_ctx.fctx;
  }

  virtual void call() = 0;

private:
  static void dispatch(ctx::transfer_t coroutine_ptr) {
    Coroutine *coroutine = reinterpret_cast&lt;Coroutine *&gt;(coroutine_ptr.data);
    coroutine-&gt;yield_context = coroutine_ptr.fctx;
    coroutine-&gt;call();
    while(true)
      coroutine-&gt;yield();
  }

private:
  ctx::fcontext_t my_context;
  ctx::fcontext_t yield_context;
  std::array&lt;intptr_t, 66 * 1024&gt; stack;
};

struct A : public Coroutine {
  void call() {
    std::cout &lt;&lt; " __________________________________ " &lt;&lt; std::endl;
    yield();
    std::cout &lt;&lt; "|    _       _       |_|    _| |_  |" &lt;&lt; std::endl;
    yield();
    std::cout &lt;&lt; "|   |_|     |_|      | |     | |_  |" &lt;&lt; std::endl;
  }
};

struct B : public Coroutine {
  void call() {
    std::cout &lt;&lt; "|                                  |" &lt;&lt; std::endl;
    yield();
    std::cout &lt;&lt; "|  _| |_   _| |_      _    |_   _| |" &lt;&lt; std::endl;
    yield();
    std::cout &lt;&lt; "|                    |_|     |___| |" &lt;&lt; std::endl;
    yield();
    std::cout &lt;&lt; "|                                  |" &lt;&lt; std::endl;
    yield();
    std::cout &lt;&lt; "|__________________________________|" &lt;&lt; std::endl;
  }
};

struct C : public Coroutine {
  void call() {
    std::cout &lt;&lt; "|                     _       _    |" &lt;&lt; std::endl;
    yield();
    std::cout &lt;&lt; "| |_   _| |_   _|    | |     | |   |" &lt;&lt; std::endl;
  }

  void operator++(int) {
    std::cout &lt;&lt; "| ++It - The Italian C++ Community |" &lt;&lt; std::endl;
    std::cout &lt;&lt; "|__________________________________|" &lt;&lt; std::endl;
  }
};


int main() {

  A a;
  B b;
  C c;
  for (size_t i = 0; i&lt;10; ++i) {
    a();
    b();
    c();
  }

  c++; // An entire operator overloading to write 'c++'? Worth it!
}
</pre>

[/compiler]

## Final words

Coroutines provide a powerful abstraction to offer the same level of concurrency one would get with asynchronous callbacks by offering at the same time a chance to write more maintainable code. At the time of writing this article boost offers context, coroutine and fiber libraries. As we&#8217;ve seen _boost::context_ provides the foundation for userland context switches, _boost::coroutine2_ offers coroutines support (which conceptually have no need of synchronization whatsoever since they implement a nonpreemptive cooperative multitasking) and _boost::fiber_ which builds on _boost::context_ to add a scheduling mechanism: each time a fiber yields, control is given back to a scheduler manager which decides the next execution strategy (cfr. <a href="http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2014/n4024.pdf" target="_blank">N4024</a>).

As usual it is up to the programmer to carefully choose which abstractions are to be used in a specific context.

## References and credits

  * <a href="http://www.boost.org/doc/libs/" target="_blank">The boost library</a>
  * <a href="http://www.crystalclearsoftware.com/soc/coroutine/coroutine/implementation.html" target="_blank">Coroutine implementation</a>
  * <a href="http://www.chiark.greenend.org.uk/~sgtatham/coroutines.html" target="_blank">Coroutines in C</a>
  * <a href="https://isocpp.org/files/papers/n3985.pdf" target="_blank">N3985</a>
  * <a href="http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2014/n4024.pdf" target="_blank">N4024</a>
  * [Library Foundations for Asynchronous Operations](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2014/n3964.pdf)

Special thanks to the ++it community and Oliver Kowalke for providing insights and reviews of parts of this article.