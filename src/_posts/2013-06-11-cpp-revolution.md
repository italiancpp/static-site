---
id: 450
title: C++ Revolution
date: 2013-06-11T11:52:40+02:00
author: marco
layout: post
guid: http://www.italiancpp.org/?p=450
permalink: /2013/06/11/cpp-revolution/
categories: articolo
tags:
  - basic
  - C++11
---
<p style="text-align: justify;">
  Da circa un paio d&#8217;anni l&#8217;interesse per il C++ è aumentato notevolmente. Che sia per la rivoluzione portata dal nuovo standard (<strong>C++11</strong>) o per necessità industriali, &#8211; legate, ad esempio, a scalabilità e performance &#8211; è indubbio che il linguaggio sia profondamente radicato in sistemi che usiamo quotidianamente. Ad esempio <em>MySQL</em>, <em>Oracle</em>, ma anche <em>Office</em>, <em>Photoshop</em> e <em>Facebook</em>. E <a href="http://www.stroustrup.com/applications.html">questo link</a> ne raccoglie molti altri.
</p>

<p style="text-align: justify;">
  Il nuovo standard ha cambiato notevolmente il linguaggio, non solo per aver aggiunto elementi inediti alla libreria, ma anche &#8211; e soprattutto &#8211; per averne mutato lo <strong>stile</strong> e gli <strong>idiomi</strong> più classici. Pensiamo, ad esempio, al tornare un oggetto da una funzione. Nel C++98 non è insolito utilizzare uno stile C-like per evitare di <strong>ritornare per oggetti per valore</strong>. Questo &#8211; a meno di ottimizzazioni del compilatore, come il <em>Return-Value Optimization</em> (<em>RVO</em>) &#8211; è per tenersi lontano da copie potenzialmente costose. Ora, grazie all&#8217;introduzione della move semantics, funzioni di questo genere:
</p>

<code lang="cpp" escaped="true">&lt;br />
void Calculate(vector&lt;HugeType&gt;& result) &lt;br />
{&lt;br />
   // ... fill result&lt;br />
}</code>  
possono essere trasformate in:  
<code lang="cpp" escaped="true">vector&lt;HugeType&gt; Calculate()&lt;br />
{&lt;br />
   vector&lt;HugeType&gt; result;&lt;br />
   // ... fill result&lt;br />
   return result;&lt;br />
}</code>

<p style="text-align: justify;">
  senza incorrere in inutili copie. Questo è garantito dallo standard, senza doversi affidare alle opzioni del compilatore. Più in generale, il C++11 consente di operare con una sintassi chiara su oggetti temporanei o, più in generale, su <strong>RVALUE</strong>.
</p>

<p style="text-align: justify;">
  Ma il C++11 aggiunge anche diverse facilitazioni per migliorare <strong>produttività</strong> e <strong>sintesi</strong>. Come <strong>auto</strong>, per dedurre automaticamente il tipo di una variabile:
</p>

<code lang="cpp" escaped="true">map&lt;string, vector&lt;int&gt;&gt; aMap;&lt;/p>
&lt;p>// C++98&lt;br />
map&lt;string, vector&lt;int&gt;&gt;::iterator it = aMap.begin();&lt;/p>
&lt;p>// C++11&lt;br />
auto it = aMap.begin();</code>  
Oppure il **range-based for loop** per iterare su un range con una sintassi compatta:  
<code lang="cpp" escaped="true">// C++98&lt;br />
for (vector&lt;int&gt;::iterator i = v.begin(); i != v.end(); ++i)&lt;br />
{&lt;br />
   cout &lt;&lt; *i &lt;&lt; " ";&lt;br />
}&lt;/p>
&lt;p>// C++11&lt;br />
for (auto i : v)&lt;br />
{&lt;br />
   cout &lt;&lt; i &lt;&lt; " ";&lt;br />
}</code>  
Le **lambda expressions** facilitano e rendono naturale l&#8217;utilizzo degli algoritmi e dello stile funzionale:  
<code lang="cpp" escaped="true">all_of( begin(vec), end(vec), [](int i){ return (i%2)==0; } );</code>

<p style="text-align: justify;">
  Le <strong>initializer_list</strong> estendono la classica inizializzazione con parentesi graffe delle struct, per essere usata in modo personalizzato:
</p>

<code lang="cpp" escaped="true">class MyVector&lt;br />
{&lt;br />
public:&lt;br />
   MyVector(std::initializer_list&lt;int&gt; list);&lt;br />
   ...&lt;br />
};&lt;/p>
&lt;p>...&lt;/p>
&lt;p>MyVector vec = {1,2,3,4,5};</code>

