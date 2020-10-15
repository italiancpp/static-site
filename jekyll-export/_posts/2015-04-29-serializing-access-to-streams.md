---
id: 3869
title: Serializing access to Streams
date: 2015-04-29T15:41:54+02:00
author: Marco Foco
layout: post
guid: http://www.italiancpp.org/?p=3869
permalink: /2015/04/29/serializing-access-to-streams/
categories:
  - Hands-on
tags:
  - stream
  - thread
---
<p style="text-align: justify;">
  Last december, I was at <a href="http://meetingcpp.com" target="_blank">Meeting C++</a> in Berlin and I attended &#8211; among others &#8211; the talk <a href="https://www.youtube.com/watch?v=paK38WAq8WY" target="_blank">Multithreading done right?</a> by <em>Rainer Grimm</em>.
</p>

<p style="text-align: justify;">
  In most of the examples, two or more threads were writing to cout using the form:
</p>

[snippet]

<pre>cout &lt;&lt; someData &lt;&lt; "some string" &lt;&lt; someObject &lt;&lt; endl;</pre>

[/snippet]

<p style="text-align: justify;">
  And one of the problems was that data sent from one thread often interrupted another thread, so the output was always messed up.<br /> You can see the problem in this example:
</p>

[compiler]

<pre>#include &lt;iostream&gt;
#include &lt;vector&gt;
#include &lt;thread&gt;

using namespace std;

int main() {
    vector&lt;thread&gt; thr;
    for(int i = 0; i &lt; 10; i++) {
        thr.emplace_back([i]() { cout &lt;&lt; "thread " &lt;&lt; i &lt;&lt; endl; });
    }
    for(int i = 0; i &lt; 10; i++) {
        thr[i].join();
    }
}
</pre>

[/compiler]

<p style="text-align: justify;">
  Which on a test execution produces things like this on CLang:
</p>

<pre>tththrhrereaeadad d  201</pre>

<p style="text-align: justify;">
  And this on Visual Studio:
</p>

<pre style="text-align: justify;">thread 0 thread thread 2 1</pre>

<p style="text-align: justify;">
  I speculated with Marco Arena about possible solutions to the problem, and tried to find a simple and elegant solution in my way back.
</p>

<p style="text-align: justify;">
  I started designing a solution by giving myself some guidelines, here listed in order of importance:
</p>

<ol style="text-align: justify;">
  <li>
    Opt-in: The user doesn&#8217;t have to pay (no performance penalty if the feature is not used).
  </li>
  <li>
    Readability: The user code must be self-explaining.
  </li>
  <li>
    Simplicity of use: I wanted to provide the end-user with something that worked &#8220;out of the box&#8221; requiring as less code as possible.
  </li>
  <li>
    Predictability: I wanted to maintain all the features and feature the standard streams have.
  </li>
  <li>
    Concise solution: I didn&#8217;t want to write tons of code, I&#8217;m too lazy.
  </li>
</ol>

<p style="text-align: justify;">
  An intrusive solution (e.g. adding a mutex to each stream) would have violated the first principle, and quite definitely the fifth too.
</p>

## Wrapping streams

<p style="text-align: justify;">
  The first solution I tried was a simple stream wrapper that locks the stream using <strong>RAII</strong> idiom:
</p>

<p style="text-align: justify;">
  [snippet]
</p>

<pre>class stream_locker {
    ostream& stream;
    lock_guard&lt;mutex&gt; guard;
public:
    stream_locker(ostream &s, mutex &m) : stream(s), guard(m) {}

    template&lt;typename T&gt; stream_locker& operator &lt;&lt; (const T &x) {
        stream &lt;&lt; x;
        return *this;
    }
};</pre>

<p style="text-align: justify;">
  [/snippet]
</p>

<p style="text-align: justify;">
  Here&#8217;s the intended usage:
</p>

[snippet]

<pre>mutex m;
stream_locker(cout, m) &lt;&lt; someData &lt;&lt; "some string" &lt;&lt; someObject &lt;&lt; endl;</pre>

[/snippet]

<p style="text-align: justify;">
  This didn&#8217;t work, because the type is not getting deduced for manipulators like endl (since it&#8217;s an overloaded function).
