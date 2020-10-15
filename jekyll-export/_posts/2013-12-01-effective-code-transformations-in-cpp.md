---
id: 2177
title: Effective Code Transformations in C++ (IAD13)
date: 2013-12-01T15:53:40+01:00
author: marco
layout: post
guid: http://www.italiancpp.org/?p=2177
permalink: /2013/12/01/effective-code-transformations-in-cpp/
categories:
  - News
tags:
  - IAD13
---
<p style="text-align: justify;">
  Ieri, in occasione dell&#8217;<a title="IAD13" href="http://www.agileday.it/front/" target="_blank">Italian Agile Day 2013</a>, <strong><span style="color: #2945a4;">++it</span></strong> (rappresentata da <em>Marco Arena</em>) ha presentato con <a href="https://twitter.com/paolopolce" target="_blank">Paolo Polce</a> un talk dal titolo &#8220;<a href="http://www.agileday.it/front/sessioni/#code_transformations" target="_blank"><em>Effective Code Transformations in C++</em></a>&#8220;. Obiettivo della sessione è stato quello di mostrare il nuovo C++ anche ad una platea di sviluppatori provenienti da tecnologie diverse dal nativo. Con piacevole sorpresa la platea era composta anche (e in buona parte) da programmatori C++! Quindi il talk è stato molto più interattivo e divertente del previsto, arricchito da diverse domande interessanti alle quali abbiamo risposto durante la sessione e che riporteremo alla fine di questo post.
</p>

<p style="text-align: justify;">
  Intanto <strong>grazie</strong> <strong>all&#8217;Agile Day</strong> e tutti i suoi organizzatori per averci dato la possibilità di raccontare, seppur in piccolo, il nuovo C++. <strong>Grazie a tutti i</strong> <strong>partecipanti</strong> alla nostra sessione. E <strong>grazie a tutti coloro che si uniranno alla nostra giovane comunità</strong>!
</p>

<p style="text-align: justify;">
  In questo articolo vorremmo fare un wrap-up dei contenuti, nonché segnalarvi dove poter scaricare slide e la solution che abbiamo utilizzato per mostrare alcune demo live. Prima di iniziare rinnovo la richiesta di feedback a tutti i partecipanti, preziosissima per migliorare! Potete contribuire su <a href="https://joind.in/talk/view/10183" target="_blank">joind.in</a>. Grazie!
</p>

<p style="text-align: center;">
  <a href="http://www.slideshare.net/ilpropheta/effective-code-transformations-in-c"><img loading="lazy" class="wp-image-2211 aligncenter" alt="slideshare-logo" src="http://www.italiancpp.org/wp-content/uploads/2013/12/slideshare.png" width="65" height="65" srcset="http://192.168.64.2/wordpress/wp-content/uploads/2013/12/slideshare.png 300w, http://192.168.64.2/wordpress/wp-content/uploads/2013/12/slideshare-150x150.png 150w, http://192.168.64.2/wordpress/wp-content/uploads/2013/12/slideshare-250x250.png 250w" sizes="(max-width: 65px) 100vw, 65px" /></a>
</p>

<h4 style="text-align: center;">
  <a href="http://www.slideshare.net/ilpropheta/effective-code-transformations-in-c" target="_blank"><strong>Slides</strong> su SlideShare</a>
</h4>

<h5 style="text-align: center;">
  <span style="color: #ffffff; text-align: justify; font-size: 12px;"> </span>
</h5>

<p style="text-align: center;">
  <strong><a href="https://ilpropheta@bitbucket.org/ilpropheta/iad2013.git "><img loading="lazy" class="size-full wp-image-2212 aligncenter" alt="cppbitbucket-logo" src="http://www.italiancpp.org/wp-content/uploads/2013/12/cppbitbucket.png" width="64" height="64" /></a></strong>
</p>

<h4 style="text-align: center;">
  Live-demo:
</h4>

<h4 style="text-align: center;">
  <strong><a href="https://ilpropheta@bitbucket.org/ilpropheta/iad2013.git" target="_blank">https://ilpropheta@bitbucket.org/ilpropheta/iad2013.git</a> </strong>
</h4>

