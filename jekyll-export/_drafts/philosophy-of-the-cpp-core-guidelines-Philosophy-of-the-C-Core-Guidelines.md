---
id: 6885
title: Philosophy of the C++ Core Guidelines
date: 2017-02-16T15:59:24+01:00
author: marco
layout: post
guid: http://www.italiancpp.org/?p=6885
permalink: /?p=6885
evolve_sidebar_position:
  - default
evolve_full_width:
  - 'no'
evolve_page_title:
  - 'yes'
evolve_page_breadcrumb:
  - 'yes'
evolve_widget_page:
  - 'no'
evolve_slider_position:
  - default
evolve_slider_type:
  - 'no'
wp_sponsor_link_behaviour:
  - "0"
categories:
  - Hands-on
tags:
  - C++ Core Guidelines
  - GSL
---
<p style="text-align: justify;">
  Last October I gave a talk at <a href="https://www.microsoft.com/italy/futuredecoded/" target="_blank">FutureDecoded 2016 in Milan</a> where I introduced the <a href="https://github.com/isocpp/CppCoreGuidelines" target="_blank">C++ Core Guidelines</a> and <a href="https://github.com/Microsoft/GSL" target="_blank">Microsoft GSL</a>, and I also showed how to use <a href="https://www.nuget.org/packages/Microsoft.CppCoreCheck" target="_blank">CppCoreCheck</a> for checking C++ code against a part of such guidelines.
</p>

<p style="text-align: justify;">
  First of all I introduced some basic concepts then most of the time was spent on live demos. I think it&#8217;s worth summarising the main ideas of the first part, showing also some examples.
</p>

<p style="text-align: justify;">
  Although the <strong>GSL</strong> and <strong>CppCoreCheck</strong> are &#8211; in my opinion &#8211; too young for being seamlessly employed in medium/large codebases (especially in mature projects, with a lot of legacy code), many ideas and constructs have been successfully used in the industry for years.
</p>

<p style="text-align: justify;">
  The <strong>GSL</strong> provides things such as <strong>span</strong> &#8211; that resambles <a href="http://www.boost.org/doc/libs/1_61_0/libs/multi_array/doc/user.html#sec_views" target="_blank">boost::array_view</a> &#8211; and <strong>not_null</strong> &#8211; that is similar to <a href="https://github.com/dropbox/nn" target="_blank">Dropbox&#8217;s nn</a>.
</p>

<p style="text-align: justify;">
  The main purpose of the <strong>GSL</strong> is to be a self-contained small library providing missing concepts from the C++ Standard which will enable developers to easily embrace the <a href="https://github.com/isocpp/CppCoreGuidelines" target="_blank">C++ Core Guidelines</a>.
</p>

