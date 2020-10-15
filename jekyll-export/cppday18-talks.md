---
id: 8794
title: C++ Day 2018 Talks
date: 2018-09-26T09:06:47+02:00
author: marco
layout: page
guid: https://www.italiancpp.org/?page_id=8794
wp_sponsor_link_behaviour:
  - "0"
evolve_sidebar_position:
  - default
evolve_full_width:
  - 'no'
evolve_page_title:
  - 'yes'
evolve_page_breadcrumb:
  - 'yes'
evolve_widget_page:
  - 'no'
evolve_slider_position:
  - default
evolve_slider_type:
  - 'no'
---
#### <a href="http://www.italiancpp.org/itcppcon18" target="_blank" rel="noopener noreferrer">Event page</a>

<span style="color: #ffffff;"> </span>

#### <a href="https://github.com/italiancpp/cppday18" target="_blank" rel="noopener noreferrer">Talks slides repository</a>

#### <span style="color: #ffffff;"> </span>  
<a id="1"></a>  
<span style="color: #ffffff;"> </span>

* * *

#### <span style="color: #2945a4;">HPX : High performance computing in C++ with concurrency, parallelism and futures</span>

##### [John Biddiscombe](https://www.italiancpp.org/speakers#jbiddiscombe)

<p style="text-align: justify;">
  HPX implements upcoming C++ standards proposals for C++17/20 and beyond, focusing on futures, executors and task based approaches to parallelism. The aim of HPX is to make distributed multi-threaded programming easier and safer so that the developer can focus on algorithm development and worry less about race conditions and concurrent programming tricks, whilst still giving the programmer the low-level tools necessary to fine tune performance. In this talk, I will cover the API basics of futures, continuations and the basics of Task Graphs (DAGs), some examples of executor use and show how CSCS is using HPX for High Performance Codes by exploring task affinity, thread pools, schedulers and how they interoperate with the C++ standard and the many core world of processors (and accelerators).
</p>

<h5 style="text-align: justify;">
  <span style="color: #339966;">Keynote <strong>[ENG]</strong>, 90 minutes</span>
</h5>

<a href="https://github.com/italiancpp/cppday18/blob/master/Keynote%20HPX%20-%20John%20Biddiscombe.pdf" target="_blank" rel="noopener noreferrer"><img loading="lazy" class="alignnone wp-image-3669 size-full" src="https://www.italiancpp.org/wp-content/uploads/2014/10/slides_icon-e1423585085875.png" alt="slides" width="142" height="83" /></a>    <a href="https://www.youtube.com/watch?v=ScKNrkN2SF4" target="_blank" rel="noopener noreferrer"><img loading="lazy" class="alignnone wp-image-5060" src="http://www.italiancpp.org/wp-content/uploads/2015/05/video-icon.png" alt="video-icon" width="149" height="84" srcset="http://192.168.64.2/wordpress/wp-content/uploads/2015/05/video-icon.png 456w, http://192.168.64.2/wordpress/wp-content/uploads/2015/05/video-icon-300x169.png 300w, http://192.168.64.2/wordpress/wp-content/uploads/2015/05/video-icon-250x141.png 250w" sizes="(max-width: 149px) 100vw, 149px" /></a>

<span style="color: #ffffff;"> </span>  
<a id="2"></a>

<h5 style="text-align: justify;">
</h5>

* * *

#### <span style="color: #2945a4;">Unconvex Nesting Optimization</span>

##### [Fabrizio Radaelli](https://www.italiancpp.org/speakers#fradaelli)

Optimization problems consists in finding the value of an optimization variable x that minimizes a function F(x) under some constrains. We can distinguish between convex and non-convex optimization problems: while it is certain to reach the optimal value for the optimization variable (i.e. the value of x for which F(x) is at its minimum) when solving problems of the first kind, in the non-convex case it is not guaranteed that the reached minimum of F(x) is a global or a local minimum.  
Despite optimization problems can be solved analytically, in the most of the cases it is requested a numerical approach to optimization. Machine learning, deep learning and, in general, artificial intelligence are based on numerical optimization of non-convex problems.

