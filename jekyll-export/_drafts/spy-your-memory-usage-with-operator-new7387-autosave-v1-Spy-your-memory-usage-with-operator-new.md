---
id: 8250
title: Spy your memory usage with operator new
date: 2018-01-14T13:18:54+01:00
author: stefano
layout: revision
guid: http://www.italiancpp.org/2017/09/01/7387-autosave-v1/
permalink: /2018/01/14/7387-autosave-v1/
---
_Special thanks to_ **_Marco Alesiani_** _for many corrections and suggestions._

_Anche tu campi a spaghetti e pizza? Leggi [l&#8217;articolo in italiano](http://www.italiancpp.org/?p=7318)._

* * *

When we say &#8220;efficiency&#8221;, we often think &#8220;time&#8221;. The sooner the code does its job, the more it is efficient.

What about memory? Granted, today even the lousiest laptop comes with &#8220;a bucket load&#8221; of RAM which… is never enough. My PC &#8220;wastes&#8221; 1.4GB just to idle. I open a browser, 300 more MB are gone.<a href="javascript:void(0);" data-target="#nota1" data-toggle="collapse">*</a>.

<div id="nota1" class="collapse inlineNote" data-target="#nota1" data-toggle="collapse">
  &#8230;we take the occasion to apologize for the “Allowed memory size of &#8230; bytes exhausted “ errors and the white pages that you may occasionally see on ++It. There is a reason why we care so much about memory.
</div>

Adding insult to injury, using memory is one of the slowest operations on current systems<a href="javascript:void(0);" data-target="#nota2" data-toggle="collapse">*</a>.

<div id="nota2" class="collapse inlineNote" data-target="#nota2" data-toggle="collapse">
  (Italian only) Daniele Maccioni: <a href="http://www.italiancpp.org/sessioni-cppday16/#cpp17">Data Oriented Design: alte performance in C++</a>
</div>

Moreover, finding the culprit line among the code is not easy. Was it a &#8220;new&#8221; we wrote? Some allocation hidden inside a library? Are temporary objects to blame?

_How to easily find the part of the code that uses most of the memory?_

This post collects some personal experiments. You can &#8220;thank&#8221; the author for any mistake.

#### Let&#8217;s use some memory

Today&#8217;s toy-code is nothing special, but it does many an allocation using operator new.

[snippet]  
/* Program that allocates some memory when it feels like.  
No delete &#8211; today&#8217;s essay is not about memory leaks.*/  
#include <string>  
#include <memory>  
#include <boost/shared_ptr.hpp>  
#include <boost/make_shared.hpp>  
#include "SomeClass.h"  
//  
void h() {  
SomeClass* t = new SomeClass();  
}  
void g() { h(); }  
void f() { g(); }  
void MakeSomeClass() { f(); }  
//  
int main(int argc, char **argv) {  
int * number = new int(89);  
std::string * test = new std::string("abc");  
//  
SomeClass * oggetto = new SomeClass();  
MakeSomeClass();  
//  
boost::shared\_ptr<SomeClass> smartPointer = boost::make\_shared<SomeClass>();  
std::shared\_ptr<SomeClass> stdSmartPointer = std::make\_shared<SomeClass>();  
return 0;  
}  
[/snippet]

Compile, run and&#8230; almost 42MB (measured &#8220;on the cheap&#8221; with <span class="inlineCode">/usr/bin/time -v</span>).

_Who is using all that memory?_

#### The right way: memory profiler

The idea should be familiar: the &#8220;classic&#8221; profiler tells for how long each function executes. The memory profiler instead tells where and when the program uses memory, and how much.  
For example, here is some of the information that Massif <a href="javascript:void(0);" data-target="#nota3" data-toggle="collapse">*</a> returns about our program.

<div id="nota3" class="collapse inlineNote" data-target="#nota3" data-toggle="collapse">
  <a href="http://valgrind.org/docs/manual/ms-manual.html">http://valgrind.org/docs/manual/ms-manual.html</a><br /> Should you work on Windows: <a href="https://blogs.msdn.microsoft.com/vcblog/2015/10/21/memory-profiling-in-visual-c-2015/">https://blogs.msdn.microsoft.com/vcblog/2015/10/21/memory-profiling-in-visual-c-2015/</a>
</div>

We can start with the memory growth (in ASCII art!) over &#8220;time&#8221; &#8211; actually its growth over the number of executed instructions:

<pre>MB
38.23^                                                           ::::::::::::#
     |                                                           :           #
     |                                                           :           #
     |                                                           :           #
     |                                                           :           #
     |                                               :::::::::::::           #
     |                                               :           :           #
     |                                               :           :           #
     |                                               :           :           #
     |                                               :           :           #
     |                                   @@@@@@@@@@@@:           :           #
     |                                   @           :           :           #
     |                                   @           :           :           #
     |                                   @           :           :           #
     |                                   @           :           :           #
     |                       ::::::::::::@           :           :           #
     |                       :           @           :           :           #
     |                       :           @           :           :           #
     |                       :           @           :           :           #
     |                       :           @           :           :           #
   0 +----------------------------------------------------------------------->Mi
     0                                                                   6.203
</pre>

Then we can get detailed snapshots (the &#8220;A&#8221;, &#8220;B&#8221; and &#8220;C&#8221; tags are ours):

<pre>--------------------------------------------------------------------------------
  n        time(i)         total(B)   useful-heap(B) extra-heap(B)    stacks(B)
--------------------------------------------------------------------------------
...
  9      4,311,691       30,080,056       30,072,844         7,212            0
99.98% (30,072,844B) (heap allocation functions) malloc/new/new[], --alloc-fns, etc.
-&gt;99.73% (30,000,000B) 0x4078E8: __gnu_cxx::new_allocator&lt;char&gt;::allocate(unsigned long, void const*) (new_allocator.h:104)
| -&gt;99.73% (30,000,000B) 0x40785A: std::allocator_traits&lt;std::allocator&lt;char&gt; &gt;::allocate(std::allocator&lt;char&gt;&, unsigned long) (alloc_traits.h:491)
|   -&gt;99.73% (30,000,000B) 0x407800: std::_Vector_base&lt;char, std::allocator&lt;char&gt; &gt;::_M_allocate(unsigned long) (stl_vector.h:170)
|     -&gt;99.73% (30,000,000B) 0x40777B: std::_Vector_base&lt;char, std::allocator&lt;char&gt; &gt;::_M_create_storage(unsigned long) (stl_vector.h:185)
|       -&gt;99.73% (30,000,000B) 0x4076A7: std::_Vector_base&lt;char, std::allocator&lt;char&gt; &gt;::_Vector_base(unsigned long, std::allocator&lt;char&gt; const&) (stl_vector.h:136)
|         -&gt;99.73% (30,000,000B) 0x407636: std::vector&lt;char, std::allocator&lt;char&gt; &gt;::vector(unsigned long, std::allocator&lt;char&gt; const&) (stl_vector.h:278)
|           -&gt;99.73% (30,000,000B) 0x4075C5: SomeClass::SomeClass() (SomeClass.cpp:4)
|  A ====>   -&gt;33.24% (10,000,000B) 0x405F91: main (main.cpp:20)
|             | 
|  B ====>    -&gt;33.24% (10,000,000B) 0x405EC1: h() (main.cpp:10)
|             | -&gt;33.24% (10,000,000B) 0x405EEF: g() (main.cpp:12)
|             |   -&gt;33.24% (10,000,000B) 0x405EFB: f() (main.cpp:13)
|             |     -&gt;33.24% (10,000,000B) 0x405F07: MakeSomeClass() (main.cpp:14)
|             |       -&gt;33.24% (10,000,000B) 0x405F9A: main (main.cpp:21)
|             |         
|  C ====>    -&gt;33.24% (10,000,000B) 0x4063F2: _ZN5boost11make_sharedI9SomeClassIEEENS_6detail15sp_if_not_arrayIT_E4typeEDpOT0_ (make_shared_object.hpp:254)
|               -&gt;33.24% (10,000,000B) 0x405FA6: main (main.cpp:23)
|                 
-&gt;00.24% (72,844B) in 1+ places, all below ms_print's threshold (01.00%)
</pre>

We quickly see that line 20 of the main uses one third of the memory (A) where we wrote a new. The next 30% of the memory (B) is allocated in h() &#8211; Massif recorded all the call stack at the point of allocation. We can trace it down to the call to MakeSomeClass() in the main. Massif also works with shared pointers (C).

We can&#8217;t see the allocation at line 24 because it has not yet been executed and &#8220;intercepted&#8221; by Massif. We may spot it in a later snapshot. The remaining allocations are &#8220;small&#8221; and summarized in the last line.

A quick glance at the report tells us to go check the constructor of SomeClass. What the heck is it doing with a std::vector that takes 99% of the memory?

This is already a good result, obtained with little effort. Be aware that Massif can do more. It can measure the memory used &#8220;behind the scenes&#8221; by the system to make the heap work (extra-heap – 7,212 bytes in the example), track the stack&#8230;

#### The do-it-yourself way: override operator new

C++ allows to replace the operator to create objects (new) with a custom one.<a href="javascript:void(0);" data-target="#nota4" data-toggle="collapse">*</a>

<div id="nota4" class="collapse inlineNote" data-target="#nota4" data-toggle="collapse">
  <a href="http://en.cppreference.com/w/cpp/memory/new/operator_new">http://en.cppreference.com/w/cpp/memory/new/operator_new</a>
</div>

Almost nobody has a good reason to do so, but we do: <span style="text-decoration: line-through;">I could not figure out how to use the profiler</span> intercept heap allocations.

By and large, all we have to do is define a custom new (and its overloads) in any file of a program.

If the memory profiler is an equivalent of the “time” profiler, then you can compare this trick to the classic snippet <span class="inlineCode">cout << endTime - startTime;</span>. Not really detailed or accurate, but simple and useful.

A few lines of code can give us something raw, but usable. You should compile with debug symbols. The code that outputs the stack trace can probably work only on Linux.<a href="javascript:void(0);" data-target="#nota5" data-toggle="collapse">*</a>.

<div id="nota5" class="collapse inlineNote">
  <!-- No collapse on click, altrimenti non si può cliccare per fare copia e incolla del codice. -->
  
  <br /> There is nothing portable when you work at low level.</p> 
  
  <p>
    If you are in the Microsoft world: <a href="https://msdn.microsoft.com/en-us/library/windows/desktop/bb204633%28v=vs.85%29.aspx">https://msdn.microsoft.com/en-us/library/windows/desktop/bb204633%28v=vs.85%29.aspx</a>.
  </p>
  
  <p>
    That means:
  </p>
  
  <p>
    [snippet]<br /> #include <iostream><br /> //<br /> #include <Windows.h> // Capture stack traces.<br /> #include <Dbghelp.h> // Read debug symbols.
  </p>
  
  <p>
    //<br /> void StackTrace() {<br /> /* Capture the stack trace. */<br /> const ULONG doNotSkipAnyFrame = 0;<br /> const ULONG takeTenFrames = 10;<br /> const PULONG doNotHash = nullptr;<br /> PVOID stackTrace[takeTenFrames];<br /> const USHORT framesCaptured = CaptureStackBackTrace(<br /> doNotSkipAnyFrame,<br /> takeTenFrames,<br /> stackTrace,<br /> doNotHash<br /> );<br /> //<br /> /*Prepare the symbol table to convert from addresses to lines of code. */<br /> const HANDLE thisProcess = GetCurrentProcess();<br /> SymInitialize(thisProcess, NULL, TRUE); // Linkare Dbghelp.lib<br /> //<br /> for (ULONG i = 0; i < framesCaptured; i++) {<br /> /*Estrae il nome della funzione. */<br /> const size_t nameStringSize = 256;<br /> SYMBOL_INFO * functionData = (SYMBOL_INFO*)malloc(sizeof(SYMBOL_INFO) + (nameStringSize + 1) * sizeof(char)); // +1 because there is \0<br /> functionData->MaxNameLen = nameStringSize;<br /> functionData->SizeOfStruct = sizeof(SYMBOL_INFO);<br /> SymFromAddr(thisProcess, (DWORD64)(stackTrace[i]), 0, functionData);<br /> //<br /> /* Find the file matching the function call.*/<br /> DWORD displacementInLine;<br /> IMAGEHLP_LINE64 lineOfCode;<br /> lineOfCode.SizeOfStruct = sizeof(IMAGEHLP_LINE64);<br /> SymGetLineFromAddr64(thisProcess, (DWORD)(stackTrace[i]), &displacementInLine, &lineOfCode);<br /> //<br /> std::cout << functionData->Name << " at "<br /> << lineOfCode.FileName << ":" << lineOfCode.LineNumber << std::endl;<br /> }<br /> }<br /> [/snippet]
  </p>
</div>

.

[snippet]  
// Our special new must allocate memory as expected&#8230;  
#include <cstdio>  
#include <cstdlib>  
// &#8230;but also inspect the stack and print some results.  
#include <execinfo.h>  
#include <unistd.h>  
#include <fstream>  
// Import bad_alloc, expected in case of errors.  
#include <new>  
//  
/\* Opens (once) and return the file to save the results.. \*/  
static std::ofstream& resultFile() {  
static std::ofstream memoryProfile;  
static bool open = false; // Init on 1st use, as usual.  
if (! open) {  
memoryProfile.open ("allocations.txt");  
open = true;  
}  
// Else, handle errors, close the file&#8230;  
// We won&#8217;t do it, to keep the example simple.  
return memoryProfile;  
}  
//  
/\* This is the "magic" function that inspect the stack and writes it in a file. \*/  
static void dumpStackTrace(std::ofstream& memoryProfile) {  
// Record 15 pointers to stack frame &#45; enough for the example program.  
const int maximumStackSize = 15;  
void *callStack[maximumStackSize];  
size_t framesInUse = backtrace(callStack, maximumStackSize);  
// Now callStack is full of pointers. Request the names of the functions matching each frame.  
char ** mangledFunctionNames = backtrace_symbols(callStack, framesInUse);  
// Writes all the function names in the stream.  
for (size_t i = 0; i < framesInUse; ++i)  
memoryProfile << mangledFunctionNames[i] << std::endl;  
// To be fair, we should release mangledFunctionNames with free&#8230;  
}  
//  
/\* Now we have all the elements to build the custom operator new. \*/  
void* operator new(std::size_t sz) {  
// Allocate the requested memory for the caller.  
void * requestedMemory = std::malloc(sz);  
if (! requestedMemory)  
throw std::bad_alloc();  
// Share our allocations with the world.  
std::ofstream& memoryProfile = resultFile();  
memoryProfile << "Allocation, size = " << sz << " at " << static_cast<void*>(requestedMemory) << std::endl;  
dumpStackTrace(memoryProfile);  
memoryProfile << "&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;" << std::endl; // Poor man&#8217;s separator.

return requestedMemory;  
}  
[/snippet]

Let&#8217;s add the &#8220;tricked out&#8221; operator new to our test program. This is an example of the result &#8211; can you guess the line of code behind it?

<pre>Allocation, size = 40 at 0x18705b0
./overridenew(_Z14dumpStackTraceRSt14basic_ofstreamIcSt11char_traitsIcEE+0x3c) [0x40672c]
./overridenew(_Znwm+0xaf) [0x406879]
./overridenew(_ZN9__gnu_cxx13new_allocatorISt23_Sp_counted_ptr_inplaceI9SomeClassSaIS2_ELNS_12_Lock_policyE2EEE8allocateEmPKv+0x4a) [0x405d9e]
./overridenew(_ZNSt16allocator_traitsISaISt23_Sp_counted_ptr_inplaceI9SomeClassSaIS1_ELN9__gnu_cxx12_Lock_policyE2EEEE8allocateERS6_m+0x28) [0x405bef]
./overridenew(_ZSt18__allocate_guardedISaISt23_Sp_counted_ptr_inplaceI9SomeClassSaIS1_ELN9__gnu_cxx12_Lock_policyE2EEEESt15__allocated_ptrIT_ERS8_+0x21) [0x4059e2]
./overridenew(_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEC2I9SomeClassSaIS4_EJEEESt19_Sp_make_shared_tagPT_RKT0_DpOT1_+0x59) [0x4057e1]
./overridenew(_ZNSt12__shared_ptrI9SomeClassLN9__gnu_cxx12_Lock_policyE2EEC2ISaIS0_EJEEESt19_Sp_make_shared_tagRKT_DpOT0_+0x3c) [0x4056ae]
./overridenew(_ZNSt10shared_ptrI9SomeClassEC2ISaIS0_EJEEESt19_Sp_make_shared_tagRKT_DpOT0_+0x28) [0x40560e]
./overridenew(_ZSt15allocate_sharedI9SomeClassSaIS0_EIEESt10shared_ptrIT_ERKT0_DpOT1_+0x37) [0x405534]
./overridenew(_ZSt11make_sharedI9SomeClassJEESt10shared_ptrIT_EDpOT0_+0x3b) [0x405454]
./overridenew(main+0x9c) [0x4052e8]
/lib/x86_64-linux-gnu/libc.so.6(__libc_start_main+0xf0) [0x7f83fe991830]
./overridenew(_start+0x29) [0x405079]
-----------
Allocation, size = 10000000 at 0x7f83fc9c3010
./overridenew(_Z14dumpStackTraceRSt14basic_ofstreamIcSt11char_traitsIcEE+0x3c) [0x40672c]
./overridenew(_Znwm+0xaf) [0x406879]
./overridenew(_ZN9__gnu_cxx13new_allocatorIcE8allocateEmPKv+0x3c) [0x406538]
./overridenew(_ZNSt16allocator_traitsISaIcEE8allocateERS0_m+0x28) [0x4064aa]
./overridenew(_ZNSt12_Vector_baseIcSaIcEE11_M_allocateEm+0x2a) [0x406450]
./overridenew(_ZNSt12_Vector_baseIcSaIcEE17_M_create_storageEm+0x23) [0x4063cb]
./overridenew(_ZNSt12_Vector_baseIcSaIcEEC1EmRKS0_+0x3b) [0x4062f7]
./overridenew(_ZNSt6vectorIcSaIcEEC2EmRKS0_+0x2c) [0x406286]
./overridenew(_ZN9SomeClassC1Ev+0x3d) [0x406215]
./overridenew(_ZN9__gnu_cxx13new_allocatorI9SomeClassE9constructIS1_JEEEvPT_DpOT0_+0x36) [0x405e3a]
./overridenew(_ZNSt16allocator_traitsISaI9SomeClassEE9constructIS0_JEEEvRS1_PT_DpOT0_+0x23) [0x405d51]
./overridenew(_ZNSt23_Sp_counted_ptr_inplaceI9SomeClassSaIS0_ELN9__gnu_cxx12_Lock_policyE2EEC2IJEEES1_DpOT_+0x8c) [0x405b4a]
./overridenew(_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEC2I9SomeClassSaIS4_EJEEESt19_Sp_make_shared_tagPT_RKT0_DpOT1_+0xaf) [0x405837]
./overridenew(_ZNSt12__shared_ptrI9SomeClassLN9__gnu_cxx12_Lock_policyE2EEC2ISaIS0_EJEEESt19_Sp_make_shared_tagRKT_DpOT0_+0x3c) [0x4056ae]
./overridenew(_ZNSt10shared_ptrI9SomeClassEC2ISaIS0_EJEEESt19_Sp_make_shared_tagRKT_DpOT0_+0x28) [0x40560e]

...
</pre>

&#8230;I can&#8217;t. Where is &#8220;main+0xa8&#8221; in my code? Thankfully in the &#8220;gnu/Linux world&#8221; there are tools to de-mangle names and find the point in the code that corresponds to a given address. We can use them, for example, in a simple <a href="javascript:void(0);" data-target="#nota6" data-toggle="collapse">script</a>.

<div id="nota6" class="collapse inlineNote">
  [snippet]<br /> #!/usr/bin/python<br /> #<br /> # C++filt demangles names.<br /> #<br /> # addr2line converts code pointers (e. g. functions&#8217; addresses)<br /> # into the file:line couple corresponding to the code (if there are debug symbols).<br /> #<br /> # The python code should be portable, but the called utilities aren&#8217;t.<br /> #</p> 
  
  <p>
    import re<br /> import subprocess<br /> #
  </p>
  
  <p>
    # Opens a sub-process and passes shell commands to it. Returns the results as a string.<br /> # Not very efficient, but easy.<br /> def run_shell(command):<br /> return subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0]<br /> #<br /> #<br /> if __name__ == "__main__":<br /> total_size = 0;<br /> #<br /> # There are 2 types of lines in the output: stack frames and allocation sizes.<br /> size_line = re.compile("Allocation, size = (\d+) at (\d+)") # Allocation, size = <bytes> at <pointer somewhere in the heap><br /> stack_line = re.compile(".*\((.*)\+.*\) \[(.*)\]") # <rubbish>(mangled name) [<code pointer>]<br /> #<br /> allocations_file = open("allocations.txt")<br /> for line in allocations_file:<br /> match_size = size_line.match(line)<br /> match_stack = stack_line.match(line)<br /> #<br /> # For a demo, I compute the sum of all the used memory.<br /> # The things you can do with an overridden new!<br /> if (match_size):<br /> allocation_size = int(match_size.group(1))<br /> total_size += allocation_size<br /> print "Used " + str(allocation_size)<br /> #<br /> elif (match_stack):<br /> mangled_name = match_stack.group(1)<br /> line_address = match_stack.group(2)<br /> demangled_name = run_shell(["c++filt", "-n", mangled_name])<br /> line_number = run_shell(["addr2line", "-e", "./overridenew", line_address])<br /> #<br /> # This is not professional-grade formatting. The -1 cuts away the newlines.<br /> print"\t" + demangled_name[:-1] + "\n\t\t" + line_number,<br /> #<br /> # Copy the separator as they were.<br /> else:<br /> print line<br /> #<br /> print "\n total allocated size " + str(total_size)<br /> [/snippet]
  </p>
</div>

As an alternative, we could to everything at run time, using the compiler&#8217;s demangling utilities, such as [the gcc one](https://gcc.gnu.org/onlinedocs/libstdc++/manual/ext_demangling.html). Personally I prefer to keep the code instrumentation as simple as possible and do the &#8220;heavy lifting&#8221; off-line. My script returns:

<pre>Used 40
    dumpStackTrace(std::basic_ofstream&lt;char, std::char_traits&lt;char&gt; &gt;&)
        /home/stefano/projects/code/spy-memory-with-new/InstrumentedNew.cpp:29
    operator new(unsigned long)
        /home/stefano/projects/code/spy-memory-with-new/InstrumentedNew.cpp:48
    __gnu_cxx::new_allocator&lt;std::_Sp_counted_ptr_inplace&lt;SomeClass, std::allocator&lt;SomeClass&gt;, (__gnu_cxx::_Lock_policy)2&gt; &gt;::allocate(unsigned long, void const*)
        /usr/include/c++/5/ext/new_allocator.h:105
    
    ... internal calls of the shared pointer...
    
    std::shared_ptr&lt;SomeClass&gt; std::allocate_shared&lt;SomeClass, std::allocator&lt;SomeClass&gt;&gt;(std::allocator&lt;SomeClass&gt; const&)
        /usr/include/c++/5/bits/shared_ptr.h:620
    _ZSt11make_sharedI9SomeClassIEESt10shared_ptrIT_EDpOT0_
        /usr/include/c++/5/bits/shared_ptr.h:636
    main
        /home/stefano/projects/code/spy-memory-with-new/main.cpp:25
    __libc_start_main
        ??:0
    _start
        ??:?
-----------

Used 10000000
    dumpStackTrace(std::basic_ofstream&lt;char, std::char_traits&lt;char&gt; &gt;&)
        /home/stefano/projects/code/spy-memory-with-new/InstrumentedNew.cpp:29
    operator new(unsigned long)
        /home/stefano/projects/code/spy-memory-with-new/InstrumentedNew.cpp:48
    __gnu_cxx::new_allocator&lt;char&gt;::allocate(unsigned long, void const*)
        /usr/include/c++/5/ext/new_allocator.h:105
    
    ...internal calls of vector...
    
    std::vector&lt;char, std::allocator&lt;char&gt; &gt;::vector(unsigned long, std::allocator&lt;char&gt; const&)
        /usr/include/c++/5/bits/stl_vector.h:279
    SomeClass::SomeClass()
        /home/stefano/projects/code/spy-memory-with-new/SomeClass.cpp:4 (discriminator 2)
    ...
</pre>

The first allocation are the 40 bytes requested by make_shared. 24 for SomeClass (its only member is a vector &#8211; sizeof(vector) is 24), the rest should be the control block of the shared pointer. The second allocation are the 10MB in the notorious constructor of SomeClass.

It takes some effort to navigate the stacks, but it is possible to understand that the mistery line was <span class="inlineCode">std::shared_ptr<SomeClass> stdSmartPointer = std::make_shared<SomeClass>();</span> &#8211; close to the return at main.cpp:25.

Homework: how many allocations would there be with <span class="inlineCode">std::shared_ptr<SomeClass> notSoSmartPointer(new SomeClass());<br /> ?</span><a href="javascript:void(0);" data-target="#nota7" data-toggle="collapse">*</a>

<div id="nota7" class="collapse inlineNote" data-target="#nota7" data-toggle="collapse">
  Three, and using 8 more bytes.<br /> In a test I found:<br /> 24 bytes for SomeClass&#8217;s instance<br /> 10 MB to fill the vector<br /> 24 bytes for the shared pointer.</p> 
  
  <p>
    Looking at the <a href="en.cppreference.com/w/cpp/memory/shared_ptr">implementation notes</a>, I believe that the difference is in the content of the shared pointer&#8217;s control block. </div> 
    
    <hr />
    
    <h4>
      In the end&#8230;
    </h4>
    
    <p>
      Programmers have been fighting against memory since the dawn of time, because it is slow and too small. As for every bottleneck, one can&#8217;t trust his instincts. We saw that there are proper tools (memory profilers) to measure the memory usage. We discovered that, in a pinch, there are &#8220;home made&#8221; tools we can build ourselves with a &#8220;stereotypical C++ hack&#8221;, the override of operator new.
    </p>
    
    <p>
      <em>You can find the &#8220;ready-to-compile&#8221; code <a href="https://github.com/italiancpp/code/tree/master/spy-memory-with-new">in the ++It GitHub repo<a>.</em></p>