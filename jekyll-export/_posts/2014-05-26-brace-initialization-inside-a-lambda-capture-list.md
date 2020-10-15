---
id: 3229
title: Brace initialization inside a lambda capture list
date: 2014-05-26T15:24:05+02:00
author: Gian Lorenzo
layout: post
guid: http://www.italiancpp.org/?p=3229
permalink: /2014/05/26/brace-initialization-inside-a-lambda-capture-list/
categories:
  - Hands-on
tags:
  - auto
  - initialized lambda capture
  - initializer-list
---
Mi sono inmbattuto oggi in un problema abbastanza subdolo:  
[compiler]

<pre>#include &lt;iostream&gt;
#include &lt;functional&gt;
#include &lt;vector&gt;
using namespace std;
function&lt;void()&gt; f()
{
    vector&lt;int&gt; v(1000, 0);
    cout &lt;&lt; "v size is: " &lt;&lt; v.size() &lt;&lt; endl;

    return [ v {move(v)} ]() {
        cout &lt;&lt; "inside lambda =&gt; v size is: " &lt;&lt; v.size() &lt;&lt; endl;
    };
}

int main()
{
    f() ();
}</pre>

[/compiler]  
Se eseguite il codice, l&#8217;output del programma è (ammetto con mia sorpresa) il seguente:

**v size is: 1000**  
**inside lambda => v size is: 1**

<p style="text-align: justify;">
  La dimensione di <strong>v</strong> all&#8217;interno della lambda è 1. Ma perchè?<br /> Il problema, come vedremo, non ha nulla a che vedere con le lambda in se ma risiede nel modo in cui <strong>v</strong> viene dedotto nella <em>capture list</em>.
</p>

Dato un vettore cosi definito:  
[snippet]

<pre>vector&lt;int&gt; v(1000, 0); // crea 1000 interi inizializzati a 0</pre>

[/snippet]  
e altri due oggetti (t, u) cosi definiti:  
[snippet]

<pre>vector&lt;int&gt; u{10,20,30};
auto t{10,20,30};</pre>

[/snippet]

<p style="text-align: justify;">
  <strong>u</strong> è un vettore come tutti ce lo aspettiamo, completamente definito ed inizializzato (tramite la uniform initialization) con tre numeri (10, 20, 30), <strong>t</strong> invece è definito tramite <em><strong>auto. </strong></em>Il compilatore deduce <strong>t</strong> come <strong>std::initializer_list<decltype(v)></strong> (= <strong>std::initializer_list<vector<int>></strong>)!.
</p>

<p style="text-align: justify;">
  Ecco perchè <strong>v</strong> catturata dentro la lambda, definita implicitamente come <strong>auto</strong>, ha dimensione 1 (in quel caso abbiamo una std::initializer_list<vector<int>>). Per evitare il problema dobbiamo dunque riscrivere la nostra funzione in questo modo:<br /> [compiler]
</p>

<pre>#include &lt;iostream&gt;
#include &lt;functional&gt;
#include &lt;vector&gt;
using namespace std;

function&lt;void()&gt; f()
{
    vector&lt;int&gt; v(1000, 0);
    cout &lt;&lt; "v size is: " &lt;&lt; v.size() &lt;&lt; endl;

    return [ v = move(v) ]() { //adesso v è un vector&lt;int&gt;
        cout &lt;&lt; "inside lambda =&gt; v size is: " &lt;&lt; v.size() &lt;&lt; endl;
    };
}

int main()
{
    f()();
}</pre>

[/compiler]

<p style="text-align: justify;">
  Finalmente il compilatore dedurrà correttamente <strong>v</strong> nella capture list come un <strong>vector<int></strong>. Con questa modifica il risultato è quello atteso!
</p>

<p style="text-align: justify;">
  Concludendo: <strong>evitate</strong> <strong>di usare la brace initialization all&#8217;interno delle capture list</strong>, ma piuttosto utilizzate la notazione <strong>VAR = EXPR</strong>, perchè <strong>auto + brace initialization</strong> implica che il tipo dedotto sia una std::initializer_list.
</p>

**Biblio**: [Scott Meyers] &#8211; <a title="Item 7 - More Effective C++" href="http://aristeia.com/EC++11-14/parens%20or%20braces%202014-03-18.pdf" target="_blank">Item 7 More Effective C++</a>