Here we present an algorithm we developed to solve a common case of non-convex problem: the 2D nesting problem. The goal of a nesting algorithm is to arrange some objects into a container, satisfying some arbitrary criteria (e.g. nest the objects in the most compact fashion). Our method is able to reach a solution in few ms; moreover it exploits a GPU-based geometrical approach and it can tackle nesting problems independently from the size and the shape of both objects and container.

After an introduction about non-convex problems, how they are defined and how they can be solved, we will present the principles of our nesting algorithm and discuss its potential. Next we will introduce a deep learning method to boost the nesting procedure, reaching high precision results without exploiting the nesting algorithm.

##### <span style="color: #339966;">Talk <strong>[ENG]</strong>, 50 minutes </span>

<a href="https://github.com/italiancpp/cppday18/blob/master/Unconvex%20Nesting%20Optimization%20-%20Fabrizio%20Radaelli.pptx" target="_blank" rel="noopener noreferrer"><img loading="lazy" class="alignnone wp-image-3669 size-full" src="http://www.italiancpp.org/wp-content/uploads/2014/10/slides_icon-e1423585085875.png" alt="slides" width="142" height="83" /></a>    <a href="https://www.youtube.com/watch?v=bDYjZsfbPkA" target="_blank" rel="noopener noreferrer"><img loading="lazy" class="alignnone wp-image-5060" src="http://www.italiancpp.org/wp-content/uploads/2015/05/video-icon.png" alt="video-icon" width="149" height="84" srcset="http://192.168.64.2/wordpress/wp-content/uploads/2015/05/video-icon.png 456w, http://192.168.64.2/wordpress/wp-content/uploads/2015/05/video-icon-300x169.png 300w, http://192.168.64.2/wordpress/wp-content/uploads/2015/05/video-icon-250x141.png 250w" sizes="(max-width: 149px) 100vw, 149px" /></a>

<span style="color: #ffffff;"> </span>  
<a id="3"></a>

&nbsp;

<span style="color: #ffffff;"> </span>

* * *

#### <span style="color: #2945a4;">A.I. dalla teoria alla pratica<br /> </span>

##### [Sebastiano Galazzo](https://www.italiancpp.org/speakers/#sgalazzo)

<p style="text-align: justify;">
  Una introduzione teorica agli algoritmi di machine learning ed A.I. seguita da una panoramica completa dei Microsoft Cognitive Services di Microsoft e la loro integrazione ed utilizzo pratico in C++ tramite il framework Qt.
</p>

<h5 style="text-align: justify;">
  <span style="color: #339966;">Talk <strong>[ITA]</strong>, 50 minutes</span>
</h5>

<a href="https://github.com/italiancpp/cppday18/blob/master/AI%20-%20Sebastiano%20Galazzo.pptx" target="_blank" rel="noopener noreferrer"><img loading="lazy" class="alignnone wp-image-3669 size-full" src="http://www.italiancpp.org/wp-content/uploads/2014/10/slides_icon-e1423585085875.png" alt="slides" width="142" height="83" /></a>    <a href="https://www.youtube.com/watch?v=J1fv33NBvP8" target="_blank" rel="noopener noreferrer"><img loading="lazy" class="alignnone wp-image-5060" src="http://www.italiancpp.org/wp-content/uploads/2015/05/video-icon.png" alt="video-icon" width="149" height="84" srcset="http://192.168.64.2/wordpress/wp-content/uploads/2015/05/video-icon.png 456w, http://192.168.64.2/wordpress/wp-content/uploads/2015/05/video-icon-300x169.png 300w, http://192.168.64.2/wordpress/wp-content/uploads/2015/05/video-icon-250x141.png 250w" sizes="(max-width: 149px) 100vw, 149px" /></a>

