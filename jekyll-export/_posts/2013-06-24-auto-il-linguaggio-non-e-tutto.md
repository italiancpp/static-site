---
id: 625
title: 'auto: il linguaggio non è tutto'
date: 2013-06-24T11:44:06+02:00
author: davide
layout: post
guid: http://www.italiancpp.org/?p=625
permalink: /2013/06/24/auto-il-linguaggio-non-e-tutto/
categories:
  - Hands-on
tags:
  - basic
---
<p style="text-align: justify;">
  Molta enfasi di recente è stata posta sul nuovo uso della keyword <strong>auto</strong> in C++11 (si veda per esempio <a title="qui" href="http://herbsutter.com/2013/06/05/gotw-92-auto-variables-part-1/">qui</a>). In sintesi, auto sostituisce un tipo esplicito con una richiesta rivolta al compilatore di riempire con l&#8217;informazione corretta:
</p>

<code lang="cpp" escaped="true">&lt;br />
std::vector&lt;double&gt; v;&lt;br />
auto it = v.begin();&lt;br />
</code>

<p style="text-align: justify;">
  Il frammento sopra afferma: <em>lascio al compilatore la deduzione del tipo di it.</em>
</p>

<p style="text-align: justify;">
  La maggior parte dei commenti però tende a enfatizzare <em>i casi in cui usare auto,</em> ma il vero problema è quando <em>non </em>usarlo. Siccome la keyword risparmia fatica al programmatore, ricordare continuamente &#8220;usate auto qui, usate auto là&#8221; porta facilmente a pensare che vada usato sempre, e diventa abbastanza naturale abusarne. auto però non è gratis: <strong>è fondamentale che il codice esprima correttamente l&#8217;intento del programmatore</strong>. se l&#8217;intento è chiaro, i bug diventano evidenti e si possono correggere facilmente. ma <strong>ci sono casi in cui l&#8217;uso di auto nasconde l&#8217;intento</strong>:
</p>

