---
id: 6905
title: Philosophy of the C++ Core Guidelines in 4 concepts
date: 2016-10-21T15:27:10+02:00
author: marco
layout: revision
guid: http://www.italiancpp.org/2016/10/21/6885-revision-v1/
permalink: /2016/10/21/6885-revision-v1/
---
A couple of weeks ago I gave a talk at <a href="https://www.microsoft.com/italy/futuredecoded/" target="_blank">FutureDecoded 2016 in Milan</a> where I introduced the <a href="https://github.com/isocpp/CppCoreGuidelines" target="_blank">C++ Core Guidelines</a> and <a href="https://github.com/Microsoft/GSL" target="_blank">Microsoft GSL</a>, and I showed how to check against them with <a href="https://www.nuget.org/packages/Microsoft.CppCoreCheck" target="_blank">CppCoreCheck</a>.

I think it&#8217;s worth summarising the ideas of my talk into this blog post.

Although **GSL** and **CppCoreCheck** are &#8211; in my opinion &#8211; too young for being seamlessly employed in medium/large codebases (especially in mature projects, with a lot of legacy code), many ideas and constructs have been successfully used in the industry for years.

<p style="text-align: justify;">
  The C++ Core Guidelines (and, accordingly, the design of the GSL) is well characterized by 4 basic concepts, that can be valuable in general (and not only speaking about C++):
</p>

  * **Correct-by-Construction**
  * **Fail-Fast**
  * **Turning undefined behavior into well-known expectations**
  * **Using types instead of pointers**

Let me discuss about them briefly.

&nbsp;

#### Correct-by-Construction

<p style="text-align: justify;">
  Making errors happen at compile-time instead of run-time implies that some issues simply do not compile.
</p>

<p style="text-align: justify;">
  Not only is this achievable by adopting particular types, but also by verifying programs with checkers/analyzers that may spot dangerous pieces of code.
</p>

<p style="text-align: justify;">
  An example of Correct-by-Construction methodology is <strong>gsl::not_null</strong> for passing around not-nullable pointers. Constructing an instance of <strong>not_null</strong> by simply passing nullptr is forbidden:
</p>

[snippet]

<pre>void SomeFunction(int& val);

int* ptr = nullptr;
SomeFunction(*ptr); // undefined behavior (crash, if you are lucky)

gsl::not_null&lt;int*&gt; ptr = nullptr; // does not compile</pre>

[/snippet]

<p style="text-align: justify;">
  In general speaking, Correct-by-Construction methodology does not limit to compilation but it extends to program verification and analysis. For this reason some of the C++ Core Guidelines are intended to be automatically checked.
</p>

####  <span style="color: #ffffff;"> </span>

#### Fail-Fast

<p style="text-align: justify;">
  When a problem cannot simply be detected at compile-time, failing as soon as the problem is detected may be helpful. In general, &#8220;the problem is detected&#8221; results in &#8220;an invariant is about to be violated&#8221;.
</p>

<p style="text-align: justify;">
  Failing can result in different actions, like:
</p>

<ul style="text-align: justify;">
  <li>
    throwing an exception
  </li>
  <li>
    aborting the program
  </li>
</ul>

<p style="text-align: justify;">
  The GSL supports the &#8220;do-nothing&#8221; option as well, that is mandatory for <strong>gradual adoption</strong>.
</p>

<p style="text-align: justify;">
  Failing policies can be set with preprocessor macros:
</p>

<p style="text-align: justify;">
  &#8211; GSL_TERMINATE_ON_CONTRACT_VIOLATION (default): std::terminate will be called<br /> &#8211; GSL_THROW_ON_CONTRACT_VIOLATION: <strong>gsl::fail_fast</strong> exception will be thrown<br /> &#8211; GSL_UNENFORCED_ON_CONTRACT_VIOLATION: nothing happens
</p>