<span style="color: #ffffff;"> <a id="4"></a></span>

&nbsp;

<span style="color: #ffffff;"> </span>

* * *

#### <span style="color: #2945a4;">Exploring IoT with RTI DDS Connext<br /> </span>

##### [Giorgio Zoppi](https://www.italiancpp.org/speakers/#gzoppi)

<p style="text-align: justify;">
  RTI Connext DDS is a C++ framework designed to address the performance, scalability, security and resilience requirements of the Industrial Internet of Things.<br /> Its architecture is completely decentralized. Applications automatically discover each other and communicate peer-to-peer.<br /> Initally created for U.S.Navy, nowadays RTI Connext DDS has been employed in many different scenarios: medical hospital, automotive, real time network traffic. At first we will explain you the infrastracture of DDS, its distributed bus structure, performance, quality of service. In second instance we will use a real use case, vehicle tracking in C++14 using RTI DDS as data distribution bus and its &#8220;thing&#8221; discovery capabilities.<br /> We will show a fleet vehicle tracking application in C++14 where each vehicle send updates to the DDS and the UI will show us the state of the vehicle. As we guide you through this use case, we will talk about the architecture, the code, and the configuration in a way that it will make easy and fast the deployment of DDS.
</p>

<h5 style="text-align: justify;">
  <span style="color: #339966;">Short Talk <strong>[ENG],</strong> 20 minutes</span>
</h5>

<a href="https://github.com/italiancpp/cppday18/blob/master/Exploring%20IoT%20with%20RTI%20DDS.pdf" target="_blank" rel="noopener noreferrer"><img loading="lazy" class="alignnone wp-image-3669 size-full" src="http://www.italiancpp.org/wp-content/uploads/2014/10/slides_icon-e1423585085875.png" alt="slides" width="142" height="83" /></a>    <a href="https://www.youtube.com/watch?v=GLaj5Vm6jOE" target="_blank" rel="noopener noreferrer"><img loading="lazy" class="alignnone wp-image-5060" src="http://www.italiancpp.org/wp-content/uploads/2015/05/video-icon.png" alt="video-icon" width="149" height="84" srcset="http://192.168.64.2/wordpress/wp-content/uploads/2015/05/video-icon.png 456w, http://192.168.64.2/wordpress/wp-content/uploads/2015/05/video-icon-300x169.png 300w, http://192.168.64.2/wordpress/wp-content/uploads/2015/05/video-icon-250x141.png 250w" sizes="(max-width: 149px) 100vw, 149px" /></a>

<span style="color: #ffffff;"> </span>  
<a id="5"></a>  
<span style="color: #ffffff;"> </span>

&nbsp;

* * *

#### <span style="color: #2945a4;">Unevaluated operands: the SFINAE you don&#8217;t expect</span>

##### [Michele Caini](https://www.italiancpp.org/speakers/#mcaini)

<p style="text-align: justify;">
  C++11 gave us an extended set of contexts where unevaluated operands appear. SFINAE adepts said thank you and started doing strange things with them.<br /> Let&#8217;s discuss some modern techniques to solve ancient problems.
</p>

##### <span style="color: #339966;">Short Talk <strong>[ITA]</strong>, 20 minutes</span>

<a href="https://github.com/italiancpp/cppday18/blob/master/Unevaluated%20Operands%20-%20Michele%20Caini.pdf" target="_blank" rel="noopener noreferrer"><img loading="lazy" class="alignnone wp-image-3669 size-full" src="http://www.italiancpp.org/wp-content/uploads/2014/10/slides_icon-e1423585085875.png" alt="slides" width="142" height="83" /></a>    <a href="https://www.youtube.com/watch?v=BjVvCZgOE8E" target="_blank" rel="noopener noreferrer"><img loading="lazy" class="alignnone wp-image-5060" src="http://www.italiancpp.org/wp-content/uploads/2015/05/video-icon.png" alt="video-icon" width="149" height="84" srcset="http://192.168.64.2/wordpress/wp-content/uploads/2015/05/video-icon.png 456w, http://192.168.64.2/wordpress/wp-content/uploads/2015/05/video-icon-300x169.png 300w, http://192.168.64.2/wordpress/wp-content/uploads/2015/05/video-icon-250x141.png 250w" sizes="(max-width: 149px) 100vw, 149px" /></a>