</p>

<p style="text-align: justify;">
  A solution to this problem could have been manually providing overloads for operator << for manipulators, such as:
</p>

[snippet]

<pre>class stream_locker {
    ...
    stream_locker& operator &lt;&lt; (ostream& (*pf)(ostream&)) {
        stream &lt;&lt; pf;
        return *this;
    }
 };</pre>

[/snippet]

<p style="text-align: justify;">
  The big drawback with this solution was that we needed to provide an overload for every std manipulator type, like the ones declared in <em><strong><ostream></strong></em> and also any other manipulator contained in <em><iomanip></em>. Moreover, any overloaded <em>operator <<</em> in other libraries or user code would have require additional effort (it violates both simplicity and predictability guidelines I gave myself). This was not getting anywhere.
</p>

<p style="text-align: justify;">
  Another possible solution was to return back using the <em>ostream&</em> as soon as possible, like after the first execution of <em>operator <<</em>.
</p>

[snippet]

<pre>class stream_locker {
    ostream& stream;
    lock_guard&lt;mutex&gt; guard;
public:
    stream_locker(ostream &s, mutex &m) : stream(s), guard(m) {}

    template&lt;typename T&gt; ostream& operator &lt;&lt; (const T &x) {
        return stream &lt;&lt; x;
    }
};</pre>

[/snippet]

<p style="text-align: justify;">
  This was slightly better, but it would require, sometimes, to insert empty strings to achieve correct results. Consider the following:
</p>

[snippet]

<pre>stream_locker(cout, m) &lt;&lt; value &lt;&lt; " in octal is " &lt;&lt; oct &lt;&lt; value &lt;&lt; dec &lt;&lt; endl; // OK
stream_locker(cout, m) &lt;&lt; oct &lt;&lt; value &lt;&lt; " in octal is " &lt;&lt; dec &lt;&lt; value &lt;&lt; " in decimal." &lt;&lt; endl; // ERROR
stream_locker(cout, m) &lt;&lt; "" &lt;&lt; oct &lt;&lt; value &lt;&lt; " in octal is " &lt;&lt; dec &lt;&lt; value &lt;&lt; " in decimal." &lt;&lt; endl; // OK

</pre>

[/snippet]

<p style="text-align: justify;">
  The second line won&#8217;t compile, since there&#8217;s no overload for <em>operator <<</em> between a stream_locker and a manipulator like <em>oct</em>. The third will work, because inserting the empty string will result in calling our member <em>operator <<</em>, which now returns an <em>ostream&</em>.
</p>

<p style="text-align: justify;">
  We could definitely solve the problem by making the stream variable public, and changing the usage syntax slightly:
</p>

[snippet]

<pre>class stream_locker {
    lock_guard&lt;mutex&gt; guard;
public:
    ostream& stream;
    stream_locker(ostream &s, mutex &m) : stream(s), guard(m) {}
};

stream_locker(cout, m).stream &lt;&lt; value &lt;&lt; " in octal is " &lt;&lt; oct &lt;&lt; value &lt;&lt; dec &lt;&lt; endl; // OK
stream_locker(cout, m).stream &lt;&lt; oct &lt;&lt; value &lt;&lt; " in octal is " &lt;&lt; dec &lt;&lt; value &lt;&lt; " in decimal." &lt;&lt; endl; // OK
stream_locker(cout, m).stream &lt;&lt; "" &lt;&lt; oct &lt;&lt; value &lt;&lt; " in octal is " &lt;&lt; dec &lt;&lt; value &lt;&lt; " in decimal." &lt;&lt; endl; // OK

</pre>

[/snippet]

<p style="text-align: justify;">
  This works, but the syntax looks horrible.
</p>

## Lifetime of temporaries

<p style="text-align: justify;">
  Wait a second, why does this works? If we are return back to the <em>ostream&</em>, doesn&#8217;t our temporary <em>stream_locker</em> get destroyed right away, releasing the lock?
</p>

<p style="text-align: justify;">
  The answer is no. Any temporary variable created in a sub-expression have its lifetime extended to the &#8220;full-expression&#8221;, which in our case ends at the <em>semicolon</em>.
