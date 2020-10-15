---
id: 1201
title: Modern range-based iteration
date: 2013-09-23T09:29:47+02:00
author: marco
layout: post
guid: http://www.italiancpp.org/?p=1201
permalink: /2013/09/23/modern-range-based-iteration/
categories:
  - Hands-on
tags:
  - basic
  - input iterator
  - iterazione
  - range
---
<p style="text-align: justify;">
  La libreria standard è basata sul concetto di <strong>iteratore</strong>,  ovvero un oggetto che &#8220;punta&#8221; ad un elemento di un range e che consente di &#8220;spostarsi&#8221; (iterare) attraverso gli altri elementi, imitando per quanto possibile la sintassi usata con i puntatori. Tutti gli iteratori sono classificati in base ad alcune categorie, all&#8217;incirca a seconda che permettano lettura e/o scrittura, e a seconda di che tipi di spostamento supportano (questa spiegazione va oltre lo scopo dell&#8217;articolo &#8211; <em>basic &#8211;</em> ma per saperne di più è possibile partire da <a href="http://www.cplusplus.com/reference/iterator/">qui</a>). In particolare, un vero <strong>puntatore</strong> è un caso particolare di iteratore:
</p>

<code lang="cpp" escaped="true">int arr[] = {1,2,3,4};&lt;br />
int* ptr = &arr[1]; // ptr punta a 2&lt;br />
++ptr; // ptr punta a 3&lt;br />
*ptr = 10;&lt;br />
// arr è ora {1,2,10,4}</code>

<p style="text-align: justify;">
  Questo articolo tratta alcune <strong>linee guida</strong> a proposito di <strong>iterazione su range</strong>. Un range è inteso come due <strong>iteratori </strong>che rappresentano l&#8217;inzio e la fine dell&#8217;intervallo di elementi sui quali iterare. Non si tratta, però, di iteratori qualsiasi bensì di quelli che lo standard definisce come <a href="http://www.cplusplus.com/reference/iterator/InputIterator/" target="_blank">InputIterator</a>. Questo categoria di iteratori è la più semplice e consente di scorrere serialmente gli elementi in &#8220;sola lettura&#8221; (solo input &#8211; a &#8220;scrivere&#8221; sono gli <strong>OutputIterator</strong>). Per essere più rigorosi (ma non troppo), un <strong>InputIterator</strong> è un qualsiasi tipo di oggetto che supporta almeno queste operazioni:
</p>

  * <span style="line-height: 12px;"><strong>value-semantics</strong> (ha un costruttore di copia, un operator= e un distruttore pubblici)</span>
  * si può testare **l&#8217;uguaglianza** (operator==, operator!=)
  * può essere **dereferenziato** (*it, it->member), ma il risultato va trattato come se fosse di sola lettura (si può scrivere _auto x = *it_; ma non _*it = 10_ come sopra)
  * può essere **incrementato di 1** (con operator++)

<p style="text-align: justify;">
  Altre operazioni sono implicate (ad esempio,  la funzione <strong><em>swap</em></strong>) o supportate con certe limitazioni (il costruttore di default). Si noti però che non si parla mai della sequenza di oggetti &#8220;puntati&#8221;, che infatti potrebbe addirittura&#8230; non esistere! Un InputIterator potrebbe &#8220;fingere&#8221; di iterare su elementi che vengono creati al volo nell&#8217;istante in cui si de-referenzia (si vedrà un esempio più avanti). Secondo lo standard, de-referenziando due copie dello stesso iteratore non necessariamente si ottiene lo stesso valore!
</p>

<p style="text-align: justify;">
  Comunque, l&#8217;idea fondamentale è che <em>è necessario definire alcune funzioni anziché ereditare da una classe base</em>. Qualsiasi classe che &#8220;si comporta&#8221; come un InputIterator è allora considerata un InputIterator. Si tratta del classico approccio della <strong>generic programming</strong>, meglio formalizzato nei <a href="http://en.wikipedia.org/wiki/Concepts_(C%2B%2B)" target="_blank">Concepts</a>.
