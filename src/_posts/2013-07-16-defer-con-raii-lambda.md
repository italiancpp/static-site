---
id: 1072
title: 'DEFER con RAII &#038; lambda'
date: 2013-07-16T23:16:21+02:00
author: marco
layout: post
guid: http://www.italiancpp.org/?p=1072
permalink: /2013/07/16/defer-con-raii-lambda/
categories: Articoli
---
<p style="text-align: justify;">
  Spesso è necessario garantire <em>a tutti i costi</em> l&#8217;esecuzione di un certo frammento di codice entro lo scope di una funzione, ovvero prima che essa ritorni il controllo al chiamante. Supponiamo di doverci interfacciare con un&#8217;API legacy che presenta il classico pattern:
</p>

  1. <span style="line-height: 12px;">InitializeAPI(&#8230;) // alloca risorse</span>
  2. UseApi(&#8230;)
  3. &#8230;
  4. TerminateAPI(&#8230;) // libera risorse

Quindi per essere utilizzata, l&#8217;API ha prima bisogno di un&#8217;inizializzazione e poi alla fine di una terminazione. Una sequenza di questo tipo non è &#8220;sicura&#8221;:  
<code lang="cpp" escaped="true">&lt;br />
// exception-unsafe&lt;br />
void IWillUseTheAPI()&lt;br />
{&lt;br />
   InitializeAPI();&lt;br />
   UseAPI();&lt;br />
   // other stuff&lt;br />
   TerminateAPI();&lt;br />
}</code>

<p style="text-align: justify;">
  Cosa accadrebbe infatti se qualcosa (e.g. <em>UseApi</em>) sollevasse un&#8217;eccezione prima di arrivare alla chiamata di terminazione? Chiaramente, per com&#8217;è scritto il codice, la chiamata a <em>TerminateAPI</em> andrebbe persa causando potenziali problemi al resto del programma.
</p>

<p style="text-align: justify;">
  La soluzione classica a questo problema è di usare l&#8217;idioma <a href="http://en.wikipedia.org/wiki/Resource_Acquisition_Is_Initialization">RAII</a>, ovvero creare un oggetto che inizializzi risorse in costruzione e le rilasci in distruzione; qualcosa del tipo:
</p>

<code lang="cpp" escaped="true">&lt;br />
class LibWrapper&lt;br />
{&lt;br />
public:&lt;br />
   LibWrapper()&lt;br />
   {&lt;br />
     InitializeAPI();&lt;br />
   }&lt;/p>
&lt;p>   ~LibWrapper()&lt;br />
   {&lt;br />
     TerminateAPI();&lt;br />
   }&lt;/p>
&lt;p>   Use()&lt;br />
   {&lt;br />
     UseAPI();&lt;br />
   }&lt;br />
};&lt;/p>
&lt;p>void IWillUseTheAPI()&lt;br />
{&lt;br />
   LibWrapper wrapper; // Qui inizializza&lt;br />
   wrapper.Use(); // throw? Ok, terminerò lo stesso&lt;br />
} // Termina qui&lt;br />
</code>

<p style="text-align: justify;">
  Il C++ garantisce che in caso di eccezione tutti gli oggetti costruiti sullo stack vengano distrutti (<a href="http://stackoverflow.com/questions/2331316/what-is-stack-unwinding">stack unwinding</a>). Nel nostro caso l&#8217;istanza di <em>LibWrapper</em> è costruita sullo stack quindi abbiamo la garanzia di chiamare <em>TerminateAPI</em> nel suo distruttore non appena <em>wrapper</em> uscirà dallo scope (ovvero un attimo prima che <em>IwillUseTheAPI</em> ritorni).
</p>

La soluzione proposta è chiaramente poco generica. Possiamo allora sfruttare le novità del C++11 per fare ancora di meglio?

<p style="text-align: justify;">
  Sì. Possiamo implementare la versione più semplice di un <strong>DEFER</strong>, ovvero un&#8217;operazione che rimandi l&#8217;esecuzione di un certo codice al termine della funzione in cui compare, anche se viene sollevata un&#8217;eccezione. In pseudocodice, qualcosa del tipo:
</p>

<code lang="cpp" escaped="true">&lt;br />
void IWillUseTheAPI()&lt;br />
{&lt;br />
   InitAPI();&lt;br />
   DEFER(TerminateAPI()); // sarà eseguito alla fine&lt;br />
   //... altre chiamate&lt;br />
}</code>

<p style="text-align: justify;">
  Grazie alle lambda, possiamo passare codice scritto al volo e tenerlo da parte. Per essere sufficientemente generici, è possibile scrivere un wrapper che riceva in costruzione un qualsiasi oggetto che supporti l&#8217;operatore di chiamata a funzione (e.g. una lambda, un funtore, una std::function) e lo &#8220;esegua&#8221; in distruzione. Sintetizzando:
</p>

<code lang="cpp" escaped="true">&lt;br />
template &lt;typename F&gt;&lt;br />
struct finalizer&lt;br />
{&lt;br />
    template&lt;typename T&gt;&lt;br />
    finalizer(T&& f)&lt;br />
       : m_f { forward&lt;T&gt;(f) },&lt;br />
         m_dismiss { false }&lt;br />
    {&lt;br />
    }&lt;/p>
&lt;p>    ~finalizer()&lt;br />
    {&lt;br />
       if (!m_dismiss)&lt;br />
          m_f();&lt;br />
    }&lt;/p>
&lt;p>    // paranoia (leggi più avanti)&lt;br />
    finalizer(finalizer&& other)&lt;br />
       : m_f { move(other.m_f) },&lt;br />
         m_dismiss { other.m_dismiss }&lt;br />
    {&lt;br />
       other.m_dismiss = true; // altrimenti m_f() può essere eseguita due volte&lt;br />
    }&lt;/p>
&lt;p>    // non fanno parte della semantica del DEFER&lt;br />
    finalizer(const finalizer&) = delete;&lt;br />
    finalizer& operator=(const finalizer&) = delete;&lt;/p>
&lt;p>private:&lt;br />
    F m_f;&lt;br />
    bool m_dismiss;&lt;br />
}; &lt;/p>
&lt;p>template &lt;typename F&gt;&lt;br />
finalizer&lt;F&gt; defer(F&& f)&lt;br />
{&lt;br />
    return finalizer&lt;F&gt; { std::forward&lt;F&gt;(f) };&lt;br />
}</code>

<p style="text-align: justify;">
  Perché ho usato il flag m_dismiss e ho scritto il move constructor? Perché, nella chiamata a defer, <strong>non</strong> è garantito che i compilatori <a href="http://en.wikipedia.org/wiki/Copy_elision"><strong>elidano</strong> la copia</a> del <em>finalizer</em> &#8211; anche se molto probabilmente lo faranno. Chiaramente non è opportuno copiare un finalizer (tutti eseguono <em>m_f</em>?!) ma ci viene in aiuto la move semantics (la responsabilità di eseguire <em>m_f</em> viene <strong>trasferita</strong> all&#8217;<em>ultimo</em> <em>finalizer</em>).
</p>

<p style="text-align: justify;">
  Universal references (e.g. F&&) e forward servono ad evitare potenziali copie (ma è anche possibile passare tutto per valore e fare delle move). Il codice è semplice, non fa altro che tenere da parte una &#8220;funzione&#8221; (in realtà un oggetto che sa comportarsi come tale) e poi eseguirla in distruzione.
</p>

<p style="text-align: justify;">
  Come utilizzare tutto questo? Così:
</p>

<code lang="cpp" escaped="true">&lt;br />
void IWillUseTheAPI()&lt;br />
{&lt;br />
   InitAPI();&lt;br />
   auto defer_1 = defer([]{ TerminateAPI(); });&lt;br />
   // ...&lt;br />
}</code>

<p style="text-align: justify;">
  Non vi piace? Concordo! Usiamo una semplicissima macro per evitare di dare un nome ad un oggetto che non dovrà più essere utilizzato e per esplicitare la semantica di quello che stiamo facendo:
</p>

<code lang="cpp" escaped="true">&lt;br />
// generalmente tutti hanno queste (o di più generiche) due nella propria codebase :)&lt;br />
#define PASTE_STRING(arg1, arg2) DO_PASTE_STRING(arg1, arg2)&lt;br />
#define DO_PASTE_STRING(arg1, arg2) arg1 ## arg2&lt;/p>
&lt;p>#define DEFER(...) auto PASTE_STRING(defer_, __LINE__) = defer(__VA_ARGS__)&lt;br />
// e.g. auto defer_13 = defer(...)</code>  
E finalmente:  
<code lang="cpp" escaped="true">&lt;br />
void IWillUseTheAPI()&lt;br />
{&lt;br />
   InitAPI();&lt;br />
   DEFER([]{ TerminateAPI(); }); // sarà eseguito alla fine&lt;br />
   //... altre chiamate&lt;br />
}</code>

<p style="text-align: justify;">
  Questa è stata una delle primissime utility che ho inserito nella mia libreria di supporto! Poco tempo dopo ho scoperto che <a href="http://channel9.msdn.com/Shows/Going+Deep/C-and-Beyond-2012-Andrei-Alexandrescu-Systematic-Error-Handling-in-C">già ci aveva pensato Alexandrescu</a> e consiglio a tutti la visione del video (specialmente la prima parte, molto più deep di quella sullo ScopeGuard &#8211; l&#8217;equivalente del nostro DEFER).
</p>

<p style="text-align: justify;">
  Ricapitolando:
</p>

  * <span style="line-height: 12px;">No ad una cattiva struttura del codice che può portare problemi di exception-safety,</span>
  * Sì all&#8217;utilizzo dell&#8217;idioma RAII,
  * Sì++ se riusciamo ad essere non solo safe ma anche generici e flessibili. DEFER è solo un semplice esempio!