<p style="text-align: justify;">
  Fail-fast means also refusing to construct an object &#8211; while an object is being constructed &#8211; in case an invariant is about to break.<br /> Let&#8217;s go back to the previous example. What happens when not_null is constructed with a pointer that is null? That is:
</p>

[snippet]

<pre>int* ptr = nullptr;
not_null&lt;int*&gt; nptr = ptr;
SomeFunction(*nptr);</pre>

[/snippet]

<p style="text-align: justify;">
  Does <em>nptr</em> make sense to exist? Not at all! For this reason, <strong>not_null</strong>&#8216;s constructor fails according to the choosen policy (that may be throwing an exception).
</p>

<span style="color: #ffffff;"> </span>

#### Turning undefined behavior into well-known expectations

Consider again the very first example:

[snippet]

<pre>void SomeFunction(int& i);

int* ptr = nullptr;
SomeFunction(*ptr); // undefined behavior</pre>

[/snippet]

<p style="text-align: justify;">
  Dereferencing a nullptr results in <strong>undefined behavior</strong>, that is basically &#8220;the compiler can do everything&#8221;. Sometimes &#8220;everything&#8221; means it may call <em>SomeFunction</em> with a reference to a <em>broken</em> int value (a dangling or invalid reference).
</p>

<p style="text-align: justify;">
  Suppose now we turn the function&#8217;s signature into:
</p>

[snippet]

<pre>void SomeFunction(not_null&lt;int*&gt; i);</pre>

[/snippet]

And suppose we set the failure policy to **GSL\_THROW\_ON\_CONTRACT\_VIOLATION**.

<p style="text-align: justify;">
  What&#8217;s changed? In case <em>ptr</em> is nullptr, we have <strong>turned undefined behavior into throwing an exception</strong>.
</p>

<p style="text-align: justify;">
  Another solution would have been checking the pointer. However this should be done everywhere SomeFunction is used.
</p>

<p style="text-align: justify;">
  Using <strong>not_null</strong> is also convenient to express <strong>intent</strong>: callers of SomeFunction know they have to guarantee that the parameter is not null.
</p>

<p style="text-align: justify;">
  Why not using a reference? A reference just <strong>shouldn&#8217;t</strong> be null, instead <strong>gsl::not_null</strong> will never be.
</p>

When I see **not_null**, I see a **barrier** which a nullptr can not go beyond.

<p style="text-align: justify;">
  not_null can also be adoperated to ensure that a function returns a valid pointer-like instance:
</p>

[snippet]

<pre>gsl::not_null&lt;shared_ptr&lt;IService&gt;&gt; CreateService(...params...);</pre>

[/snippet]

<p style="text-align: justify;">
  <em>CreateService</em> ensures the returned shared_ptr will be always valid, otherwise the invariant is broken and a failure is expected.
</p>

<p style="text-align: justify;">
  Here we need to be fair and report that:
</p>

  * some people just don&#8217;t expect that such functions fail (they expect these functions always return valid pointers and never throw);
  * others expect either a valid pointer or a failure.

<p style="text-align: justify;">
  The latter point is formally more correct, indeed creating <strong>not_null</strong> may result in failing due to breaking the invariant.
</p>

<p style="text-align: justify;">
  The same idea of not_null is in <a href="https://github.com/dropbox/nn/" target="_blank">Dropbox&#8217;s nn</a> (a difference with gsl::not_null is that <strong>nn</strong> supports move semantics).
</p>

Another example of Fail-Fast is **Bounds-Checking**:

[snippet]

<pre>int arr[] = {1,2,3};
int idx = 4;
arr[idx] = 10; // undefined behavior</pre>

[/snippet]

<p style="text-align: justify;">
  Again, we can turn undefined behavior into an exception (or something else) just by using a bounds-checked type. In the next section we&#8217;ll learn what GSL proposes for doing that.
</p>

#### <span style="color: #ffffff;"> </span>

#### Using types instead of pointers

