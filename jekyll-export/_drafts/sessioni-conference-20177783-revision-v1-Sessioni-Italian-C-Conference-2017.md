---
id: 8093
title: Sessioni Italian C++ Conference 2017
date: 2017-06-14T16:21:46+02:00
author: marco
layout: revision
guid: http://www.italiancpp.org/2017/06/14/7783-revision-v1/
permalink: /2017/06/14/7783-revision-v1/
---
#### <a href="http://www.italiancpp.org/event/conference-2017" target="_blank" rel="noopener noreferrer">Pagina dell&#8217;evento</a>

#### <span style="color: #ffffff;"> </span>  
<a id="1"></a>  
<span style="color: #ffffff;"> </span>

* * *

#### <span style="color: #2945a4;">C++ executors to enable heterogeneous computing in tomorrow&#8217;s C++ today</span>

##### [Michael Wong](http://italiancpp.org/speakers#mwong)

<p style="text-align: justify;">
  For a long time, C++ has been outpaced by other models such as CUDA, OpenMP, OpenCL, HSA, which has offered Heterogeneous computing capability to enable dispatch to GPU, DSP, FPGA or other accelerators.<br /> SG14 is an ISO C++ SG that works on low-latency, in the areas of Games, Financial, Embedded programming. One of their mandate is support of heterogeneous in Native C++, without having to drop to some other model as is needed today.<br /> This talk will describe the first and possibly the most important step towards supporting heterogeneous computing with a description of C++ executors, an interface between concurrency constructs, and the agents/resources, one of which can be a GPU core, or a SIMD unit.  I have led a small group of experts from Google, Nvidia, Codeplay, and NASDAQ, to define a specification to enable separation of concerns in defining where, when, and how execution is done in service of the constructs in existing C++ standard library, Concurrency, Parallelism, Transactional Memory, and Networking TS.<br /> This talk will help you understand these TSes which currently only works on CPUs and how they will tie together in future to enable execution on accelerators based on C++ models we already have today such as SYCL, HPX, Kokkos, and Raja. This will enable native C++ to be usable on machine learning algorithms on future self-driving cars, or medical devices.
</p>

<h5 style="text-align: justify;">
  <span style="color: #339966;">Keynote da 75&#8242;</span>
</h5>

<h5 style="text-align: justify;">
</h5>

<h5 style="text-align: justify;">
  <a id="2"></a><br /> <span style="color: #ffffff;"> </span>
</h5>

* * *

#### <span style="color: #2945a4;">Lambda out: a simple pattern for generic output</span>

##### [Davide Di Gennaro](http://italiancpp.org/speakers#dadigen)

<p style="text-align: justify;">
  The lecture will show how to adapt the traditional STL-style generic algorithms to C++0x, replacing output iterators with &#8220;output functors&#8221;
</p>

##### <span style="color: #339966;">Talk da 60&#8242;</span>

<span style="color: #ffffff;"> </span>  
<a id="3"></a>  
<span style="color: #ffffff;"> </span>

* * *

#### <span style="color: #2945a4;">An overly simple, C++ idiomatic pattern language for message-based product families<br /> </span>

##### <a href="http://italiancpp.org/speakers#carlo-pescio" target="_blank" rel="noopener noreferrer">Carlo Pescio</a>

<p style="text-align: justify;">
  In questo talk mostro come realizzare un sistema, costituito modularmente da sottosistemi, ognuno dei quali gestisce messaggi, in modo realmente estendibile. Per aggiungere un sottosistema o un messaggio aggiungiamo dei file. Per eliminarli li escludiamo. Nessun file viene mai modificato e l&#8217;eseguibile includerà i soli sottosistemi e messaggi richiesti. Non si utilizzano configurazioni esterne, caricamenti dinamici o pseudo reflection. Vedremo anche come alcuni vituperati pattern siano in realtà utili, una volta capite bene alcune simmetrie ed asimmetrie proprie del C++.
</p>