<a id="6"></a>  
<span style="color: #ffffff;"> </span>

&nbsp;

* * *

#### <span style="color: #2945a4;">Macro free non intrusive runtime reflection system in C++</span>

##### [Michele Caini](https://www.italiancpp.org/speakers/#mcaini)

<p style="text-align: justify;">
  C++ and reflection are a long debated topic. Sooner or later we&#8217;ll see reflection finds its way into the standard. Until then, a non intrusive runtime reflection system is probably the most respectful thing you can do for your colleagues.
</p>

##### <span style="color: #339966;">Talk <strong>[ENG]</strong>, 50 minutes</span>

<a href="https://github.com/italiancpp/cppday18/blob/master/Runtime%20Reflection%20-%20Michele%20Caini.pdf" target="_blank" rel="noopener noreferrer"><img loading="lazy" class="alignnone wp-image-3669 size-full" src="http://www.italiancpp.org/wp-content/uploads/2014/10/slides_icon-e1423585085875.png" alt="slides" width="142" height="83" /></a>    <a href="https://www.youtube.com/watch?v=qGUKZWXkM7k" target="_blank" rel="noopener noreferrer"><img loading="lazy" class="alignnone wp-image-5060" src="http://www.italiancpp.org/wp-content/uploads/2015/05/video-icon.png" alt="video-icon" width="149" height="84" srcset="http://192.168.64.2/wordpress/wp-content/uploads/2015/05/video-icon.png 456w, http://192.168.64.2/wordpress/wp-content/uploads/2015/05/video-icon-300x169.png 300w, http://192.168.64.2/wordpress/wp-content/uploads/2015/05/video-icon-250x141.png 250w" sizes="(max-width: 149px) 100vw, 149px" /></a>

##### <a id="7"></a>  
<span style="color: #ffffff;"> </span>

&nbsp;

* * *

#### <span style="color: #2945a4;">Lessons Learned Developing Evolutionary Algorithms in C++<br /> </span>

##### [Manlio Morini](https://www.italiancpp.org/speakers/#mmorini)

Evolutionary optimisation frameworks offer significant &#8216;off-the-shelf&#8217; optimisation capabilities.  
Many C++ libraries enjoy on-going development and increasing maturity and they can be attractive options for programmers.

This talk describes some key aspects to make an informed choice:

  * evolutionary algorithms (EAs) and the AI / ML landscape;
  * how do they work;
  * (sub-)varieties of EAs;
  * when to prefer other approaches;
  * coding examples;
  * survey of available C++ frameworks.

It also deals with C++ techniques adopted in our open source Genetic Programming framework (Vita) regarding:

  * PRNG;
  * hashing;
  * small vector optimization.

##### <span style="color: #339966;">Talk <strong>[ITA]</strong>, 50 minutes</span>

<a href="https://github.com/italiancpp/cppday18/blob/master/Lessons%20Learned%20Developing%20Evolutionary%20Algorithms%20in%20C%2B%2B%20-%20Manlio%20Morini.pdf" target="_blank" rel="noopener noreferrer"><img loading="lazy" class="alignnone wp-image-3669 size-full" src="http://www.italiancpp.org/wp-content/uploads/2014/10/slides_icon-e1423585085875.png" alt="slides" width="142" height="83" /></a>    <a href="https://www.youtube.com/watch?v=WQoy2BxoCwg" target="_blank" rel="noopener noreferrer"><img loading="lazy" class="alignnone wp-image-5060" src="http://www.italiancpp.org/wp-content/uploads/2015/05/video-icon.png" alt="video-icon" width="149" height="84" srcset="http://192.168.64.2/wordpress/wp-content/uploads/2015/05/video-icon.png 456w, http://192.168.64.2/wordpress/wp-content/uploads/2015/05/video-icon-300x169.png 300w, http://192.168.64.2/wordpress/wp-content/uploads/2015/05/video-icon-250x141.png 250w" sizes="(max-width: 149px) 100vw, 149px" /></a>