<p style="text-align: justify;">
  Correlato alle <strong>initializer_list</strong>, anche il fastidioso problema del <a href="http://en.wikipedia.org/wiki/Most_vexing_parse">most vexing parse</a> è stato risolto, con la<strong> uniform initialization</strong>. Il C++11 consente di inizializzare qualsiasi oggetto con una sintassi omogenea:
</p>

<code lang="cpp" escaped="true">struct BasicStruct&lt;br />
{&lt;br />
    int x;&lt;br />
    double y;&lt;br />
};&lt;/p>
&lt;p>struct AltStruct&lt;br />
{&lt;br />
    AltStruct(int x, double y) : x_{x}, y_{y} {}&lt;/p>
&lt;p>private:&lt;br />
    int x_;&lt;br />
    double y_;&lt;br />
};&lt;/p>
&lt;p>BasicStruct var1{5, 3.2};&lt;br />
AltStruct var2{2, 4.3};</code>  
Proseguendo questa panoramica molto generale, è importante ricordare che anche la **libreria standard** ha accolto tante novità. A partire dagli _smart pointers_, deprecando il frainteso _auto_ptr_:  
<code lang="cpp" escaped="true">// C++98&lt;br />
int* anIntPtr = new int(10);&lt;/p>
&lt;p>... &lt;/p>
&lt;p>delete anIntPtr;&lt;/p>
&lt;p>// C++11&lt;br />
unique_ptr&lt;int&gt; anIntPtr( new int(10) ); // will be deleted</code>

<p style="text-align: justify;">
  Passando poi per nuove strutture dati, come gli <strong>unordered container</strong>, le <strong>tuple</strong>, le <strong>forward_list</strong>, &#8230; Anche il supporto alla <strong>metaprogrammazione</strong> è cresciuto, con l&#8217;introduzione di diversi <strong>type_traits</strong> standard e <strong>decltype</strong> per inferire il tipo di un&#8217;espressione.
</p>

E finalmente è possibile scrivere codice **multi-thread** portabile, sfruttando la libreria nativa:  
<code lang="cpp" escaped="true">thread aThread( some_function ); // may be a lambda or any callable obj&lt;br />
thread anotherThread ( another_function );&lt;br />
aThread.join();&lt;br />
anotherThread.join();</code>

<p style="text-align: justify;">
  Questa panoramica è solo una piccoa parte di tutta la storia. Per tutte le novità del C++11 potete consultare, ad esempio, la <a href="http://en.wikipedia.org/wiki/C%2B%2B11">pagina relativa su wikipedia</a>.
</p>

<p style="text-align: justify;">
  Non tutto è però gratuito. Per sfruttare al massimo tutte le innovazioni del C++11 (e tra breve del<strong> C++14</strong>) è necessario comprenderle ed applicarle con disciplina. Non è difficile trovare siti, articoli, tutorial e molto altro su tantissimi aspetti del nuovo standard. Spesso tutto questo volume di informazioni mette in difficoltà chi desidera apprendere gradualmente e non sa da dove iniziare. La prossima sezione raccoglie in modo ordinato alcune delle risorse più importanti ad apprendere e restare aggiornati.
</p>

<p style="text-align: justify;">
  Inoltre, il motivo di questa categoria &#8211; <strong>DOs & DON&#8217;Ts &#8211; </strong>è proprio quello di suggerire al lettore alcune nuove pratiche e idiomi, rimpiazzando il vecchio stile.
</p>

<span style="color: #ffffff;"> </span>

#### C++ Revolution: come inziare

<p style="text-align: justify;">
  Il C++11 ha mosso molti programmatori C++ verso la riscoperta e la rivisitazione del linguaggio; alcuni si sono ritirati perché convinti in un aumento di complessità, mentre altri ne hanno tratto diversi benefici. Negli ultimi anni sono proliferate risorse, articoli, video e materiale divulgativo per apprendere e approfondire molti aspetti del nuovo standard. Questa breve sezione conclusiva vuole raccogliere in modo ordinato risorse utili per approfondire e restare aggiornati, specialmente per chi è ancora indeciso e smarrito.
</p>

<h5 style="text-align: justify;">
  <span style="color: #ffffff;"> </span>
</h5>

<h5 style="text-align: justify;">
  Consulta isocpp.org periodicamente<br /> <span style="color: #ffffff;"> </span>
</h5>