In my talk <a href="http://www.italiancpp.org/wp-content/uploads/2016/05/Marco-Arena-With-great-C-comes-great-responsibility.pdf" target="_blank">Great C++ comes with great responsibility</a>, I pronounced for the first time the term **Factotum Pointers**, referring to pointers whose usage can vary, depending on the context. Take this example:

[snippet]

<pre>void Function(int* p);</pre>

[/snippet]

What is the intent of p? It may be:

  * pointer to a single element
  * pointer to a dynamically-allocated sequence of elements
  * pointer to a statically-allocated sequence of elements
  * a position that can be changed/incremented/subtracted

Moreover, we don&#8217;t know if:

  * p owns a resource that should be deleted after Function is called
  * Function allows p to be null

<p style="text-align: justify;">
  If they can, clients of <em>Function</em> generally look into the implementation to figure out how <em>p</em> is used and what happens at the <strong>boundaries</strong> of the function call.
</p>

<p style="text-align: justify;">
  By adopting rules we can avoid such problems. For example, we know that using a raw pointer to pass around ownership is dangerous and unclear, so we usually agree on employing smart pointers, containers or custom wrappers, that are safer and clearer alternatives.
</p>

<p style="text-align: justify;">
  What about the other problems? Let&#8217;s try finding solutions for them.
</p>

<p style="text-align: justify;">
  <strong>What about expressing that p may not be null?</strong> We have references and we have just met <strong>gsl::not_null</strong>.
</p>

<p style="text-align: justify;">
  <strong>What about the difference between a single element and a sequence?</strong> Here we need something new. The C++ Core Guidelines project proposes:
</p>

<li style="text-align: justify;">
  never use pointers to represent and pass arrays
</li>
<li style="text-align: justify;">
  never do pointer arithmetic directly
</li>
<li style="text-align: justify;">
  access static arrays only with constant indexes, or via bounds-checked functions (e.g. gsl::at)
</li>
<li style="text-align: justify;">
  pass around naked ranges/sequences as <strong>span</strong>
</li>

<p style="text-align: justify;">
  We can turn the rules above into one: <strong>pointers should only represents nullable references to single objects</strong>.
</p>

**span<T>** is the alternative to represent both contiguous ranges and C-style arrays.

The previous example is changed to:

[snippet]

<pre>int arr[] = {1,2,3};
span&lt;int&gt; sp = arr;
int idx = 4;
sp[idx] = 10; // bounds-checked</pre>

[/snippet]

GSL actually provides also:

[snippet]

<pre>gsl::at(arr, idx); // bounds-checked</pre>

[/snippet]

<p style="text-align: justify;">
  That is more succint and works also with <em>std::array</em>, <em>std::initializer_list</em> and containers providing both <em>operator[]</em> and <em>size()</em>. And it is declared constexpr.
</p>

<p style="text-align: justify;">
  <strong>Using span is clearly a tradeoff</strong>, not only because bounds-checking may be expensive in some cases, but also because it&#8217;s not true that using span over pointers is seamless. Reasons vary and I have read lots of different opinions online and I have discussed with many people about that topic.
</p>

<p style="text-align: justify;">
  I give you one example I deal with every day at work (I think you do as well). You know, it&#8217;s common to express functions taking many arrays of the same length (and possibly of different types) as many pointers and only one number for size. For example:
</p>

[snippet]

<pre>void twofft(float data1*, float data2*. float fft1*, float fft2*, long len);</pre>

[/snippet]

(Often, arrays can have different types).

<p style="text-align: justify;">
  According to the Guidelines, each array should be replaced with span. Suppose copying and replicating the length for each span is not an issue (when in doubt, just measure). Suppose also that bounds-checking and other invariants check are fine:
</p>

[snippet]

<pre>void twofft(span&lt;float&gt; data1, span&lt;float&gt; data2. span&lt;float&gt; fft1, span&lt;float&gt; fft2);</pre>