##### <a id="8"></a><span style="color: #ffffff;"> </span>

&nbsp;

* * *

#### <span style="color: #2945a4;">Building a scientific C++ library as front-end of a Fortran library<br /> </span>

##### [Alfio Lazzaro](https://www.italiancpp.org/speakers/#alazzaro)

<p style="text-align: justify;">
  Fortran is one of the most used languages for scientific libraries in the High Performance Computing community. In the recent years, there has been a progressive shift in the community to use the C++ language for the development of new libraries. Therefore, it becomes important to allow codes written in the two languages to interplay. Here we present how we built a C++ API to the sparse matrix library DBCSR (Distributed Block Compressed Sparse Row). The library is written in Fortran and is freely available under GPL license. We present the design strategies implemented for the interoperability between C++ and Fortran.
</p>

##### <span style="color: #339966;">Talk <strong>[ENG]</strong>, 50 minutes</span>

##### <a id="9"></a>  
<span style="color: #ffffff;"> </span>

&nbsp;

&nbsp;

* * *

#### <span style="color: #2945a4;">Il punto su C++20<br /> </span>

##### [Alberto Barbati](https://www.italiancpp.org/speakers/#abarbati)

<p style="text-align: justify;">
  Il C++20 porterà molte importanti novità al linguaggio. Vedremo come concetti e contratti, feature già ufficialmente approvate, ma anche feature minori come i &#8220;class non type template parameters&#8221; possono cambiare profondamente il modo di programmare. Ne approfitteremo anche per vedere la situazione delle altre attesissime feature maggiori: moduli, coroutine e range, la cui inclusione nello standard è al momento ancora in discussione.
</p>

##### <span style="color: #339966;">Talk <strong>[ITA]</strong>, 50 minutes</span>

<a href="https://github.com/italiancpp/cppday18/blob/master/Il%20Punto%20su%20C%2B%2B20%20-%20Alberto%20Barbati.pdf" target="_blank" rel="noopener noreferrer"><img loading="lazy" class="alignnone wp-image-3669 size-full" src="http://www.italiancpp.org/wp-content/uploads/2014/10/slides_icon-e1423585085875.png" alt="slides" width="142" height="83" /></a>    <a href="https://www.youtube.com/watch?v=psZPax9TWrk" target="_blank" rel="noopener noreferrer"><img loading="lazy" class="alignnone wp-image-5060" src="http://www.italiancpp.org/wp-content/uploads/2015/05/video-icon.png" alt="video-icon" width="149" height="84" srcset="http://192.168.64.2/wordpress/wp-content/uploads/2015/05/video-icon.png 456w, http://192.168.64.2/wordpress/wp-content/uploads/2015/05/video-icon-300x169.png 300w, http://192.168.64.2/wordpress/wp-content/uploads/2015/05/video-icon-250x141.png 250w" sizes="(max-width: 149px) 100vw, 149px" /></a>

<span style="color: #ffffff;"> </span>  
<a id="10"></a>

&nbsp;

&nbsp;

* * *

#### <span style="color: #2945a4;">Cython: Importare il C++ in Python velocemente</span>

##### [Federico Pasqua](https://www.italiancpp.org/speakers/#fpasqua)

<p style="text-align: justify;">
  Un introduzione al Cython, un modo semplice e veloce di mettere in comunicazione C/C++ con il Python, seguita dall’analisi di un progetto PyGame + Cython preso come esempio.
</p>