<ul style="text-align: justify;">
  <li>
    rileggendo il codice a distanza di tempo,<strong> diventa più difficile</strong> <strong>capire cosa</strong> <strong>sta</strong> <strong>succedendo</strong> (soprattutto se <em>tutte</em> le variabili locali sono auto&#8230; caso realmente accaduto)
  </li>
  <li>
    ci sono casi in cui un <strong>cast</strong> viene <strong>involontariamente</strong> <strong>eliminato: </strong>nell&#8217;esempio semplificato sopra, it poteva essere const_iterator, ma il programmatore intendeva dire <em>auto it = v.cbegin() </em>oppure <em>const_iterator it = v.begin()</em>?.
  </li>
  <li>
    (caso particolare del punto precedente) alcuni container restituiscono dei proxy, e l&#8217;uso indiscriminato di auto può rompere del codice funzionante
  </li>
</ul>

<code lang="cpp" escaped="true">&lt;br />
bool f1()&lt;br />
{&lt;br />
   std::vector&lt;bool&gt;* vp = new std::vector&lt;bool&gt;(1000, true);&lt;br />
   bool y = (*vp)[314]; // ok&lt;br />
   delete vp;&lt;br />
   return y;&lt;br />
}&lt;/p>
&lt;p>bool f2()&lt;br />
{&lt;br />
   std::vector&lt;bool&gt;* vp = new std::vector&lt;bool&gt;(1000, true);&lt;br />
   auto y = (*vp)[314]; // mmm...&lt;br />
   delete vp;&lt;br />
   return y; // argh! il proxy potrebbe leggere il container già distrutto&lt;br />
}&lt;br />
</code>

  *  un **IDE** che fa un parsing euristico potrebbe **non** essere più **in grado** **di** **elencare** **correttamente** **tutti** **i punti in cui un tipo viene usato;** a volte il _completamento automatico_ non funziona più. si pensi ad esempio a:

<code lang="cpp" escaped="true">&lt;br />
class ABC&lt;br />
{&lt;br />
   int size() const;&lt;br />
};&lt;br />
</code>

ABC GimmeMyObject();

<code lang="cpp" escaped="true">&lt;br />
// molto più tardi...&lt;br />
auto abc = GimmeMyObject();&lt;br />
auto n = GimmeMyObject().size();&lt;br />
</code>

<p style="text-align: justify;">
  Durante il refactoring, si vogliono trovare tutti gli oggetti di tipo ABC; normalmente basta una ricerca di testo (ci possono essere mille motivi: progetto troppo grosso, o stiamo usando un modem a 56k e vi&#8230;), ma se la variabile è auto, ci vuole un IDE più sofisticato e ben integrato con il compilatore.
</p>

<p style="text-align: justify;">
  In sintesi, <span style="line-height: 12px;">è una <span style="text-decoration: underline;">buona</span> idea usare auto quando:</span>
</p>

<ol style="text-align: justify;">
  <li>
    <strong>chiunque è in grado di dedurre il tipo </strong>senza saltellare attraverso il codice<strong>,</strong> vuoi per il nome della variabile, vuoi per la semplicità dell&#8217;inizializzazione (cfr. esempio #1). Di solito, il tipo è un nome dipendente e lunghissimo (std::map<std::string, std::list<double>, MySpecialComparisonOperator, MyCustomAllocator>::const_iterator&#8230;); questa è una buona indicazione per usare auto.
  </li>
  <li>
    il <strong>tipo</strong> della variabile <strong>potrebbe</strong> <strong>cambiare</strong> in qualsiasi momento, <strong>mantenendo</strong> <strong>la</strong> <strong>stessa</strong> <strong>interfaccia</strong>. Nell&#8217;esempio #2, si pensi che le prime righe siano in realtà <em>generate da un programma esterno che emette codice c++</em> (ad esempio, <a title="questo" href="http://code.google.com/p/protobuf/">questo</a>). Il tipo esatto di &#8220;n&#8221; potrebbe variare semplicemente aggiornando il programma esterno, ma il cambiamento <em>potrebbe</em> non essere rilevante (spesso basta che sia n un intero con certe proprietà);
  </li>
  <li>
    quando c&#8217;è un limite di  80 caratteri per riga (ma suvvia&#8230; siamo nel 2013, <a title="chi mai" href="http://google-styleguide.googlecode.com/svn/trunk/cppguide.xml#Line_Length">chi</a> mai segue una regola del genere?).
  </li>
</ol>

<p style="text-align: justify;">
  Per enfatizzare che il nostro scopo è <em>scoraggiare criticamente</em>, riportiamo anche i casi contrari: è una <span style="text-decoration: underline;">cattiva</span> idea usare auto quando:
</p>

<ol style="text-align: justify;">
  <li>
    l&#8217;<strong>inizializzazione non è ovvia</strong>, ovvero solo guardando cosa c&#8217;è a destra dell&#8217;= non è possibile dedurre il tipo della variabile. auto significa &#8220;lascio la deduzione al compilatore&#8221;, ma non &#8220;lascio la deduzione al compilatore&#8230; perché io non la so fare&#8221; (questo si applica anche alle somme di interi di tipo diverso, p.es. short + unsigned char)
  </li>
  <li>
    c&#8217;è un <strong>cast  </strong>di mezzo<br /> <code lang="cpp" escaped="true">&lt;br />
auto x = static_cast&lt;int&gt;(GetNumberAsDouble()); // mmm... l'intento è chiaro, ma il codice è contorto&lt;br />
</code>
  </li>
  <li>
    c&#8217;è un <strong>proxy</strong>: auto rischia di tenere in vita degli oggetti che non sono pensati per sopravvivere a lungo
  </li>
  <li>
    <span style="line-height: 12px;">si esagera! non è il caso di iniziare un sorgente con:</span>
  </li>
</ol>

<code lang="cpp" escaped="true">&lt;br />
auto main(auto argc, const auto* argv[]) -&gt; int // uhm... forse in c++2075...&lt;br />
</code>

<p class="lang:c++ decode:true">