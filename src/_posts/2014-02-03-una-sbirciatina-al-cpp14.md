---
id: 2614
title: Una sbirciatina al C++14
date: 2014-02-03T12:40:45+01:00
author: marco
layout: post
guid: http://www.italiancpp.org/?p=2614
permalink: /2014/02/03/una-sbirciatina-al-cpp14/
categories: Articoli
tags:
  - C++14
---
<p style="text-align: justify;">
  Il <strong>C++14</strong> è il nome informale della prossima revisione dello standard C++ ISO/IEC che potrebbe essere ufficializzata quest&#8217;anno. La bozza approvata dal comitato ISO &#8211; <a title="N3797" href="http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2013/n3797.pdf" target="_blank">N3797</a> &#8211; è stata pubblicata il 15 Maggio 2013.
</p>

<p style="text-align: justify;">
  In questo breve articolo vediamo alcune delle features più interessanti già disponibili su Clang (ogni argomento ha il link al relativo paper/draft). Vi diamo la possibilità di provare <strong>alcuni</strong> esempi direttamente nell&#8217;articolo. Qualsiasi autore può utilizzare nei propri articoli questi &#8220;snippet compilabili&#8221;, quindi se avete voglia di scrivere un articolo del genere <a title="Diventa autore!" href="http://www.italiancpp.org/articoli/diventa-un-autore/" target="_blank">fatevi sotto</a>!
</p>

<h3 style="text-align: justify;">
  <a href="http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2013/n3649.html" target="_blank">Generic lambdas</a> & <a href="http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2013/n3648.html" target="_blank">initialized capture</a>
</h3>

<p style="text-align: justify;">
  Scrivendo una lambda, quante volte  vi siete chiesti: &#8220;ma perché il compilatore non deduce il tipo dei parametri automaticamente?!&#8221; Per esempio in un for_each:
</p>

<p style="text-align: justify;">
  [snippet]
</p>

<pre>vector&lt;int&gt; v;
for_each(begin(v), end(v), [](int i) {
   cout &lt;&lt; i &lt;&lt; endl;
});</pre>

<p style="text-align: justify;">
  [/snippet]
</p>

<p style="text-align: justify;">
  Per prima cosa il compilatore sa quale tipo ci va, ma non solo: la stessa lambda (a parte il parametro) potrebbe essere riutilizzata altrove, per stampare qualsiasi oggetto che supporti l&#8217;operator<<(ostream&):
</p>

<p style="text-align: justify;">
  [snippet]
</p>

<pre>auto printer = [](string s) {
   cout &lt;&lt; s &lt;&lt; endl;
};</pre>

<p style="text-align: justify;">
  [/snippet]
</p>

<p style="text-align: justify;">
  In C++14 è possibile creare delle <strong>lambda generiche</strong> (dette anche <em>polimorfe</em>), tramite <strong>auto</strong>:
</p>

<p style="text-align: justify;">
  [compiler]
</p>

<pre>#include &lt;iostream&gt;

using namespace std;

int main()
{
   auto printer = [](auto value) {
      cout &lt;&lt; "PRINTING: " &lt;&lt; value &lt;&lt; endl;
   };

   printer(10);
   printer("hello");
}</pre>

<p style="text-align: justify;">
  [/compiler]
</p>

