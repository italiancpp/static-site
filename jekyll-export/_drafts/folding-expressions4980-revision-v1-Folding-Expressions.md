---
id: 6491
title: Folding Expressions
date: 2016-08-05T23:35:08+02:00
author: marco
layout: revision
guid: http://www.italiancpp.org/2016/08/05/4980-revision-v1/
permalink: /2016/08/05/4980-revision-v1/
---
<p style="text-align: justify;">
  People familiar with the new features C++11 brought to the C++ programming language should know what a <a href="https://en.wikipedia.org/wiki/Variadic_template" target="_blank">variadic template</a> is and why they&#8217;re important. Variadic templates can have a variable number of parameters of any type:
</p>

[snippet]

<pre>template &lt;typename... Types&gt; class tuple;</pre>

[/snippet]

<p style="text-align: justify;">
  This not only brings type safety to the code but also ensures that all the variadic arguments handling is performed at compile-time. Before their introduction, in order to have a template accepting a variable number of template parameters, programmers were used to write verbose code like:
</p>

[snippet]

<pre>template&lt;typename T0&gt;
void function( T0 arg0 );

template&lt;typename T0, typename T1&gt;
void function( T0 arg0, T1 arg1 );

template&lt;typename T0, typename T1, typename T2&gt;
void function( T0 arg0, T1 arg1, T2 arg2 );

template&lt;typename T0, typename T1, typename T2, typename T3&gt;
void function( T0 arg0, T1 arg1, T2 arg2, T3 arg3 );

...</pre>

[/snippet]

<p style="text-align: justify;">
  Template <a href="http://en.cppreference.com/w/cpp/language/parameter_pack" target="_blank">parameter packs</a> went hand-in-hand with variadic templates and together with <a href="http://en.cppreference.com/w/cpp/language/constant_expression" target="_blank">constant expressions</a> they enabled a recursive-like style of coding to create more complex compile-time operations:
</p>

[compiler]

<pre>#include &lt;iostream&gt;
#include &lt;array&gt;

template&lt;size_t... Is&gt; struct seq{};
template&lt;size_t N, size_t... Is&gt;
struct gen_seq : gen_seq&lt;N-1, N-1, Is...&gt;{};
template&lt;size_t... Is&gt;
struct gen_seq&lt;0, Is...&gt; : seq&lt;Is...&gt;{};

template&lt;size_t N1, size_t... I1, size_t N2, size_t... I2&gt;
// Expansion pack
constexpr std::array&lt;int, N1+N2&gt; concat(const std::array&lt;int, N1&gt;& a1, 
        const std::array&lt;int, N2&gt;& a2, seq&lt;I1...&gt;, seq&lt;I2...&gt;){
  return {{ a1[I1]..., a2[I2]... }};
}

template&lt;size_t N1, size_t N2&gt;
// Initializer for the recursion
constexpr std::array&lt;int, N1+N2&gt; concat(const std::array&lt;int, N1&gt;& a1, 
                                       const std::array&lt;int, N2&gt;& a2){
  return concat(a1, a2, gen_seq&lt;N1&gt;{}, gen_seq&lt;N2&gt;{});
}

int main() {
    constexpr std::array&lt;int, 3&gt; a1 = {{1,2,3}};
    constexpr std::array&lt;int, 2&gt; a2 = {{4,5}};

    constexpr std::array&lt;int,5&gt; res = concat(a1,a2);
    for(int i=0; i&lt;res.size(); ++i)
        std::cout &lt;&lt; res[i] &lt;&lt; " "; // 1 2 3 4 5

    return 0;
}</pre>

[/compiler]

<p style="text-align: justify;">
  Exploiting a <a href="http://en.cppreference.com/w/cpp/container/array/operator_at" target="_blank">constexpr overload of the operator[]</a> the code above generates an integer sequence, aggregate-initializes an <em>std::array</em> and concatenates the input arrays at compile time (details of the operations involved are available <a href="http://stackoverflow.com/q/25068481/1938163" target="_blank">at this link</a>).
</p>

<p style="text-align: justify;">
  The integer generation sequence construct was then provided by the standard library itself in C++14 with <a href="http://en.cppreference.com/w/cpp/utility/integer_sequence" target="_blank">std::integer_sequence</a>.
</p>

<p style="text-align: justify;">
  These features allowed new ways to exploit templates, anyway parameter packs could only be used and expanded in a strictly-defined series of contexts. For instance, something like the following wasn&#8217;t allowed:
</p>

[snippet]

<pre>template&lt;typename T&gt;
void printer(T arg) {
    std::cout &lt;&lt; arg &lt;&lt; " ";
}

template&lt;typename... Args&gt;
static void function(Args &&... args) {
    (printer(std::forward&lt;Args&gt;(args)) , ...);
}</pre>

[/snippet]

<p style="text-align: justify;">
  Anyway one of those restricted contexts was <a href="http://en.cppreference.com/w/cpp/language/list_initialization" target="_blank">brace-init-lists</a>, therefore workarounds to have parameter packs be expanded were immediately deployed:
</p>

[snippet]

<pre>template&lt;typename T&gt;
void printer(T arg) {
    std::cout &lt;&lt; arg &lt;&lt; " ";
}

template&lt;typename... Args&gt;
static void function(Args &&... args) {
    // Expand the pack into a brace-init-list while discarding the return
    // values and filling an unused array
    int unusedVar[] = { 0, 
              ( (void) printer(std::forward&lt;Args&gt;(args)), 0) ... };
}</pre>

