---
id: 5479
title: First steps with Boost.Python
date: 2015-12-02T19:11:41+01:00
author: stefano
layout: post
guid: http://www.italiancpp.org/?p=5479
permalink: /2015/12/02/first-steps-with-boost-python/
categories: Articoli
tags:
  - boost
  - python
---
### &#8220;Finally a modern, pragmatic language.&#8221;

Who among us wants to work with a multi-paradigm, highly-expressive, fast-evolving language with a huge standard library? We are talking, as usual, about&#8230; Python.

There are scenarios where our trusty champion (C++11) doesn&#8217;t cut it. For a prototype to rush out in a hurry, a &#8220;single use&#8221; script, the server side of a web application, research code&#8230; the complexity of C++ is more a problem than an asset.

How can we continue to take advantage of C++ efficiency or re-use some already available code without looking like old-fashioned cavemen?

The Python interpreter can load modules written in C, compiled as dynamic libraries. Boost.Python helps, a lot, to prepare them. It joins the power of Boost and C++ with the ease of use of Python.

Danger: even if all the examples compile, run and pass the tests this is not the ultimate guide about Boost.Python. The code is meant to be an example, it mirrors our (minimal) experience with Boost.Python. Do not hesitate to report any error we made.

#### A speed problem

Let&#8217;s see a (not too) practical use case. There are numbers which are equal to the sum of their divisors (6 = 3 + 2 + 1; [perfect numbers](https://en.wikipedia.org/wiki/Perfect_number)). The marketing department believes it is something hot, but we must compute as many perfect numbers as possible and release them before our competitors. The development speed enabled by Python is key, after 5 minutes we release Pefect 1.0<span style="font-family: Liberation Serif,serif;">®:</span>

[snippet]

<pre>def find_divisors(number):
	divisors = []
	for i in range(1, number):
		if number % i == 0:
			divisors.append(i)
	return divisors


def perfect(number):
	divisors = find_divisors(number)
	return number == sum(divisors)


def find_perfect_numbers(how_many):
	found = 0
	number_to_try = 1
	while (found &lt; how_many):
		if perfect(number_to_try):
			print number_to_try
			found += 1
		number_to_try += 1


if __name__ == "__main__":
	find_perfect_numbers(4)  # Look for more at your own risk.
							 # And prepare for a long wait.
</pre>

[/snippet]

This code is not really &#8220;pythonic&#8221; (<https://www.python.org/dev/peps/pep-0008/>), but it really was created, tested and debugged in less time that it takes to read a C++ compilation error.<a class="sdfootnoteanc" href="#sdfootnote1sym" name="sdfootnote1anc"><sup>1</sup></a>.