</p>

<p style="text-align: justify;">
  Spesso ci troviamo a scrivere cicli su strutture dati, ad esempio su vettori o liste. La libreria standard fornisce diversi algoritmi che internamente operano come dei cicli. Il più semplice è il <em>for_each</em>, che dati due InputIterator Begin/End esegue una certa funzione per ogni elemento nel range <strong>[Begin, End)</strong>.
</p>

Un container può essere &#8220;descritto&#8221; da un range **[Begin, End)** e per questo definisce le quattro funzioni:

  * **begin()**, **cbegin()** (ovvero const-begin, che produce un iteratore di sola lettura)
  * **end()**, **cend()** (ovvero const-end)

<p style="text-align: justify;">
  <strong>begin()</strong> è, chiaramente, un InputIterator che punta al primo elemento del container, <strong>end()</strong>, invece, punta subito fuori dal range (<em>one-past-the-last-element</em>). Ci sono diverse motivazioni per questa scelta architetturale, ma (semplificando) è possibile pensare che questa sia in linea col classico pattern:
</p>

<code lang="cpp" escaped="true">for (int i=0; i!=END; ++i) // END escluso&lt;br />
...</code>

<p style="text-align: justify;">
  con i = END il ciclo si arresta, quindi l&#8217;ultima iterazione è proprio con i = END &#8211; 1.
</p>

<p style="text-align: justify;">
  <span style="text-decoration: underline;">Nota</span>: gli iteratori ritornati dalle funzioni begin/end di un container sono generalmente più avanzati di un InputIterator (ad esempio possono supportare contemporaneamente input e output), ma tutti comunque ne supportano le specifiche.
</p>

<span style="text-align: justify;">Supponiamo, ora, di avere una classe </span><strong style="text-align: justify;">Plot</strong> <span style="text-align: justify;">che supporta un </span><strong style="text-align: justify;">replot</strong><span style="text-align: justify;">:</span>  
<code lang="cpp" escaped="true">class Plot&lt;br />
{&lt;br />
public:&lt;br />
   ...&lt;br />
   void replot();&lt;br />
   ...&lt;br />
};</code>  
dato un vector di Plot potremmo ridisegnare ogni plot con un banale ciclo, sfruttando le funzioni sopra citate:  
<code lang="cpp" escaped="true">vector&lt;Plot&gt; plots;&lt;br />
for (auto it = plots.begin(); it != plots.end(); ++it)&lt;br />
{&lt;br />
   i-&gt;replot();&lt;br />
}</code>  
Ma potremmo usare anche un for_each:  
<code lang="cpp" escaped="true">for_each(plots.begin(), plots.end(), [](Plot& plot)&lt;br />
{&lt;br />
   plot.replot();&lt;br />
});</code>  
Cosa scegliere e perché? Ci sono almeno quattro buone ragioni per le quali scegliere un algoritmo invece di scrivere un ciclo:

**1) Efficienza:** un algoritmo è potenzialmente vincente perché:

<li style="text-align: justify;">
  <span style="line-height: 12px;">evita di ripetere alcune chiamate (e.g. <strong>plots.end()</strong>), mantenendo il codice compatto,</span>
</li>
<li style="text-align: justify;">
  gli implementatori delle STL possono specializzare particolari algoritmi in base al container, massimizzando le performance,
</li>
<li style="text-align: justify;">
  (generalmente) gli algoritmi sono sofisticati e implementati rispettando lo stato dell&#8217;arte (e.g. sort). anche algoritmi apparentemente banali, come potrebbe essere &#8220;visitare tutti gli elementi&#8221; possono essere ottimizzati e nascondere  gradi di sofisticazione insospettabili!
</li>

<p style="text-align: justify;">
  <strong>2) Correttezza:</strong> scrivere un ciclo a mano è error-prone, richiede di controllare la validità del range in cui si itera e potenzialmente fa perdere più tempo a scrivere controlli che non a implementare il core del proprio algoritmo.