[/snippet]

* * *

### 

### C++17 ~ fold expressions

<p style="text-align: justify;">
  <a href="https://en.wikipedia.org/wiki/C%2B%2B17" target="_blank">C++17</a>, scheduled by 2017 at the time of writing, will introduce<strong> fold expressions</strong> into play and significantly broaden parameter packs scopes of use (cfr. <a href="http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2014/n4191.html" target="_blank">N4191 paper</a>).
</p>

<p style="text-align: justify;">
  As listed in <a href="http://en.cppreference.com/w/cpp/language/fold" target="_blank">cppreference</a>, at the time of writing, there are four kinds of fold expressions:
</p>

  * Unary right fold 
    <pre>( pack op ... )</pre>

  * Unary left fold 
    <pre>( ... op pack )</pre>

  * Binary right fold 
    <pre>( pack op ... op init )</pre>

  * Binary left fold 
    <pre>( init op ... op pack )</pre>

being their respective expansions:

  * <pre>E_1 op (... op (E_N-1 op E_N))</pre>

  * <pre>((E_1 op E_2) op ...) op E_N</pre>

  * <pre>E_1 op (... op (E_N−1 op (E_N op init)))</pre>

  * <pre>(((init op E_1) op E_2) op ...) op E_N</pre>

<p style="text-align: justify;">
  In binary folds the <em>op</em> operators must be the same and <em>init</em> represents an expression without an unexpanded parameter pack (e.g. the init value for the expanded expression).
</p>

<p style="text-align: justify;">
  With fold expressions writing a printer construct becomes straightforward:
</p>

[compiler]

<pre>#include &lt;iostream&gt;

template&lt;typename F, typename... T&gt;
void for_each(F fun, T&&... args)
{
    (fun (std::forward&lt;T&gt;(args)), ...);
}

int main() {
     for_each([](auto i) { std::cout &lt;&lt; i &lt;&lt; " "; }, 4, 5, 6); // 4 5 6
}</pre>

[/compiler]

<p style="text-align: justify;">
  The sample above uses fold expressions together with the <a href="http://en.cppreference.com/w/cpp/language/operator_other#Built-in_comma_operator" target="_blank">comma operator</a> to create a simple function that calls the provided lambda per each one of the supplied arguments with <a href="http://stackoverflow.com/q/24732926/1938163" target="_blank">perfect forwarding</a>.
</p>

<p style="text-align: justify;">
  A caveat relative to the previous example though: unary right fold expressions and unary left fold expressions applied with the comma operator do yield different expressions but their evaluation order remains the same, e.g.
</p>

[compiler]

<pre>#include &lt;iostream&gt;
#include &lt;memory&gt;

template&lt;typename F, typename... T&gt;
void for_each1(F fun, T&&... args)
{
    (fun (std::forward&lt;T&gt;(args)), ...);
}

template&lt;typename F, typename... T&gt;
void for_each2(F fun, T&&... args)
{
    (..., fun (std::forward&lt;T&gt;(args)));
}

int main()
{
     for_each1([](auto i) { std::cout &lt;&lt; i &lt;&lt; " "; }, 4, 5, 6); // 4 5 6
     std::cout &lt;&lt; std::endl;
     for_each2([](auto i) { std::cout &lt;&lt; i &lt;&lt; " "; }, 4, 5, 6); // 4 5 6
}</pre>

[/compiler]

<p style="text-align: justify;">
  It has to be noted that one of the main reasons fold expressions were accepted as a C++17 proposal is because of their use in <a href="https://en.wikipedia.org/wiki/Concepts_(C%2B%2B)" target="_blank">concepts</a>:
</p>

[snippet]

<pre>template &lt;typename T&gt;
  concept bool Integral = std::is_integral&lt;T&gt;::value;

template &lt;Integral... Ts&gt; // A constrained-parameter pack
  void foo(Ts...);

template &lt;typename... Ts&gt;
  requires Integral&lt;Ts&gt;... // error: requirement is ill-formed
void foo(Ts...);</pre>

[/snippet]

<p style="text-align: justify;">
  The problem boiled down to the same issue we talked of some paragraphs ago: the parameter pack cannot expand in that context. Fold expressions provide an elegant and effective way to deal with this issue instead of resorting to other <em>constexpr</em> machineries to ensure requirements are met:
</p>

[snippet]

<pre>template&lt;typename... Ts&gt;
  requires (Integral&lt;Ts&gt; && ...)
void foo(Ts...);</pre>

[/snippet]

* * *

&nbsp;

References and sources:  
<a href="http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2014/n4191.html" target="_blank">N4191 &#8211; Folding expressions</a>  
<a href="http://en.cppreference.com/" target="_blank">cppreference</a>  
<a href="http://stackoverflow.com/questions/25068481/c11-constexpr-flatten-list-of-stdarray-into-array" target="_blank">constexpr flatten list of std::array into array</a>  
<a href="http://stackoverflow.com/q/25680461/1938163" target="_blank">Variadic template pack expansion</a>  
<a href="http://stackoverflow.com/questions/30819547/why-doesnt-a-left-fold-expression-invert-the-output-of-a-right-fold-expression" target="_blank">Why doesn&#8217;t a left fold expression invert the output of a right fold expression</a>

Thanks to <a href="http://www.italiancpp.org/utenti/marco/" target="_blank">Marco Arena</a> and <a href="http://stackoverflow.com/users/1932150/andy-prowl" target="_blank">Andy</a> for the quick review of this article.