<p style="text-align: justify;">
  Un lambda <em>stateless</em> (con cattura &#8220;vuota&#8221;), proprio come nel C++11, si può castare ad un puntatore a funzione <strong>appropriato</strong>:
</p>

<p style="text-align: justify;">
  [snippet]
</p>

<pre>auto printer = [](auto value) {
    cout &lt;&lt; value &lt;&lt; endl;
};

void(*printIntFn)(int) = printer;</pre>

<p style="text-align: justify;">
  [/snippet]
</p>

<p style="text-align: justify;">
  Un altro limite delle lambda riguarda la cattura che è consentita solo per copia e per reference, escludendo, di fatto, una cattura &#8220;by-move&#8221;. Si possono adottare alcuni workaround &#8211; come bind oppure nascondere una move sotto una copy &#8211; ma si tratta, appunto, solo di trucchi per eludere un limite del linguaggio.
</p>

<p style="text-align: justify;">
  Nel C++14 la sintassi della capture-list permette delle vere e proprie <strong>inizializzazioni</strong> di variabili (questa nuova caratteristica è chiamata, infatti, <em>initialized lambda capture</em>):
</p>

<p style="text-align: justify;">
  [compiler]
</p>

<pre>#include &lt;iostream&gt;
#include &lt;memory&gt;
#include &lt;vector&gt;
#include &lt;numeric&gt;
using namespace std;

int main()
{
    unique_ptr&lt;int&gt; ptr {new int{10}};

    auto closure = [ptr = move(ptr)]{
        cout &lt;&lt; "From closure: " &lt;&lt; *ptr &lt;&lt; endl;
    };

    closure();

    if (ptr) // is ptr valid?
        cout &lt;&lt; "ops...move didn't work..." &lt;&lt; endl;

    vector&lt;int&gt; v{1,2,3,4,5};

    auto printSum = [sum = accumulate(begin(v), end(v), 0)]{
        cout &lt;&lt; "Sum is: " &lt;&lt; sum &lt;&lt; endl;
    };

    printSum();
}</pre>

<p style="text-align: justify;">
  [/compiler]
</p>

<p style="text-align: justify;">
  Suggeriamo di non abusare di questa notazione&#8230;Non è il caso di scrivere tutto il codice tra [ ] 🙂
</p>

<p style="text-align: justify;">
  Notevole di questa sintassi è il poter creare delle closure con &#8220;full ownership&#8221;: nell&#8217;esempio di prima, se avessimo introdotto uno shared_ptr la lambda avrebbe in qualche modo condiviso la proprietà del puntatore con lo scope in cui è definita. Al contrario, muovendo uno unique_ptr dentro la lambda si sta completamente trasferendo la proprietà del puntatore all&#8217;interno della stessa. Non mancano casi in cui questa nuova sintassi farà davvero comodo, specialmente in ambito multi-thread.
</p>

<h3 style="text-align: justify;">
  <a href="http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2012/n3386.html" target="_blank">Return type deduction for normal functions</a>
</h3>

<p style="text-align: justify;">
  In C++11 il tipo di ritorno di una lambda viene dedotto automaticamente se questa è composta di una sola espressione. Nel C++14 la deduzione del tipo di ritorno di una lambda viene estesa anche per casi i più complicati.
</p>

<p style="text-align: justify;">
  Ma non solo: la deduzione automatica è abilitata anche per le funzioni ordinarie, tramite due diverse notazioni:
</p>

<p style="text-align: justify;">
  [snippet]
</p>

<pre>// auto-semantics
auto func() {...}

// decltype-semantics
decltype(auto) func() {...}</pre>

<p style="text-align: justify;">
  [/snippet]
</p>

<p style="text-align: justify;">
  Nel primo caso il tipo di ritorno è dedotto seguendo la semantica di <strong>auto</strong> (e.g. &-qualifiers eliminati), nel secondo quella di <strong>decltype</strong>. Vediamo un esempio con auto:
</p>

<p style="text-align: justify;">
  [compiler]
</p>

<pre>#include &lt;iostream&gt;
#include &lt;type_traits&gt;
#include &lt;vector&gt;
using namespace std;

template&lt;typename T&gt;
auto sum(T&& a, T&& b)
{
    return a+b;
}

int main()
{
    cout &lt;&lt; "Summing stuff:" &lt;&lt; endl;
    cout &lt;&lt; sum(1, 2) &lt;&lt; endl;
    cout &lt;&lt; sum(1.56, 3.66) &lt;&lt; endl;
    cout &lt;&lt; sum(string{"hel"}, string{"lo"}) &lt;&lt; endl;
}</pre>

<p style="text-align: justify;">
  [/compiler]
</p>

<p style="text-align: justify;">
  Uno scenario nel quale questa notazione sarebbe poco appropriata (l&#8217;esempio <span style="text-decoration: underline;">non compila</span>, di fatto):
</p>

<p style="text-align: justify;">
  [compiler]
</p>

<pre>#include &lt;memory&gt;
using namespace std;

struct Base {};
struct Derived : Base {};

shared_ptr&lt;Base&gt; share_ok(int i) // ok
{
    if (i)
        return make_shared&lt;Base&gt;();
    return make_shared&lt;Derived&gt;();
}

auto share_ops(int i) // ops
{
    if (i)
        return make_shared&lt;Base&gt;();
    return make_shared&lt;Derived&gt;();
}

int main()
{
    auto shared1 = share_ok(1);
    auto shared2 = share_ops(1); 
}</pre>

<p style="text-align: justify;">
  [/compiler]
</p>

<p style="text-align: justify;">
  In ogni caso, prima di dare linee guida o suggerimenti stilistici, attendiamo di utilizzare questa feature in produzione.
</p>

<p style="text-align: justify;">
  Ed ecco <strong>auto</strong> e <strong>decltype(auto)</strong> a confronto:
</p>

<p style="text-align: justify;">
  [compiler]
</p>

<pre>#include &lt;iostream&gt;
#include &lt;type_traits&gt;
#include &lt;vector&gt;
using namespace std;

vector&lt;int&gt; v{1,2,3,4};

decltype(auto) getDecltype(size_t index)
{
    return v[index];
}

auto getAuto(size_t index)
{
    return v[index];
}

int main()
{
    auto val = getAuto(0); 
    auto anotherVal = getDecltype(1);
    auto& ref = getDecltype(0);
    ref += 10; // aka: v[0] += 10;
    cout &lt;&lt; "copied v[0] = " &lt;&lt; val &lt;&lt; endl;
    cout &lt;&lt; "copied v[1] = " &lt;&lt; anotherVal &lt;&lt; endl;

    cout &lt;&lt; "final vector: [ ";
    for (auto i : v)
        cout &lt;&lt; i &lt;&lt; " "; 
    cout &lt;&lt; "]" &lt;&lt; endl;
}</pre>

<p style="text-align: justify;">
  [/compiler]
</p>

<p style="text-align: justify;">
  Questo facile esempio mostra che, nonostante l&#8217;operator[] di un vector riporti una reference, la semantica di deduzione di <strong>auto</strong> vuole che i ref-qualifiers siano eliminati. Per questo <strong>getAuto()</strong> restituisce un int (per copia). Viceversa, con <strong>decltype(auto)</strong>, vengono utilizzate le regole deduttive di <strong>decltype</strong> che preservano i qualificatori (e quindi il fatto che operator[] riporti una reference). Per una spiegazione più accurata di auto e decltype vi consigliamo <a title="C++ auto and decltype Explained" href="http://thbecker.net/articles/auto_and_decltype/section_01.html" target="_blank">questo articolo</a> di Thomas Becker. Provate a giocare con l&#8217;esempio direttamente nell&#8217;articolo. Se siete soliti scrivere codice generico, troverete molto utili queste due novità!
</p>

<h3 style="text-align: justify;">
  <a href="http://isocpp.org/files/papers/N3651.pdf" target="_blank">Variable templates</a>
</h3>

<p style="text-align: justify;">
  Nel C++11 non c&#8217;è modo di parametrizzare una costante direttamente con i template, come invece è possibile per classi e funzioni. Generalmente vengono utilizzati dei workarounds come classi al cui interno sono definite una serie di static constexpr (e.g. vedi <strong>numeric_limits</strong>).
</p>

<p style="text-align: justify;">
  Dal C++14 è consentito definire delle <strong>constexpr variable templates</strong> (o solo <strong>variable templates</strong>), come ad esempio:
</p>

<p style="text-align: justify;">
  [compiler]
</p>

<pre>#include &lt;iostream&gt;
#include &lt;iomanip&gt;
using namespace std;

template&lt;typename T&gt;
constexpr T pi = T(3.1415926535897932385);

template&lt;typename T&gt;
T areaOfCircle(T r) 
{
    return pi&lt;T&gt; * r * r;
}

int main()
{
    cout &lt;&lt; setprecision(10);
    cout &lt;&lt; "PI double = " &lt;&lt; pi&lt;double&gt; &lt;&lt; endl;
    cout &lt;&lt; "PI float = " &lt;&lt; pi&lt;float&gt; &lt;&lt; endl;
    cout &lt;&lt; "Area double = " &lt;&lt; areaOfCircle(1.5) &lt;&lt; endl;
    cout &lt;&lt; "Area float = " &lt;&lt; areaOfCircle(1.5f) &lt;&lt; endl;
}</pre>

<p style="text-align: justify;">
  [/compiler]
</p>

<p style="text-align: justify;">
  La nostra carrellata del C++14 è completa. Non esitate a lasciare un commento con le vostre impressioni. E se un commento non vi basta, scrivete un intero articolo! <a title="Diventa un autore" href="http://www.italiancpp.org/articoli/diventa-un-  autore" target="_blank">Contattateci</a> e vi aiuteremo a pubblicare il vostro &#8220;pezzo&#8221; su <strong>++it</strong> &#8211; i mini-compilatori sono disponibili per tutti!
</p>