</p>

<p style="text-align: justify;">
  The stream_locker object is now just behaving exactly like a normal <em>lock_guard<mutex></em>. Can&#8217;t we just use a <em>lock_guard<mutex></em> directly?
</p>

<p style="text-align: justify;">
  [snippet]
</p>

<pre>cout &lt;&lt; lock_guard&lt;mutex&gt;(m) &lt;&lt; ... ;</pre>

[/snippet]

To provide this syntax we just need to overload the _operator <<:_

[snippet]

<pre>inline ostream& operator&lt;&lt;(ostream& out, const lock_guard&lt;mutex&gt; &) {
    return out;
}</pre>

<p style="text-align: justify;">
  [/snippet]
</p>

<p style="text-align: justify;">
  This solution doesn&#8217;t have the drawbacks of wrapper object, since no wrapper is created anywhere. The stream is returned right away, and the lock guard parameter is there for the only sake of including it in the streaming chain.
</p>

<p style="text-align: justify;">
  This definitely looks promising, but the syntax is still a bit too complex. Could we possibly simplify it?
</p>

I would definitely prefer something like:

[snippet]

<pre>cout &lt;&lt; lock_with(m) &lt;&lt; ... ;</pre>

[/snippet]

Basically, lock\_with should return a fresh new lock\_guard locking our mutex m. Something like this:

[snippet]

<pre>template &lt;typename T&gt; lock_guard&lt;T&gt; lock_with(T &mutex) {
    return lock_guard&lt;T&gt;(mutex);
}</pre>

[/snippet]

Unluckily, this doesn&#8217;t work, as you can see yourself by trying to compile the following snippet.

[compiler]

<pre>#include &lt;mutex&gt;
#include &lt;iostream&gt;

using namespace std;

inline ostream& operator&lt;&lt;(ostream& out, const lock_guard&lt;mutex&gt; &) {
    return out;
}

template &lt;typename T&gt; lock_guard&lt;T&gt; lock_with(T &mutex) {
    return lock_guard&lt;T&gt;(mutex);
}

int main() {
    mutex m;
    cout &lt;&lt; lock_with(m) &lt;&lt; "test" &lt;&lt; endl;
}</pre>

[/compiler]

<p style="text-align: justify;">
  Problem is, lock_guard is not copyable. Moving is also deleted, because this class implements the concept of &#8220;scoped ownership&#8221;. Moreover, the constructor taking a mutex is explicit, so we can&#8217;t exploit <em>copy-list-initialization</em> in our solution. Not with that constructor, at least.
</p>

<p style="text-align: justify;">
  As often happens, the solution to my problem was already on <a title="Stack Overflow" href="http://stackoverflow.com/questions/22502606/why-is-stdlock-guard-not-movable" target="_blank">stack overflow</a>, The link explains why lock_guard is not moveable, and it provides a nice workaround, using another constructor, taking two parameters (so we can use <em>copy-list-initialization</em> on that).
</p>

[snippet]

<pre>template &lt;typename T&gt; inline lock_guard&lt;T&gt; lock_with(T &mutex) {
    mutex.lock();
    return { mutex, adopt_lock };
}</pre>

[/snippet]

## The solution

Finally, we can test our original code with the final structure:

[compiler]

<pre>#include &lt;mutex&gt;
#include &lt;vector&gt;
#include &lt;thread&gt;
#include &lt;iostream&gt;

using namespace std;

inline ostream& operator&lt;&lt;(ostream& out, const lock_guard&lt;mutex&gt; &) {
    return out;
}

template &lt;typename T&gt; inline lock_guard&lt;T&gt; lock_with(T &mutex) {
    mutex.lock();
    return { mutex, adopt_lock };
}

int main() {
    mutex m;
    vector&lt;thread&gt; thr;
    for(int i = 0; i &lt; 10; i++) {
        thr.emplace_back([i, &m]() { cout &lt;&lt; lock_with(m) &lt;&lt; "thread " &lt;&lt; i &lt;&lt; endl; });
    }
    for(int i = 0; i &lt; 10; i++) {
        thr[i].join();
    }
}
</pre>

[/compiler]