<h5 style="text-align: justify;">
  <span style="color: #339966;">Talk da 60&#8242;</span>
</h5>

<span style="color: #ffffff;"> <a id="4"></a></span>

<span style="color: #ffffff;"> </span>

* * *

#### <span style="color: #2945a4;">Monads for C++<br /> </span>

##### <a href="http://italiancpp.org/speakers#bartosz" target="_blank" rel="noopener noreferrer">Bartosz Milewski</a>

<p style="text-align: justify;">
  Monad is no longer a dirty word at C++ conferences. Ignoring monads got us a flawed design of std::future (monadic &#8220;then&#8221; and &#8220;make_ready_future&#8221; are to this day experimental). I&#8217;ve talked about monads in C++ before, but I never tackled the most mysterious one, the IO monad. Realizing that no amount of abstract nonsense is going to make monads approachable, I decided to explain abstraction through implementation. Once you see how it works, you&#8217;ll be surprised what a powerful pattern it is.
</p>

<h5 style="text-align: justify;">
  <span style="color: #339966;">Talk da 60&#8242;</span>
</h5>

<span style="color: #ffffff;"> </span>  
<a id="5"></a>  
<span style="color: #ffffff;"> </span>

* * *

#### <span style="color: #2945a4;">Costruire un bridge C++ tra NodeJS e C#</span>

##### <a href="http://italiancpp.org/speakers#raf" target="_blank" rel="noopener noreferrer">Raffaele Rialdi</a>

<p style="text-align: justify;">
  Oggi più che mai l&#8217;interoperabilità tra linguaggi è strategica per moltissime applicazioni. NodeJS, C++ e .NET sono ecosistemi ben consolidati che risolvono problemi differenti. La loro integrazione non solo è possibile ma può rivelarsi strategica per sfruttare il meglio dei tre mondi e distribuire le competenze all&#8217;interno del team di sviluppo.
</p>

<p style="text-align: justify;">
  Nel corso della sessione vedremo un esempio di come sia possibile sviluppare uno strato di interoperabilità che permetta a NodeJS di comunicare con C++ e a catena con una libreria C# sviluppata con il più recente .NET Core.
</p>

<p style="text-align: justify;">
  Sarà un&#8217;occasione per vedere cosa si nasconde dietro la libreria V8, cuore di NodeJS, l&#8217;hosting del CoreCLR e la tecnica di Reverse PInvoke che permette di eseguire chiamate native verso .NET.
</p>

<p style="text-align: justify;">
  L&#8217;esempio più interessante sarà quello di sviluppare una applicazione Electron/Angular2 con un backend misto tra C++ e C#.
</p>

##### <span style="color: #339966;">Talk da 60&#8242;</span>

<a id="6"></a>  
<span style="color: #ffffff;"> </span>

* * *

#### <span style="color: #2945a4;">Una libreria di rete asincrona scritta in C++ ispirata a Node.js</span>

##### <a href="http://italiancpp.org/speakers#ste-cristiano" target="_blank" rel="noopener noreferrer">Stefano Cristiano</a>

<p style="text-align: justify;">
  Racconterò le motivazioni che hanno portato a creare un framework in C++ per programmazione asincrona di rete (e molto altro) ispirato a Node.js.
</p>

##### <span style="color: #339966;">Talk da 60&#8242;</span>

##### <a id="7"></a><span style="color: #ffffff;"> </span>

* * *

#### <span style="color: #2945a4;">Talk C++ like a restless pirate</span>

##### <a href="http://italiancpp.org/speakers#marco-foco" target="_blank" rel="noopener noreferrer">Marco Foco</a>

<p style="text-align: justify;">
  Nata all&#8217;inizio del nuovo millennio, la religione Pastafariana ha portato sin da subito innovazione in ogni campo della scienza e della fede, proponendo nuove teorie, come quella che vede l&#8217;uomo discendere dal pirata, e scoprendo la sorprendente correlazione tra assenza di pirati e riscaldamento globale.
</p>

<p style="text-align: justify;">
  In questo intervento verra&#8217; proposta una soluzione a quest&#8217;ultimo problema basata sul ritorno alle origini (ricorrendo quindi al gergo piratesco), dando al contempo nuovi significati a termini come &#8220;Arr!&#8221;, &#8220;Aaargh!&#8221; e &#8220;Aaaargh?!&#8221;.
</p>

<p style="text-align: justify;">
  Ai partecipanti è cortesemente richiesto di portare bende per occhio, uncini e pappagalli da casa.
</p>

##### <span style="color: #339966;">Talk da 60&#8242;</span>

##### <a id="8"></a>  
<span style="color: #ffffff;"> </span>

* * *

#### <span style="color: #2945a4;">Boost vs Qt: What Could They Learn From Each Other?<br /> </span>

##### [Jens Weller](http://italiancpp.org/speakers#jens)

<p style="text-align: justify;">
  Having a long history of using boost and Qt, plus visiting both communities for a long time, this talk reflects, on what the boost and Qt communities could learn from each other.
</p>

##### <span style="color: #339966;">Talk da 60&#8242;</span>

##### <a id="9"></a>  
<span style="color: #ffffff;"> </span>

* * *

#### <span style="color: #2945a4;">Functional C++ for Fun and Profit<br /> </span>

##### [Phil Nash](http://italiancpp.org/speakers#phil-nash)

<p style="text-align: justify;">
  C++11 gave us lambdas in the language for the first time (boost::lambda aside) &#8211; so it&#8217;s a functional language now, right? There&#8217;s a bit more to functional programming than having first class function objects (and I&#8217;d even argue we still don&#8217;t quite have that). But does that mean we can&#8217;t do functional programming in C++? Yes. No. Maybe&#8230;<br /> First we have to define what functional programming actually is &#8211; and it may not be quite what you think! Then we need to see what valuable ideas have come out of the functional approach to software design and which ones we can use in C++ to good effect. In the end we&#8217;ll see that, while not strictly a functional programming language, we can get quite a long way with immutable data types, persistent data structures, atomic references, and &#8211; if you&#8217;re not watching carefully &#8211; we might even throw the M word in there!<br /> All this based on real-world experience &#8211; not just theoretical.
</p>

##### <span style="color: #339966;">Talk da 60&#8242;</span>

##### <a id="10"></a>  
<span style="color: #ffffff;"> </span>

* * *

#### <span style="color: #2945a4;">Quicker Sorting<br /> </span>

##### <a href="http://italiancpp.org/speakers#dietmar" target="_blank" rel="noopener noreferrer">Dietmar Kühl</a>

<p style="text-align: justify;">
  Quicksort is a well-known sorting algorithm used to implement sort functionality in many libraries. The presentation isn&#8217;t really about the algorithm itself but rather about how to actually create an efficient implementation of the algorithm: a text-book implementation of the algorithm actually is not that quick (even if the pivot is chosen cleverly). It takes paying some attention to detail to improve the implementation significantly. This presentation starts with a simple implementation and makes incremental improvements to eventually yield a proper generic and fast sorting function. All code will be in C++ but it should be possible to follow the majority of the reasoning with knowledge of another programming language.
</p>

##### <span style="color: #339966;">Talk da 60&#8242;</span>

##### <a id="11"></a>  
<span style="color: #ffffff;"> </span>

* * *

#### <span style="color: #2945a4;">Diversity and Inclusion in Microsoft</span>

##### <a href="http://italiancpp.org/speakers#ppresutto" target="_blank" rel="noopener noreferrer">Paola Presutto</a>

<p style="text-align: justify;">
  “Sii quello che ami essere”. In questa sessione percorriamo i princìpi di Diversity and Inclusion dal punto di vista di Microsoft: raccontiamo la trasformazione della cultura nei confronti della diversità come conduttore di una crescita personale ma anche di business.
</p>

##### <span style="color: #339966;">Talk da 45&#8242;</span>