##### <span style="color: #339966;">Talk <strong>[ITA]</strong>, 50 minutes</span>

<a href="https://github.com/italiancpp/cppday18/tree/master/Cython" target="_blank" rel="noopener noreferrer"><img loading="lazy" class="alignnone wp-image-3669 size-full" src="http://www.italiancpp.org/wp-content/uploads/2014/10/slides_icon-e1423585085875.png" alt="slides" width="142" height="83" /></a>    <a href="https://www.youtube.com/watch?v=Nxc7AQvH6Ws" target="_blank" rel="noopener noreferrer"><img loading="lazy" class="alignnone wp-image-5060" src="http://www.italiancpp.org/wp-content/uploads/2015/05/video-icon.png" alt="video-icon" width="149" height="84" srcset="http://192.168.64.2/wordpress/wp-content/uploads/2015/05/video-icon.png 456w, http://192.168.64.2/wordpress/wp-content/uploads/2015/05/video-icon-300x169.png 300w, http://192.168.64.2/wordpress/wp-content/uploads/2015/05/video-icon-250x141.png 250w" sizes="(max-width: 149px) 100vw, 149px" /></a>

##### <a id="11"></a><span style="color: #ffffff;"> </span>

&nbsp;

&nbsp;

* * *

#### <span style="color: #2945a4;">GIS in C++: cosa si nasconde dietro l&#8217;app mappe del tuo smarthphone?</span>

##### [Alberto Bignotti](https://www.italiancpp.org/speakers/#abignotti)

<p style="text-align: justify;">
  Verrà mostrata l’architettura di un componente C++ dedicato allo sviluppo di app Map centriche (Desktop/Mobile). In particolare vedremo alcuni concetti fondamentali di una applicazione GIS:
</p>

<ul style="text-align: justify;">
  <li>
    creazione di componenti grafici per il disegno di geometrie e immagini
  </li>
  <li>
    sistemi di coordinate, breve introduzione alla libreria proj4 (https://proj4.org/)
  </li>
  <li>
    interazione con la mappa, mouse + touch gestures
  </li>
  <li>
    manipolazione di geometrie in C++, breve introduzione alla libreria geos (http://trac.osgeo.org/geos)
  </li>
  <li>
    descrizione e esempio di alcuni standard per dati vettoriali e raster (WMS, OpenStreetMap, Bing Maps, GeoJson, WKB/WKT…)
  </li>
  <li>
    esempio di App QML (Desktop/Mobile) per mostrare gli argomenti trattati
  </li>
</ul>

<p style="text-align: justify;">
  Negli esempi, verrà utilizzato il framework Qt per l’interfaccia, C++14 per le componenti core.
</p>

##### <span style="color: #339966;">Talk <strong>[ITA]</strong>, 50 minutes</span>

<a href="https://github.com/italiancpp/cppday18/blob/master/GISinCPP.pptx" target="_blank" rel="noopener noreferrer"><img loading="lazy" class="alignnone wp-image-3669 size-full" src="http://www.italiancpp.org/wp-content/uploads/2014/10/slides_icon-e1423585085875.png" alt="slides" width="142" height="83" /></a>    <a href="https://www.youtube.com/watch?v=uhUdLcJqMl0" target="_blank" rel="noopener noreferrer"><img loading="lazy" class="alignnone wp-image-5060" src="http://www.italiancpp.org/wp-content/uploads/2015/05/video-icon.png" alt="video-icon" width="149" height="84" srcset="http://192.168.64.2/wordpress/wp-content/uploads/2015/05/video-icon.png 456w, http://192.168.64.2/wordpress/wp-content/uploads/2015/05/video-icon-300x169.png 300w, http://192.168.64.2/wordpress/wp-content/uploads/2015/05/video-icon-250x141.png 250w" sizes="(max-width: 149px) 100vw, 149px" /></a>

##### <a id="12"></a>  
<span style="color: #ffffff;"> </span>

&nbsp;