</p>

<p style="text-align: justify;">
  <strong>3)</strong> <strong>Manutenibilità</strong>: è più facile mettere mano su un codice che usa algoritmi standard, documentati e provati, oppure su listati completamente scritti a mano (e più verbosi)? Generalmente è molto più semplice leggere e comprendere un codice che utilizza algoritmi standard ed uno dei motivi principali è che questi ultimi sono ben documentati (e <em>i loro nomi hanno un significato che esprime <span style="text-decoration: underline;">l&#8217;intento</span> del programmatore</em>). Essi rappresentano un vero e proprio &#8220;vocabolario&#8221; con cui comunicare (ad esempio nel proprio team) e dal quale attingere funzionalità già pronte.
</p>

<p style="text-align: justify;">
  <strong>4) Astrazione</strong>: non sempre occorre avere a che fare con gli iteratori. Con un ciclo scritto a mano è necessario utilizzarli, dereferenziarli, &#8230; Con un algoritmo, invece, è possibile utilizzare direttamente l&#8217;oggetto &#8220;puntato&#8221;, come nell&#8217;esempio sopra, dove accediamo ad un&#8217;istanza di business, <strong>Plot</strong>, e non ad un iteratore.
</p>

<p style="text-align: justify;">
  Primo <span style="text-decoration: underline;"><strong><em>DO</em></strong></span> della giornata: <span style="color: #2945a4;"><strong>ove possibile,</strong> <strong>preferire l&#8217;utilizzo degli algoritmi ai cicli scritti a mano</strong>.</span>
</p>

<p style="text-align: justify;">
  Questo primo DO è generale, non da applicarsi sol al C++. Veniamo al nocciolo di questo post. <strong>Iterare</strong> <strong>su un range: </strong><strong>quali sono le nuove linee guida</strong>?
</p>

<p style="text-align: justify;">
  All&#8217;inizio abbiamo detto che ogni container può essere descritto da un range <strong>(Begin. End]</strong>. Abbiamo anche fatto vedere come utilizzare le funzioni begin/end per iterare su un container. Il range <strong>(Begin, End]</strong> è del tipo:
</p>

<code lang="cpp" escaped="true">vector&lt;int&gt; vec {1,2,3,4,5};&lt;br />
auto first = vec.begin();&lt;br />
auto one_past_last = vec.end();&lt;br />
// [first, one_past_last) "descrive" vec</code>

<p style="text-align: justify;">
  L&#8217;unico problema è che questo approccio non è abbastanza generico. Ad esempio non può essere applicato agli <strong>array C-style</strong> (e.g. int arr[]). Come rimediare? Il <strong>C++11</strong> introduce le <strong>funzioni non-membro</strong> begin/end, con un overload per gli array C-style. Oltre a supportare gli array, queste due funzioni danno uniformità e coerenza, promuovendo l&#8217;estensibilità (è possibile creare delle specializzazioni per i propri container) e incrementando l&#8217;incapsulamento. Le non-member functions begin/end sono fatte così:
</p>

<code lang="cpp" escaped="true">// C++11&lt;br />
template&lt; class C &gt;&lt;br />
auto begin( C& c ) -&gt; decltype(c.begin());&lt;/p>
&lt;p>// C++11&lt;br />
template&lt; class C &gt;&lt;br />
auto begin( const C& c ) -&gt; decltype(c.begin());&lt;/p>
&lt;p>// C++11 - overload per gli array C&lt;br />
template&lt; class T, size_t N &gt;&lt;br />
T* begin( T (&array)[N] );</code>

<p style="text-align: justify;">
  <span style="text-decoration: underline;"><em><strong>DO</strong></em></span>: <span style="color: #2945a4;"><strong>Utilizzare le funzioni non-membro begin(x) e end(x) invece di x.begin() e x.end().</strong></span>
</p>