[/snippet]

<p style="text-align: justify;">
  In my opinion, <strong>the worst loss is about the interface of the function</strong>.
</p>

<p style="text-align: justify;">
  We should be pragmatic and admit that the current standard &#8220;de facto&#8221; for passing around sequences of the same length is the single number at the end. It&#8217;s well-known by C and C++ programmers. Using span we totally lose that information.
</p>

<p style="text-align: justify;">
  In an ideal world I would express the requirement through <strong>contracts</strong>, but we don&#8217;t have them yet into the language.
</p>

<p style="text-align: justify;">
  We may set up an <strong>expectation</strong> (e.g. using <strong>GSL&#8217;s Expects</strong>). However, this is still an <strong>implementation detail</strong> and not really an interface constraint.
</p>

<p style="text-align: justify;">
  You can even code your own type &#8220;multiple spans, sharing the same length&#8221; (<strong>tied_span</strong>, or something else). I did it and I tried to use it with other people. These are the feedbacks I got:
</p>

<li style="text-align: justify;">
  &#8220;we have lost the name of the parameters&#8221;;
</li>
<li style="text-align: justify;">
  &#8220;declaring such <em>tied_span</em> is too complicated with more than 2 arrays of different type&#8221;;
</li>
<li style="text-align: justify;">
  &#8220;I go back to pointers&#8221;.
</li>

<p style="text-align: justify;">
  <em>span</em> is simply not enough for covering <strong>all</strong> scenarios we have, especially with legacy code (search GSL and C++ Core Guidelines repositories for issues about span and you&#8217;ll find many more).
</p>

<p style="text-align: justify;">
  <span style="color: #ffffff;">  </span>
</p>

### Checking the C++ Core Guidelines

<p style="text-align: justify;">
  An ambitious part of the Guidelines project aims to define kind of <strong>standard static analysis</strong>, that means showing exactly the same warning on every analysis tool that analyzes the same piece of code.
</p>

Checkable guidelines are subdivided into three **Safety Profiles**:

  * Type
  * Bounds
  * Lifetime

<p style="text-align: justify;">
  The daring aim of the project is to guarantee that an aspect of a program is safe as far as each guideline of the corresponding profile is correctly observed.
</p>

**Type safety** guarantees no use of a location as a T that contains an unrelated U.

**Bounds safety** guarantees no accesses beyond the bounds of an allocation.

**Lifetime safety** ensures no use of invalid or deallocated allocations.

<p style="text-align: justify;">
  <a href="https://www.nuget.org/packages/Microsoft.CppCoreCheck" target="_blank">CppCoreCheck</a> is a Microsoft extension of Visual Studio&#8217;s static analysis, which &#8211; experimentally &#8211; checks the code against these profiles.
</p>

<p style="text-align: justify;">
  I have used CppCoreCheck for many small activities, including:
</p>

  * Training
  * Legacy code analysis
  * Developing toy projects

<p style="text-align: justify;">
  Although &#8211; in my opinion &#8211; we are far away to use it on industrial medium/large codebases, I have found it useful as a tool that helps detect what the C++ Core Guidelines call the attention to. For example, whenever the checker complains with messages like:
</p>

> No array to pointer decay

<p style="text-align: justify;">
  You can decide to replace the pointer with <em>span</em> (or something else) or not. The tool enables us to start playing with these concepts directly by showing examples onto our code instead of fake examples.
</p>

### <span style="color: #ffffff;"> </span>

### GSL for annotating code

<p style="text-align: justify;">
  In programming we use types and functions to make abstractions on data. We make abstractions to express intents and to explicitly commit to decisions.
</p>

<p style="text-align: justify;">
  ddd
</p>

<p style="text-align: justify;">
  How many times do we cast types into others? Are we always on the safe side?
</p>

<p style="text-align: justify;">
  For example, casting a <em>double</em> into an <em>int</em> may cause information loss. This behavior is sometimes expected, other times is not. On large codebases, it&#8217;s extremely useful to <strong>quickly spot all the places where we perform such possibly lossy conversions</strong>.
</p>

<p style="text-align: justify;">
  In a ideal world, I would like seeing a warning whenever those <strong>narrowing conversions</strong> are done &#8211; regardless the cast is C-style or C++-style. Then a decision has to be made: just &#8220;marking&#8221; the cast as acceptable, or expecting a failure if the conversion really loses information &#8211; according to the <strong>Fail-Fast</strong> methodology.
</p>

GSL provides both the alternatives:

[snippet]

<pre>auto cmd = gsl::narrow_cast&lt;int&gt;(doubleParameter); // just annotated

auto cmd = gsl::narrow&lt;int&gt;(doubleParameter); // throw gsl::narrowing_error if cast is lossy</pre>

[/snippet]

<p style="text-align: justify;">
  <strong>gsl::narrow</strong> throws an exception (regardless of the failure policy) if the cast loses information (e.g. 1.5 into an int results in losing 0.5). Instead, <strong>gsl::narrow_cast</strong> only annotates the caset as &#8220;acceptable&#8221;.
</p>

<p style="text-align: justify;">
  Annotation is an explicit commit to a decision. Writing <em>narrow_cast</em> we are explicitly expressing that we &#8220;accept&#8221; that narrow cast, that we made a decision on that statement.
</p>

<p style="text-align: justify;">
  Both <strong>gsl::narrow</strong> and <strong>gsl::narrow_cast</strong> result useful in reviewing and refactoring code.
</p>

<p style="text-align: justify;">
  <strong>gsl::not_null</strong> is another clear example of annotation. It express a pointer-like type that cannot be null.
</p>

### <span style="color: #ffffff;">  </span>

### Manual Suppression

<p style="text-align: justify;">
  C++ Core Guidelines are intended for a <strong>gradual adoption</strong>. It&#8217;s impossible to embrace the whole set of guidelines in large codebases, especially at the current state of the project.
</p>

<p style="text-align: justify;">
  When we need to tell the analyzer not to check some blocks of code, we can use the attribute <strong>[[gsl::suppress]]</strong>. For example:
</p>

[snippet]

<pre>void many_arrays_operation(const double* in1, const double* in2, double* out, int size)
{
   for (int i = 0; i &lt;= size; i++)
   {
      [[gsl::suppress(bounds.1)]] // performance critical code (cannot do bounds-checking)
      {
          out[i] = in1[i] + in2[i]; 
      }

   }
}</pre>

[/snippet]

<p style="text-align: justify;">
  We suppress the rule 1 of the bounds profile in that particular scope. We are really specific, so it will be easier to fix the problem in the future.
</p>

### <span style="color: #ffffff;"> </span>

### Conclusions

<p style="text-align: justify;">
  I think all of us have been applying many of the idioms and the constructs described in the C++ Core Guidelines. After all, this project comes from the C++ ecosystem.
</p>

<p style="text-align: justify;">
  What this project tries to do is basically &#8220;constraining C++&#8221; when many options to do the same thing exist. The project tries to give a single and consistent vision on how to do things in C++, especially for making C++ development safer and more maintainable. Clearly, <strong>it&#8217;s impossible to reach an agreement with everyone</strong>. What is feasible, instead, is formulating a solid and consistent set of principles that covers a great part of the possible cases.
</p>

<p style="text-align: justify;">
  One example is about pointers. The C++ Core Guidelines say: <strong>use pointers only to represent nullable references to single objects </strong>and <strong>don&#8217;t do pointer arithmetic</strong>. This means stop passing arrays as pointers. Can we <strong>always</strong> embrace this rule? I say no, pragmatically. So, what should we do?
</p>

<p style="text-align: justify;">
  <p style="text-align: justify;">
    However, I think it&#8217;s precious to have a look at the main concepts and constructs.
  </p>