<p style="text-align: justify;">
  Il riferimento ufficiale dello standard &#8211; da circa novembre 2012 &#8211; è <a href="http://www.isocpp.org">isocpp.org</a>. Si tratta dell&#8217;unico catalizzatore ufficiale di risorse e news. Consultare periodicamente questo sito consente di restare aggiornati su eventi, libri, video, articoli e molto altro.
</p>

<h5 style="text-align: justify;">
  <span style="color: #ffffff;"> </span><br /> Considera alcuni testi fondamentali<br /> <span style="color: #ffffff;"> </span>
</h5>

<p style="text-align: justify;">
  I testi che sento di raccomandare a chi vuole conoscere in modo approfondito le novità del C++11 sono i seguenti:
</p>

  * [The C++ Programming Language (4th edition)](http://www.amazon.com/The-Programming-Language-4th-Edition/dp/0321563840/), di Bjarne Stroustrup (la bibbia, aggiornata al C++11)
  * <a style="line-height: 12px;" href="http://www.artima.com/shop/overview_of_the_new_cpp">Overview of the New C++</a><span style="line-height: 12px;">, di Scott Meyers (sono slides dense di contenuti),</span>
  * [The C++ Standard Library (2nd edition)](http://www.josuttis.com/libbook/), di Nicolai Josuttis (attualmente la reference più completa sulla libreria standard, aggiornata al C++11),
  * [C++ Concurrency in Action](http://www.manning.com/williams/), di Anthony Williams (a proposito di multithreading in C++11).

##### <span style="color: #ffffff;"> </span>  
Guarda i video delle ultime conferenze  
<span style="color: #ffffff;"> </span>

Se desiderate guardare qualche video, consiglierei:

  * <span style="line-height: 12px;"><a href="http://channel9.msdn.com/Series/C9-Lectures-Stephan-T-Lavavej-Core-C-">Le lezioni di Stephen T. Lavavej</a> (esistono anche lezioni sulla standard library, <a href="http://www.eventhelix.com/realtimemantra/object_oriented/stl-tutorial.htm">basic </a>& <a href="http://www.eventhelix.com/realtimemantra/object_oriented/stl-tutorial-advanced.htm">advanced</a>),</span>
  * [GoingNative2012](http://channel9.msdn.com/Events/GoingNative/GoingNative-2012) (un&#8217;importante conferenza by Microsoft),
  * [C++ And Beyond 2012](http://channel9.msdn.com/search?term=c%2B%2B+and+beyond+2012) (conferenza di Meyers/Sutter/Alexandrescu)

<h5 style="text-align: justify;">
  <span style="color: #ffffff;"> </span>
</h5>

<h5 style="text-align: justify;">
  Prova diversi compilatori<br /> <span style="color: #ffffff;"> </span>
</h5>

<p style="text-align: justify;">
  Un altro suggerimento è di provare il proprio codice su diversi compilatori, perché non tutti sono 100% compliant col C++11 (ad oggi solo GCC). Grazie ad alcuni <a href="http://www.italiancpp.org/gruppi/compilatori/forum/topic/compilatori-online/">compilatori online</a> è possibile compilare ed eseguire direttamente dal browser.
</p>

<h5 style="text-align: justify;">
  <span style="color: #ffffff;"> </span>
</h5>

<h5 style="text-align: justify;">
  Consulta la categoria DOs & DON&#8217;Ts!<br /> <span style="color: #ffffff;"> </span>
</h5>

<p style="text-align: justify;">
  Come annunciato, l&#8217;obiettivo della nostra categoria <strong>DOs & DON&#8217;Ts</strong> è quello di suggerire nuovi idiomi e pratiche stilistiche, rimpiazzando il vecchio modo di programmare in C++, ove possibile. Preferiamo la sinteticità del codice. Non mancheranno, quindi, snippet con confronti &#8220;ieri/oggi&#8221; e link a codice da compilare e provare direttamente online. Speriamo, poi, di poter discutere con i lettori non solo nei commenti ma anche (e soprattutto) nei vari <a href="http://www.italiancpp.org/gruppi/">gruppi di discussione</a>.
</p>

<p style="text-align: justify;">
  <span style="color: #ffffff;"> </span>
</p>

<p style="text-align: justify;">
  <h5 style="text-align: justify;">
    Chiaramente, invitiamo chiunque voglia contribuire a <a href="http://www.italiancpp.org/press/diventa-un-autore/">farlo</a>!
  </h5>
  
  <p>
    <span style="color: #ffffff;"> </span>
  </p>
  
  <p>
    <span style="color: #ffffff;"> </span>
  </p>