<code lang="cpp" escaped="true">for_each( begin(vec), end(vec), ... ) // C++11</code>  
E se avessimo bisogno di **cbegin()** e **cend()** ? Il **C++14** introduce anche queste due funzioni non-membro, sfuggite al C++11:  
<code lang="cpp" escaped="true">// C++14&lt;br />
template&lt; class C &gt;&lt;br />
auto cbegin( const C& c ) -&gt; decltype(std::begin(c));&lt;/p>
&lt;p>// C++14&lt;br />
template&lt; class C &gt;&lt;br />
auto cend( const C& c ) -&gt; decltype(std::end(c));</code>  
<span style="text-decoration: underline;"><em><strong>DO</strong></em></span>: <span style="color: #2945a4;"><strong>[C++14] Utilizzare le funzioni non-membro cbegin(x) e cend(x) invece di x.cbegin() e x.cend().</strong></span>

<p style="text-align: justify;">
  Concludiamo questo primo articolo a proposito di iterazione su range con una seconda novità del C++11: il <strong>range-based for loop (RBFL)</strong>. Questo costrutto equivale ad utilizzare un <strong><em>for_each</em></strong> su un container. Stesse garanzie di performance ma più compattezza:
</p>

<code lang="cpp" escaped="true">// C++11&lt;br />
for (const auto& elem : vec)&lt;br />
{&lt;br />
   cout &lt;&lt; elem &lt;&lt; " ";&lt;br />
}&lt;/p>
&lt;p>// quando vec è una variabile locale, è come scrivere&lt;br />
for_each(begin(vec), end(vec), [](const T& elem)&lt;br />
{&lt;br />
   cout &lt;&lt; elem &lt;&lt; " ";&lt;br />
});</code>  
La sintassi è semplice e probabilmente già vista in altri linguaggi. Da notare la possibilità di usare **auto**. Chiaramente, anche qui, il concetto di iteratore è celato e si opera direttamente sugli oggetti contenuti nel vettore.

<p style="text-align: justify;">
  <strong><span style="text-decoration: underline;"><em>DO</em></span></strong>: <span style="color: #2945a4;"><strong>Utilizzare il range-based for loop al posto del for_each, è più semplice e compatto.</strong></span>
</p>

<p style="text-align: justify;">
  Il RBFL opera su strutture x che supportino il concetto di <strong>iterazione</strong>, ovvero:
</p>

  * <span style="line-height: 12px;">abbiano le funzioni<strong> membro</strong> x.<strong>begin() </strong>e<strong> </strong>x.<strong>end()</strong>, <em>oppure,</em></span>
  * abbiano le funzioni **non-membro** **begin(x)** e **end(x)** (trovate con ADL &#8211; Argument Dependent Lookup), _oppure,_
  * per le quali esistono le specializzazioni di **std::begin(x)** e **std::end(x)**.

Le funzioni devono ritornare degli **InputIterator **(in realtà il requisito è più &#8220;leggero&#8221;, come vedremo nel prossimo esempio. Maggiori dettagli <a href="http://en.cppreference.com/w/cpp/language/range-for" target="_blank">qui</a>).

### Bonus track

<p style="text-align: justify;">
  Il RBFL permette di iterare su una qualsiasi struttura &#8220;iterabile&#8221;. Abbiamo detto poco fa cosa vuol dire, ma vogliamo vederne un esempio pratico?
</p>

<p style="text-align: justify;">
  Supponiamo di voler iterare su tutti gli interi entro un certo intervallo, qualcosa del tipo:
</p>

<code lang="cpp" escaped="true">for (int i=0; i&lt;100; ++i)&lt;br />
...</code>

<p style="text-align: justify;">
  Possiamo usare il RBFL senza creare una sequenza intermedia? Sì, per farlo abbiamo proprio bisogno di scrivere una struttura iterabile e un InputIterator che ne abiliti l&#8217;iterazione. Per il nostro scopo, in realtà, dobbiamo solo implementare un wrapper ad un finto container che simuli una lista crescente di numeri ed un suo iteratore.
</p>

<p style="text-align: justify;">
  Per ricapitolare, vogliamo qualcosa del genere:
</p>

<code lang="cpp" escaped="true">for (auto i : range{0,10})&lt;br />
{&lt;br />
   cout &lt;&lt; i &lt;&lt; " ";&lt;br />
}&lt;br />
// 0 1 2 3 4 5 6 7 8 9</code>  
Ribadisco che questo è solo un esempio, molto probabilmente non efficiente quanto un for da 0 a N!

Iniziamo da questo &#8220;finto container&#8221;. Abbiamo detto che per usare il RBFL è sufficiente implementare una delle tre opzioni:

  * funzioni** membro** x.**begin() **e** **x.**end()**, _oppure_
  * funzioni **non-membro** **begin(x)** e **end(x)** (trovate con ADL &#8211; Argument Dependent Lookup), _oppure_
  * specializzazioni **std::begin(x)** e **std::end(x)**

Scegliamo la prima e supponiamo, per un attimo, di aver già pensato al nostro InputIterator ad-hoc:  
<code lang="cpp" escaped="true">class range_t&lt;br />
{&lt;br />
public:&lt;br />
   class range_it&lt;br />
   {&lt;br />
   // lo vediamo dopo&lt;br />
   }&lt;/p>
&lt;p>   range_t(int s, int e)&lt;br />
      : start_it{s}, end_it{e}&lt;br />
   {&lt;br />
   }&lt;/p>
&lt;p>   range_it begin()&lt;br />
   {&lt;br />
      return start_it;&lt;br />
   }&lt;/p>
&lt;p>   range_it end()&lt;br />
   {&lt;br />
      return end_it;&lt;br />
   }&lt;/p>
&lt;p>private:&lt;br />
   range_it start_it;&lt;br />
   range_it end_it;&lt;br />
};</code>  
La nostra classe **range_t** mantiene due iteratori che rappresentano inizio e fine range. Ora vediamo una possibile implementazione di **range_it**:  
<code lang="cpp" escaped="true">class range_it&lt;br />
{&lt;br />
public:&lt;br />
   range_it(int val)&lt;br />
      : value{val}&lt;br />
   {&lt;br />
   }&lt;/p>
&lt;p>   int operator*() const&lt;br />
   {&lt;br />
      return value;&lt;br />
   }&lt;/p>
&lt;p>   bool operator!=(const range_it& o) const&lt;br />
   {&lt;br />
      return value != o.value;&lt;br />
   }&lt;/p>
&lt;p>   range_it& operator++()&lt;br />
   {&lt;br />
      ++value;&lt;br />
      return *this;&lt;br />
   }&lt;/p>
&lt;p>private:&lt;br />
   int value;&lt;br />
};</code>

<p style="text-align: justify;">
  L&#8217;idea (banale) è di wrappare un valore del range in questo iteratore range_it. Le operazioni su un range_it sono in realtà operazioni sul valore che wrappa.
</p>

<p style="text-align: justify;">
  Non siamo totalmente conformi alle <a href="http://www.cplusplus.com/reference/iterator/InputIterator/">specifiche di un InputIterator</a> ma siamo dentro ai requisiti del RBFL (perché questo ha bisogno solo degli operatori che abbiamo implementato):
</p>

<code lang="cpp" escaped="true">for (auto i : range_t{0, 10})&lt;br />
{&lt;br />
   cout &lt;&lt; i &lt;&lt; " ";&lt;br />
}&lt;br />
// 0 1 2 3 4 5 6 7 8 9</code>

<p style="text-align: justify;">
  L&#8217;esempio è volutamente semplice. Restano aperte alcune questioni (anch&#8217;esse non complicate da affrontare) che lasciamo ai lettori, come ad esempio:
</p>

  * <span style="line-height: 12px;">generalizzare il range per qualsiasi tipo numerico (attenzione all&#8217;operator!= su float e double&#8230;),</span>
  * completare range_it in modo che implementi tutte le specifiche di un InputIterator,
  * personalizzare lo step (e.g. {0, 10} a step di 0.1).