<p style="text-align: justify;">
  <p style="text-align: justify;">
    <span style="color: #ffffff;"> </span>
  </p>
  
  <h5 style="text-align: left;">
    Note delle live-demo:<br /> <span style="color: #ffffff;"> </span>
  </h5>
  
  <ul>
    <li>
      abbiamo usato <em><strong>Visual Studio 2013 Preview;</strong></em>
    </li>
    <li>
      abbiamo mostrato solo i file <strong>main.cpp</strong> e <strong>PPLSesame.cpp;</strong>
    </li>
    <li>
      <strong>GMOCK è già nella solution</strong>, in un folder apposito, quindi basta clonare tutto il repo per essere pronti a compilare ed eseguire!
    </li>
  </ul>
  
  <p style="text-align: justify;">
    <h3 style="text-align: justify;">
      Contenuti del talk
    </h3>
    
    <p style="text-align: justify;">
      Essendo ospitati da una conferenza multi-tecnologica, non potevamo dare per scontato che la platea conoscesse perfettamente il linguaggio e le novità. Per questo abbiamo puntato su un contenuto &#8220;aperto a tutti&#8221;, soprattutto a chi non aveva un background C++. Il talk è stato una sorta di intervista da parte di Paolo (che programma in C++ dai primi anni &#8217;90) a Marco (&#8220;rappresentante&#8221; delle novità).
    </p>
    
    <p style="text-align: justify;">
      Al centro del talk le <strong>trasformazioni efficaci</strong>, ovvero mutazioni che rendono il codice più leggibile, manutenibile, modificabile e compatto. Le trasformazioni affrontate sono state di due categorie: codice old-style C++98 portato in C++11/14 e codice multi-thread C++11 migliorato con costrutti più appropriati. Il talk è stato diviso quindi in tre parti:
    </p>
    
    <ol>
      <li>
        <span style="line-height: 12px;">Esempi di <strong>codice C++98 trasformati in C++11/14</strong>. Il risultato è stato poi confrontato con C#, trovando grandi somiglianze.</span>
      </li>
      <li>
        <strong>Patterns</strong>: (1) come scrivere una <em>Factory</em> in C++11/14, (2) <em>RAII</em> e <em>DEFER</em>.
      </li>
      <li>
        <strong>Multi-threaded</strong> C++ con tre trasformazioni C++11 (thread &#8211; future &#8211; future/promise) e tre trasformazioni con task <strong>PPL</strong>.
      </li>
    </ol>
    
    <p style="text-align: justify;">
      Chiaramente seguire solo con le slide non rende come quello che abbiamo detto a voce, però è una buona traccia. Gli argomenti scelti per la presentazione sono stati pochi (per ragioni di tempo) ma significativi.
    </p>
    
    <h3 style="text-align: justify;">
      Contenuti delle live-demo
    </h3>
    
    <p style="text-align: justify;">
      La parte <strong>3 </strong>(multithreading) è stata interamente raccontata al PC con un <strong>Visual Studio 2013 Preview </strong>davanti agli occhi. Ecco riassunto quello che abbiamo mostrato:
    </p>
    
    <ol>
      <li>
        <span style="line-height: 12px;"><span style="line-height: 12px;">Un banale esempio di <strong>thread</strong> C++11 che calcola la media di un vettore mentre nel main viene calcolato in parallelo il massimo.</span></span>
      </li>
      <li>
        Prima trasformazione: usiamo un <strong>future</strong> (un contenitore asincrono di un risultato) creato con <strong>async</strong>.
      </li>
      <li style="text-align: justify;">
        Seconda trasformazione: e se vogliamo gestire il thread a mano (o abbiamo bisogno di fare altro dopo che il risultato del future è stato calcolato)? Mostriamo le <strong>promise </strong>(provider asincrono del risultato di un future).
      </li>
      <li style="text-align: justify;">
        Introduciamo la <strong>Parallel Patterns Library</strong> (<strong>PPL</strong>) di Microsoft. Disponibile giù da Visual Studio 2010 e poi migliorata ancora nel 2012 con enfasi su task composition e async. Mostriamo quindi un primo esempio completamente sincrono (non c&#8217;è concorrenza) dove: prima si finge di leggere un file, poi questo viene decorato con tag HTML, poi si simulano alcune operazioni sul main e infine si visualizza il file decorato a console.
      </li>
      <li style="text-align: justify;">
        Prima trasformazione con un task PPL, dove almeno la lettura è parallela ad alcune operazioni sul main. Ancora bloccante la decorazione e le successive operazioni sul main.
      </li>
      <li style="text-align: justify;">
        Ultima trasformazione con <strong>task.then</strong> (<strong>continuation</strong>), dove lettura, decorazione e operazioni sul main sono completamente asincrone. In particolare dopo la lettura (asincrona) del file, il nuovo task (ancora asincono) diventa la decorazione. La continuation ha diversi benefici, come composizione dei task e propagazione delle eccezioni.
      </li>
    </ol>
    
    <h3>
      Le vostre domande
    </h3>
    
    <p>
      Due premesse:
    </p>
    
    <ol>
      <li>
        <span style="line-height: 12px;"><span style="line-height: 12px;"><strong>Hai seguito il talk e hai altre domande</strong>? Scrivile qui in un commento oppure apri una discussione specifica sul forum!</span></span>
      </li>
      <li>
        <strong>Vuoi contribuire migliorando le risposte alle domande che abbiamo dato durante il talk</strong>? Commenta l&#8217;articolo!
      </li>
    </ol>
    
    <p>
      Ecco alcune domande che ci avete fatto (perdonate se ne dimentichiamo qualcuna) e la sintesi delle nostre risposte:
    </p>
    
    <ol>
      <li style="text-align: justify;">
        <span style="line-height: 12px;"><span style="line-height: 12px;">La Factory ritorna <strong>unique_ptr<IWriter> </strong>ma perché è possibile ritornare uno <strong>unique_ptr<CoutWriter></strong> (con <em>CoutWriter</em> che deriva da <em>IWriter</em>)?<br /> <strong>R:</strong> Perché <em>CoutWriter</em> è convertibile in un <em>IWriter</em>. Il move-constructor dello unique_ptr è generico.</span></span><br /> <span style="color: #ffffff;"> </span>
      </li>
      <li>
        Posso castare lo <strong>unique_ptr<IWriter></strong> ad un <strong>IWriter*</strong>?<br /> <strong>R:</strong> Sì, ma esplicitamente. Puoi ottenere l&#8217;<em>IWriter*</em> che lo <em>unique_ptr</em> sta gestendo usando <strong>.get()</strong>.<br /> <span style="color: #ffffff;"> </span>
      </li>
      <li>
        Cosa succede se usando <strong>async</strong>, la lambda tira eccezione?<br /> <strong>R:</strong> Viene propagata al <strong>.get()</strong> del future.<br /> <span style="color: #ffffff;"> </span>
      </li>
      <li style="text-align: justify;">
        Posso creare un <em>thread</em> che non parte subito?<br /> <strong>R:</strong> Puoi creare un <em>thread</em> &#8220;vuoto&#8221;, cioè non associato a nessun flusso di esecuzione e poi assegnarlo in un secondo momento. Però, che noi sappiamo, non puoi evitare che il <em>thread</em> parta se l&#8217;hai costruito con un callable-object (e.g lambda).<br /> <span style="color: #ffffff;"> </span>
      </li>
      <li style="text-align: justify;">
        Puoi fare <strong>.get()</strong> su un <em>future</em> ma solo per un certo periodo di tempo?<br /> <strong>R:</strong> Sì, puoi usare <strong>.wait_for()</strong>/<strong>wait_until()</strong> passando opportune unità temporali di <em>std::chrono</em> e ottenere uno <em>future_status</em> che ti dice se il risultato è pronto.<br /> <span style="color: #ffffff;"> </span>
      </li>
      <li style="text-align: justify;">
        Puoi chiamare <strong>.get()</strong> sul <em>future</em> più di una volta?<br /> <strong>R:</strong> No, è come se stessi &#8220;prelevando&#8221; il risultato dal contenitore. Puoi usare uno <em>shared_future</em> per leggere il risultato più volte e da più threads. <span style="text-decoration: underline;">Nota a posteriori:</span> &#8220;prelevando&#8221; vuol dire &#8220;muovendo&#8221;, ma non avendo parlato di move-semantics non potevamo spiegare il concetto in questi termini.<br /> <span style="color: #ffffff;"> </span>
      </li>
      <li style="text-align: justify;">
        E&#8217; possibile fare in modo che il <em>thread</em> associato al <em>future</em> parta solo quando fai <strong>.get()</strong>? Una specie di <em>lazy evaluation</em>?<br /> <strong>R:</strong> Sì, puoi rendere la chiamata sincrona (nello stesso thread) passando come primo parametro di <em>std::async</em> una politica di lancio <strong>deferred</strong>.<br /> <span style="color: #ffffff;"> </span>
      </li>
      <li style="text-align: justify;">
        Quali compilatori supportano le nuove features?<br /> <strong>R:</strong> Visual Studio 2010 già conteneva diverse cose come le lambda, la gli smart pointers e auto. Visual Studio 2012 ha quasi tutto il supporto della concorrenza più altre cose. Il 2013 va ancora più avanti ma non è ancora completo. Clang è invece 100% compliant al C++11 e la prossima release lo sarà anche per il C++14. Anche GCC è full compliant al C++11.<br /> <span style="color: #ffffff;"> </span>
      </li>
      <li style="text-align: justify;">
        Ma il <strong>C++14</strong> è già standard ISO?<br /> <strong>R:</strong> Non è ancora stato ufficialmente &#8220;rilasciato&#8221; ma tutto quello che ci deve finire dentro è stato deciso, quindi è come se ci fosse un &#8220;bollo papale&#8221; 🙂<br /> <span style="color: #ffffff;"> </span>
      </li>
      <li style="text-align: justify;">
        Cosa consigliate per provare le nuove features?<br /> <strong>R:</strong> La cosa più semplice che puoi fare è utilizzare qualche compilatore online. Ne abbiamo uno anche noi ed è <a href="www.italiancpp.org/compiler/" target="_blank">qui</a>. Chiaramente per approfondire ti conviene scegliere un ambiente, studiare e provare!
      </li>
    </ol>
    
    <p>
      Con la speranza che quanto abbiamo presentato sia stato gradito, aspettiamo i vostri feedback! Grazie ancora!
    </p>