<p style="text-align: justify;">
  The aim of the guidelines is to help people to use <em>modern</em> <em>C++</em> effectively (&#8220;modern C++&#8221; means C++1z). &#8220;[Ideally,] Any style guide should point to the C++ Core Guidelines. Companies actively involved in the project (that is open) are working on helping/aligning with this, while leaving any company-specific rules they may need as their own addenda.&#8221; (from a private conversation with <em>Herb Sutter</em>).
</p>

<p style="text-align: justify;">
  In my opinion, the C++ Core Guidelines and the design of the GSL are characterized by 4 basic concepts that <strong>can </strong>be valuable in general (and not only speaking about C++):
</p>

  * **Correct-by-Construction**
  * **Fail-Fast**
  * **Turning undefined behavior into well-known expectations**
  * **Using types instead of pointers**

The purpose of this post is to present them briefly.

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
  In general speaking, Correct-by-Construction methodology does not limit to compilation but it extends to program verification and analysis. For this reason some of the C++ Core Guidelines are intended to be <strong>automatically checked</strong>. We&#8217;ll turn back on this point later.
</p>

####  <span style="color: #ffffff;"> </span>

#### Fail-Fast

<p style="text-align: justify;">
  When a problem cannot simply be detected at compile-time, the idea here is to fail as soon as possible. In general, a problem is detected also when an <strong>invariant</strong> is violated.
</p>

<p style="text-align: justify;">
  Failure policies may differ. For instance:
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
  The GSL supports the &#8220;do-nothing&#8221; option as well, mandatory to <strong>gradually adopt </strong>these concepts.
</p>

<p style="text-align: justify;">
  Failing policies are set as preprocessor macros:
</p>

<p style="text-align: justify;">
  &#8211; GSL_TERMINATE_ON_CONTRACT_VIOLATION (default): std::terminate will be called<br /> &#8211; GSL_THROW_ON_CONTRACT_VIOLATION: <strong>gsl::fail_fast</strong> exception will be thrown<br /> &#8211; GSL_UNENFORCED_ON_CONTRACT_VIOLATION: nothing happens
</p>

<p style="text-align: justify;">
  Fail-fast means also refusing to construct an object &#8211; while an object is being constructed &#8211; in case a check on any invariant fails.<br /> Let&#8217;s go back to the previous example. What happens when <strong>not_null</strong> is constructed with a pointer that is null? That is:
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
  Dereferencing a nullptr results in <strong>undefined behavior</strong>, that is basically &#8220;the compiler can do everything&#8221;. Sometimes &#8220;everything&#8221; means it may call <em>SomeFunction</em> with a reference to a <em>broken</em> int value (e.g. a dangling reference).
</p>

<p style="text-align: justify;">
  Suppose now we turn the function&#8217;s signature into:
</p>

[snippet]

<pre>void SomeFunction(not_null&lt;int*&gt; i);</pre>

[/snippet]

And suppose we set the failure policy to **GSL\_THROW\_ON\_CONTRACT\_VIOLATION**.

<p style="text-align: justify;">
  What&#8217;s changed? In case <em>ptr</em> is nullptr, we have <strong>turned that undefined behavior into throwing an exception</strong>.
</p>

<p style="text-align: justify;">
  Another solution would have been checking the pointer. However this should be done everywhere SomeFunction is used and also, <em>SomeFunction</em> <strong>does not express any expectation on the pointer,</strong> from the client point of view.
</p>

<p style="text-align: justify;">
  On the last point, instead, using <strong>not_null</strong> is also convenient to express <strong>intent</strong>: callers of <em>SomeFunction</em> know they <strong>have to</strong> guarantee that the parameter is not null.
</p>

<p style="text-align: justify;">
  <strong>Why not using a reference?</strong> A reference just <strong>shouldn&#8217;t</strong> be null, instead <strong>gsl::not_null</strong> will never be. During my talk I showed that in the following code <em>UseService </em>was called:
</p>

[snippet]

<pre>void UseService(Service& s)
{
   s.Do();
}

Service s = GetService(); // return nullptr
useService(*s);</pre>

[/snippet]

<p style="text-align: justify;">
  Replacing <em>Service&</em> with <em>not_null<Service*>,</em> we never got into <em>UseService</em> as far as <em>s</em> was nullptr. I imagine <strong>not_null</strong> as a <strong>barrier</strong> that nullptr just cannot break.
</p>

<p style="text-align: justify;">
  <strong>not_null</strong> can also be adoperated in <em>factory functions</em> to ensure and express a valid returned pointer-like instance:
</p>

[snippet]

<pre>gsl::not_null&lt;shared_ptr&lt;IService&gt;&gt; CreateService(...params...);</pre>

[/snippet]

<p style="text-align: justify;">
  <em>CreateService</em> ensures the returned <em>shared_ptr</em> will be always valid.
</p>

<p style="text-align: justify;">
  Here we need to be fair and say that:
</p>

  * some people just don&#8217;t expect that such functions fail (they expect that these functions always return valid pointers and never throw);
  * others expect either a valid pointer or a failure.

<p style="text-align: justify;">
  The latter point is formally more correct, indeed creating <strong>not_null</strong> may result in breaking the invariant and then failing according to the policy.
</p>

<p style="text-align: justify;">
  We find something similar to <em>not_null</em> is in <a href="https://github.com/dropbox/nn/" target="_blank">Dropbox&#8217;s nn</a> (a big difference with <em>gsl::not_null</em> is that <strong>nn</strong> supports <em>move semantics</em>).
</p>

Another example of Fail-Fast is **Bounds-Checking**:

[snippet]

<pre>int arr[] = {1,2,3};
int idx = 4;
arr[idx] = 10; // undefined behavior</pre>

[/snippet]

<p style="text-align: justify;">
  (Suppose idx is really taken at runtime &#8211; otherwise the compiler is smart enough to flag a warning).
</p>

<p style="text-align: justify;">
  Again, we can turn undefined behavior into an exception (or something else) just by using a <strong>bounds-checked type</strong>. In the next section we&#8217;ll learn what GSL proposes for that.
</p>

#### <span style="color: #ffffff;"> </span>

#### Using types instead of pointers

<p style="text-align: justify;">
  In my talk <a href="http://www.italiancpp.org/wp-content/uploads/2016/05/Marco-Arena-With-great-C-comes-great-responsibility.pdf" target="_blank">Great C++ comes with great responsibility</a>, I pronounced for the first time the term <strong>Factotum Pointers</strong> referring to pointers whose intent is unclear and depends on the context of usage. Take this example:
</p>

[snippet]

<pre>void Function(int* p);</pre>

[/snippet]

What is the intent of p? It may be:

  * pointer to a single element;
  * pointer to a dynamically-allocated sequence of elements;
  * pointer to a statically-allocated sequence of elements;
  * a position that can be changed/incremented/subtracted.

Moreover, we don&#8217;t know if:

  * p owns a resource that should be deleted after Function is called;
  * Function allows p to be null.

<p style="text-align: justify;">
  If they can, clients of <em>Function</em> generally look into the implementation to figure out how <em>p</em> is used and what happens at the <strong>boundaries</strong> of the function call.
</p>

<p style="text-align: justify;">
  <strong>By adopting rules</strong> we can avoid such problems. For example, we know that using a raw pointer to pass around ownership is dangerous and unclear, so we usually agree on employing smart pointers, containers or custom wrappers, that are safer and clearer alternatives.
</p>

<p style="text-align: justify;">
  What about the other problems? Let&#8217;s try finding solutions for them.
</p>

<p style="text-align: justify;">
  <strong>What about expressing that p may not be null?</strong> We have references and we have just met <strong>gsl::not_null</strong>.
</p>

<p style="text-align: justify;">
  <strong>What about the difference between a single element and a sequence?</strong> Here we need something new. The C++ Core Guidelines project states:
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

**span<T>** is the alternative to represent both contiguous ranges and C-style arrays. It&#8217;s similar to <a href="http://www.boost.org/doc/libs/1_61_0/libs/multi_array/doc/user.html#sec_views" target="_blank">boost::array_view</a>.

The previous example will turn into:

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
  <strong>Using span is clearly a tradeoff</strong>, not only because bounds-checking may be expensive under certain constraints, but also because it&#8217;s not true that using span over pointers is seamless. Reasons vary. I have read lots of different opinions online and I have discussed with many people about that topic.
</p>

<p style="text-align: justify;">
  I give you one example I deal with every day at work (I think you do as well). You know, it&#8217;s common to express functions taking <strong>many arrays of the same length</strong> (and possibly of different types) as many pointers and<strong> only one</strong> number for the size. For example:
</p>

[snippet]

<pre>void twofft(float data1*, float data2*. float fft1*, float fft2*, long len);</pre>

[/snippet]

(Often, arrays have different types).

<p style="text-align: justify;">
  According to the Guidelines, each array should be replaced with span. Suppose copying and replicating the length for each span is not an issue (when in doubt, measure). Suppose also that bounds-checking and other invariants check are ok and we can afford them. We have:
</p>

[snippet]

<pre>void twofft(span&lt;float&gt; data1, span&lt;float&gt; data2. span&lt;float&gt; fft1, span&lt;float&gt; fft2);</pre>

[/snippet]

<p style="text-align: justify;">
  What about the size of each span? Now, do you expect them all to have the same size? I don&#8217;t know, honestly.
</p>

<p style="text-align: justify;">
  In my opinion, the worst side effect was that now we lost the (weak) requirement on the size of those pointers. Although that requirement was not enforced, the programmer knows it. It&#8217;s a common way of doing.
</p>

<p style="text-align: justify;">
  We should be pragmatic and admit that the current standard &#8220;de facto&#8221; for passing around sequences of the same length is the single number at the end. It&#8217;s well-known by C and C++ programmers. You cannot just barge in on that and break it. At least, not with legacy code.
</p>

<p style="text-align: justify;">
  In an ideal world I would use <strong>span + contracts:</strong>
</p>

<p style="text-align: justify;">
  [snippet]
</p>

<pre>void twofft(span&lt;float&gt; data1, span&lt;float&gt; data2, ... etc) [[ensures: data1.size() == data2.size()]];</pre>

<p style="text-align: justify;">
  [/snippet]
</p>

<p style="text-align: justify;">
  That&#8217;s what I think many people and I can afford more easily.
</p>

<p style="text-align: justify;">
  We may set up an <strong>expectation</strong> (e.g. using <strong>GSL&#8217;s Expects</strong>). However, this is still an <strong>implementation detail</strong> and not really an interface constraint. I don&#8217;t want to dig into the implementation (and many times I just cannot).
</p>

<p style="text-align: justify;">
  You can even code your own type &#8220;multiple spans, sharing the same length&#8221; (<strong>tied_span</strong>, or something else). I tried to use that construct with other people and the feedbacks I got were:
</p>

<li style="text-align: justify;">
  &#8220;we have lost the name of the parameters&#8221;;
</li>
<li style="text-align: justify;">
  &#8220;declaring such <em>tied_span</em> is too complicated with more than 2 arrays of different type&#8221;;
</li>
<li style="text-align: justify;">
  &#8220;I go back to pointers&#8221;. (That&#8217;s just a failure)
</li>

<p style="text-align: justify;">
  <em>span</em> is simply not enough for covering <strong>all</strong> scenarios we have, especially with legacy code (search GSL and C++ Core Guidelines repositories for issues about span and you&#8217;ll find many more). That&#8217;s just one, but searching for <em>issues</em> on GitHub you&#8217;ll find other concerns on span (some of them are basically old/known concerns regarding <strong>boost::array_view</strong>).
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
  <a href="https://www.nuget.org/packages/Microsoft.CppCoreCheck" target="_blank">CppCoreCheck</a> is a Microsoft extension of Visual Studio&#8217;s static analysis, which &#8211; experimentally &#8211; checks the code against these profiles (you can find similar concepts in <a href="http://clang.llvm.org/extra/clang-tidy/" target="_blank">Clang Tidy</a>).
</p>

<p style="text-align: justify;">
  I have used CppCoreCheck for many small activities, including:
</p>

  * Training other people and myself
  * Legacy code analysis
  * Toy projects development support/analysis

<p style="text-align: justify;">
  Although &#8211; in my opinion &#8211; we are far away to use it on industrial medium/large codebases, I have found it useful as a tool that helps detect what the C++ Core Guidelines call the attention to. For example, whenever the checker complains with messages like:
</p>

> No array to pointer decay

<p style="text-align: justify;">
  You can decide to replace the pointer with <em>span</em> (or something else) or not. Moreover, the tool enables us to start learning/considering/understanding these concepts by <strong>starting from our code instead of looking at fake and childish examples</strong>. That&#8217;s really precious.
</p>

### <span style="color: #ffffff;"> </span>

### GSL & &#8220;type-aware annotations&#8221;

<p style="text-align: justify;">
  How many times do we cast types into others? Are we always on the safe side?
</p>

<p style="text-align: justify;">
  For example, casting a <em>double</em> into an <em>int</em> may lose information (that&#8217;s called narrowing). This behavior is sometimes expected, other times is not. <strong>Quickly spot all the places where we perform such possibly lossy conversions </strong>is somehow useful.
</p>

<p style="text-align: justify;">
  In a ideal world, I would like seeing a warning whenever those <strong>narrowing conversions</strong> are done &#8211; regardless the cast is C-style or C++-style. Then we have to decide if either &#8220;marking&#8221; the cast as acceptable, or expecting a failure if the conversion really loses information &#8211; according to the <strong>Fail-Fast</strong> methodology.
</p>

The former has more information that just a cast, because we explicitly commit to such decision. The latter is a bit more radical, but it makes sense in some cases.

GSL provides both the alternatives:

[snippet]

<pre>auto cmd = gsl::narrow_cast&lt;int&gt;(doubleParameter); // just annotated

auto cmd = gsl::narrow&lt;int&gt;(doubleParameter); // throw gsl::narrowing_error if cast is lossy</pre>

[/snippet]

<p style="text-align: justify;">
  <strong>gsl::narrow</strong> throws an exception (regardless of the failure policy) if the cast loses information (e.g. 1.5 into an int results in losing 0.5). Instead, <strong>gsl::narrow_cast</strong> only <strong>annotates</strong> the caset as &#8220;acceptable&#8221;.
</p>

<p style="text-align: justify;">
  Annotation is like an explicit commit to a decision. When we write <em>narrow_cast</em> we are explicitly expressing that we &#8220;accept&#8221; that cast, even if it casts away some information. We made a decision on that statement.
</p>

<p style="text-align: justify;">
  I have been using constructs similar to both <strong>gsl::narrow</strong> and <strong>gsl::narrow_cast</strong> for years and they resulted useful in reviewing and refactoring code many times.
</p>

<p style="text-align: justify;">
  Recently, I found it useful to adoperate a utility similar to narrow to just
</p>

<p style="text-align: justify;">
  <strong>gsl::not_null</strong> is another example of annotation because it makes clear that a pointer-like object cannot be null:
</p>

[snippet]

<pre>void UseService(Service* s); // is it safe to pass nullptr?

void UseService(not_null&lt;Service*&gt; s); // cannot pass nullptr</pre>

[/snippet]

<p style="text-align: justify;">
  As usual in (strong-typed) programming, the more we use the type system, the more we are expressive.
</p>

<p style="text-align: justify;">
  Being expressive is also convenient for static analyzers that can spot issues by looking at the boundaries of the function calls.
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
  However, I think it&#8217;s precious to have a look at the main concepts and constructs.
</p>