Unfortunately the execution time is similar: 6.5 seconds on my test machine (which is not your test machine, nor the production server, nor the Python fanboy&#8217;s PC which can run everything in a picosecond&#8230; it&#8217;s an example!).

Let&#8217;s look for the bottleneck with the profiler, like the savvy engineers we are.

[snippet]

<pre>import cProfile

... same code as before ...

if __name__ == "__main__":
	cProfile.run("find_perfect_numbers(4)")
</pre>

[/snippet]

Here is the outcome:

<pre>ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    5.657    5.657 &lt;string&gt;:1()
     8128    0.283    0.000    5.582    0.001 purePython.py:16(perfect)
        1    0.075    0.075    5.657    5.657 purePython.py:21(find_perfect_numbers)
     8128    4.294    0.001    5.229    0.001 purePython.py:8(find_divisors)
    66318    0.528    0.000    0.528    0.000 {method 'append' of 'list' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
     8128    0.406    0.000    0.406    0.000 {range}
     8128    0.070    0.000    0.070    0.000 {sum}
</pre>

find_divisors &#8220;steals&#8221; almost all of the 5.6 seconds it took to run this test!

#### boost::python

No-one denies that it is possible to write efficient code in Python (Java, VisualWhatever, this week&#8217;s functional language&#8230;), but optimize the algorithm of find_divisors is out of the question: we are here to show off Boost.Python, not to give an Algebra lesson.

First of all, we get our hands on Boost.Python. On a Linux box this is as easy as typing:

<pre>sudo apt-get install libboost-all-dev</pre>

You may need to install Python&#8217;s &#8220;dev&#8221; packages. It is easy to find instructions for any platform over the web, but installing (and compiling) the library may be the most difficult step. Do not lose heart.

This is the C++ code:  
[snippet]

<pre>#include "boost/python.hpp"  // (1)

boost::python::list findDivisors(uint64_t number) // (2)
{
	boost::python::list divisors;
	for (uint64_t i = 1; i &lt; number; ++i)  // (3)
		if (number % i == 0)
			divisors.append(i);
	return divisors;
}

BOOST_PYTHON_MODULE(divisors)
{
    using namespace boost::python;
    def("find_divisors", findDivisors);  // (4)
}
</pre>

[/snippet]

  1. Include Boost.Python. It must be included before any other header to avoid compilation warning.
  2. The function corresponding to the one we want to replace in Python. It keeps the same signature (takes an integer, returns a list) as the Python original to achieve a &#8220;transparent&#8221; replacement.
  3. Even the logic is exactly the same. Just a few syntax differences. The C++ runtime should make the difference in this case.
  4. Declare the function with “def” (&#8230;hey, it&#8217;s just like Python).

The guide ([http://www.boost.org/doc/libs/1\_59\_0/libs/python/doc/](http://www.boost.org/doc/libs/1_59_0/libs/python/doc/)) has a clear explanation with all the details.

Compiling, sadly, is not so easy, we will have to adapt to your case. Let&#8217;s check a step-by-step example (naturally, this is a single line on the console):

<pre>g++ divisors.cpp			    compile a C++ file, as usual
 -o divisors.so  			    file name: Python demands it is the same as the module name
-I /usr/include/python2.7/	            to include Python's headers (I already set boost in the path)
-l python2.7 -lboost_python -lboost_system  include python, boost
-shared -fPIC -Wl,-export-dynamic           request to create a dynamic library
</pre>

stackoverflow.com will cover the rest. Notice that &#8220;to level the play field&#8221;, I do not use optimization options in g++.

Once our library is in the system path (some place where Python can find it) we can include it in Python:  
[snippet]

<pre>from divisors import find_divisors

def perfect(number):
	divisors = find_divisors(int(number))  # Calls the C++ implementation
	return number == sum(divisors)

… same code as before …

</pre>

[/snippet]

Run time: a bit less than a second. We are witnessing the classic &#8220;80% of time is wasted by 20% of the code&#8221;. The same algorithm is 6 times faster, but the part where we had to deal with low level programming (yes, still C++98!) is just one function. Everywhere else we can still take advantage of Python&#8217;s practicality.

#### Some more opportunities

Boost.Python is not limited to primitive types conversion or adapters to pass Python lists in C++. Here is a selection of &#8220;common&#8221; cases often met when doing “C with classes&#8221;:  
[snippet]

<pre>class ReuseInPython 
{
	public:
		ReuseInPython() {};
		ReuseInPython(int x, const std::string& y) {};
		int instanceVariable;
		static void staticMethod() {};
		void method() {}
};

BOOST_PYTHON_MODULE(oop)
{
    using namespace boost::python;
    class_&lt;ReuseInPython&gt;("implemented_in_CPP")		// (1)
	.def(init&lt;int, std::string&gt;())  // (2)
	.def_readwrite("instance_variable", &ReuseInPython::instanceVariable)  // (3)
	.def("static_method", &ReuseInPython::staticMethod).staticmethod("static_method")  // (4)        
	.def("method", &ReuseInPython::method)  // (5)
    ;
}
</pre>

[/snippet]

  1. Open a class declaration, passing a string with its alias in Python.
  2. Translate the constructor in Python (&#8230;init, does that ring a bell?).
  3. The Python &#8220;translation&#8221; won&#8217;t balk at public instance variables. Here is one.
  4. Only repeat the Python name to expose a static method.
  5. The run-of-the mill, basic instance method.

Once it is compiled (&#8230;sounds easy, but&#8230;) we can use the C++ class in Python:

[snippet]

<pre>from oop import implemented_in_CPP

x = implemented_in_CPP()
y = implemented_in_CPP(3, "hello")
x.instance_variable = 23
implemented_in_CPP.static_method()
x.method()
</pre>

[/snippet]

Boost takes care of converting parameters, return types etcetera. There are options to &#8220;export&#8221; directly STL classes (and more can be defined if something is missing) and for the return type policy (by reference, by copy&#8230;). There are really many options, trust the official guide.

When the going gets tough, Boost keeps going. A sample:

[snippet]

<pre>class Problems
{
	public:
		void print() {
			std::cout &lt;&lt; "cout still works" &lt;&lt; std::endl;
		}

		void exception() {
			throw std::runtime_error("Oh, no!!!");
		}

		void coreDump()	{
			int * nullPointer = 0;
			*nullPointer = 24;
		}
};

BOOST_PYTHON_MODULE(oop)
{
    using namespace boost::python;

    class_&lt;Problems&gt;("Problems")
	.def("print_something", &Problems::print  // Print is a Python keyword.    
	.def("exception", &Problems::exception)
	.def("coreDump", &Problems::coreDump)
    ;
}

</pre>

[/snippet]

The Python &#8220;test-driver&#8221;, with an example of the output:  
[snippet]

<pre>from oop import Problems
p = Problems()
p.print_something()
try:
	p.exception()
except RuntimeError as e:
	print "The C++ code bombed: " + str(e);
p.coreDump()

</pre>

[/snippet]

<pre>cout still works	(1)
The C++ code bombed: Oh, no!!!	(2)
Segmentation fault (core dumped)	(3)
</pre>

  1. Debugging with std::cout is not a recommended practice&#8230; but it works!
  2. Exception are perfectly &#8220;thrown&#8221; to the Python runtime.
  3. &#8230;well, what did you expect?

#### Multithreading

Boost.Python is not the only weapon to tackle problems that demand efficiency.. Multithreading is a common way to improve performance, as good when computing divisors as to mine bitcoins or crack passwords. Here is a C++ class which is about to jump in a Python thread:

[snippet]

<pre>class JobFindDivisors {

	public:
		JobFindDivisors(uint64_t number, uint64_t begin, uint64_t end) :
			number(number), begin(begin), end(end) {}
		
		boost::python::list findDivisors()
		{
			std::cout &lt;&lt; "Start" &lt;&lt; std::endl;

			boost::python::list divisors;
			for (uint64_t i = begin; i &lt; end; ++i)
				 if (number % i == 0)
					divisors.append(i);

			std::cout &lt;&lt; "end" &lt;&lt; std::endl;
			return divisors;
		}

	private:
		uint64_t number;
		uint64_t begin;
 		uint64_t end;
};

BOOST_PYTHON_MODULE(factor)
{
    using namespace boost::python;
    class_&lt;JobFindDivisors&gt;("JobFindDivisors", init&lt;uint64_t, uint64_t, uint64_t&gt;())
	.def("find_divisors", &JobFindDivisors::findDivisors)
    ;
}
</pre>

[/snippet]

The &#8220;JobFindDivisors&#8221; object checks if the numbers between &#8220;begin&#8221; and &#8220;end&#8221; are divisors of &#8220;number&#8221;. We parallelize the problem of finding all the divisors in many “jobs”, dedicating each object to a different interval. No data is shared between jobs, there are no concurrency problems. This is the only advantage of such a solution, but once again let&#8217;s forget about math (and proper software engineering).

The Python call:  
[snippet]

<pre>from threading import Thread
from factor import JobFindDivisors

class Job():									# (1)
	def __init__(self, number, begin, end):
		self.cppJob = JobFindDivisors(number, begin, end)
		self.divisors = []
	
	def __call__(self):
		self.divisors = self.cppJob.find_divisors()

		
def find_divisors_in_parallel(number):			# (2)
	limit = number / 2

	job1 = Job(number, 1, limit)
	job2 = Job(number, limit, number)

	t1 = Thread(None, job1)
	t2 = Thread(None, job2)
	
	t1.start()
	t2.start()
	t1.join()
	t2.join()

	return [job1.divisors, job2.divisors]


if __name__ == "__main__":
	print  find_divisors_in_parallel(223339244); # (3)
</pre>

[/snippet]

  1. Encapsulate the C++ Job to &#8220;keep it simple&#8221;, without exporting a C++ callable.
  2. This method creates 2 jobs, does &#8220;fork and join&#8221; (or, as they say nowadays, &#8220;map and reduce&#8221;), then prints the results.
  3. Factoring any number would do.

The output: do you remember the &#8220;Start&#8221; and &#8220;end&#8221; printouts in the C++ class? After around 8 seconds the computation terminates, with no parallelism whatsoever:

<pre>Start
end
Start
end
[[1L, 2L, 4L, 53L, 106L, 212L, 1053487L, 2106974L, 4213948L, 55834811L], [111669622L]]
</pre>

Working as designed. Python&#8217;s objects are protected by the Global Interpreter Lock (GIL). It is up to the programmer to release it in each thread to &#8220;give way&#8221; to the other threads. The trick is to call pure Python code only when holding the lock.

As usual in C++ we control resources with RAII. The idiom for the GIL is ([https://wiki.python.org/moin/boost.python/HowTo#Multithreading\_Support\_for\_my\_function](https://wiki.python.org/moin/boost.python/HowTo#Multithreading_Support_for_my_function)):  
[snippet]

<pre>class ScopedGILRelease
{
public:
    inline ScopedGILRelease(){
        m_thread_state = PyEval_SaveThread();
    }
    inline ~ScopedGILRelease()    
        PyEval_RestoreThread(m_thread_state);
        m_thread_state = NULL;
    }
private:
    PyThreadState * m_thread_state;
};
</pre>

[/snippet]

Release the lock in the C++ class:  
[snippet]

<pre>boost::python::list findDivisors() {
	ScopedGILRelease noGil = ScopedGILRelease();  // (1)
	std::cout &lt;&lt; "Start" &lt;&lt; std::endl;

	boost::python::list divisors;
	for (uint64_t i = begin; i &lt; end; ++i)
		 if (number % i == 0)
			divisors.append(i);  // (2) Possible core dump!

	std::cout &lt;&lt; "end" &lt;&lt; std::endl;
	return divisors;
}
</pre>

[/snippet]

  1. When this variable goes out of scope, the lock is taken again. Like a &#8220;reversed&#8221; smart pointer.
  2. Here is where we will certainly take a core dump. But only in production.

Do you remember that _&#8220;the trick is to call pure Python code only when holding the lock&#8221;_? Line (2) may do just that, without the lock. You can try to massively grow the list (say erase the “if (number&#8230;” and save all the number in the list). I believe that, maybe (please read the official documents for the real answer!) the Python interpreter must allocate a bigger list, but without the lock all it gets is corrupted memory.

Let&#8217;s encapsulate the parallelizable section in a dedicated scope, saving the numbers in a variable which we do not share with Python:  
[snippet]

<pre>boost::python::list findDivisors()
{
	std::cout &lt;&lt; "Start" &lt;&lt; std::endl;
	std::vector divisorsTemp;
	boost::python::list divisors;
	{
		ScopedGILRelease noGil = ScopedGILRelease();
		for (uint64_t i = begin; i &lt; end; ++i)
			if (number % i == 0)
				divisorsTemp.push_back(i);
	} // noGil goes out of scope, we take the lock again.
	BOOST_FOREACH(uint64_t n, divisorsTemp) {
		divisors.append(n);
	}
	std::cout &lt;&lt; "end" &lt;&lt; std::endl;
	return divisors;
}
</pre>

[/snippet]  
After six and a half seconds (-2 compared with the &#8220;accidentally sequential&#8221; version) we get the expected interleaving (Start Start &#8211; end end). We can invest those 2 seconds to think to a less duck-tape-and-chewing-gum-oriented solution.

This completes the introduction to Boost.Python. Now we know how to &#8220;push&#8221; C++ modules in Python applications either to re-use, either for efficiency reasons. Boost.Python connects the two worlds without sacrificing Python&#8217;s simplicity and without adding constraints to C++, even if some spots do need care. _Above all, from now on we are going to always have the last word in the unavoidable &#8220;Python vs C++&#8221; flame in every forum of the world._

<div id="sdfootnote1">
  <p class="sdfootnote">
    <a class="sdfootnotesym" href="#sdfootnote1anc" name="sdfootnote1sym">1</a>It is true: it takes less time to create a whole program in Python than to fix a single bug in C++.
  </p>
  
  <p>
    Try it. Ready, steady, go:
  </p>
  
  <pre>/usr/include/c++/4.8/bits/stl_map.h:646:7: note: no known conversion for argument 1 from 
‘int’ to ‘std::map&lt;int, std::map&lt;std::basic_string&lt;char&gt;, std::basic_string&lt
;char&gt; &gt; &gt;::iterator {aka std::_Rb_tree_iterator&lt;std::pair&lt;const int, std::map&lt;std::basic_string&lt;char&gt;, std::basic_string&lt;char&gt; &gt; &gt; &gt;}’
</pre>
  
  <p class="sdfootnote">
    /usr/include/c++/4.8/bits/stl_map.h:670:9: note: template<class _InputIterator> void std::map<_Key, _Tp, _Compare, _Alloc>::insert(_InputIterator, _InputIterator) [with _InputIterator = _InputIterator; _Key = int; _Tp = std::map<std::basic_string<char>, std::basic_string<char> >; _Compare = std::less<int>; _Alloc = std::allocator<std::pair<const int, std::map<std::basic_string<char>, std::basic_string<char> > > >
  </p>
</div>