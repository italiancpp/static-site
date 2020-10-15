---
id: 8288
title: Sessioni C++ Day 2017
date: 2017-10-13T09:02:41+02:00
author: marco
layout: page
guid: http://www.italiancpp.org/?page_id=8288
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
#### <a href="http://www.italiancpp.org/cppday17" target="_blank" rel="noopener noreferrer">Pagina dell&#8217;evento</a>

<span style="color: #ffffff;"> </span>

#### <a href="https://github.com/italiancpp/cppday17" target="_blank" rel="noopener noreferrer">Slides repository</a>

#### <span style="color: #ffffff;"> </span>  
<a id="1"></a>  
<span style="color: #ffffff;"> </span>

* * *

#### <span style="color: #2945a4;">Immediate Mode Graphical User Interfaces in C++</span>

##### <a href="http://italiancpp.org/speakers#ste-cristiano" target="_blank" rel="noopener noreferrer">Stefano Cristiano</a>

<p style="text-align: justify;">
  Most graphical user interface paradigms are based on the retained mode pattern.<br /> This means building an object graph describing the user interface, listening to events in callbacks and modifying the object graph.<br /> Very often a lot of code and conversion between basic types like strings and vectors are needed to keep the GUI in sync with application data model.<br /> The browser Document Object Model (DOM) is one of the most developed forms of retained mode system.<br /> In recent years a new paradigm commonly referred as &#8220;immediate mode&#8221; changes perspective on how to create a graphical user interface.<br /> It&#8217;s not entirely new, as it has been used in the field of game programming since long time, but only in the last years it has been re-discovered and formally defined as an alternative to retained mode systems.<br /> The key elements of Immediate Mode Graphical User Interfaces (IMGUI) are:
</p>

<p style="text-align: justify;">
  1) Minimise or remove model state typically cached in retained mode gui controls (stateless controls)<br /> 2) Define the user interface by calling functions that generates graphics and modifies model data in place (functional style, creating ui by coding)<br /> 3) Redraw the entire user interface at every frame or in general when there are user inputs or model data changes
</p>

<p style="text-align: justify;">
  This approach considerably lowers application complexity but is not without caveats.<br /> We will explore the concepts of retained and immediate mode gui, with advantages and disadvantages of each approach.<br /> We will then describe a very popular open source implementation called &#8220;dear imgui&#8221;, providing code examples in C++.<br /> Finally we will show real world use case of imgui in industrial robotic vision field.
</p>

<h5 style="text-align: justify;">
  <span style="color: #339966;">Talk da 60&#8242;</span>
</h5>

<a href="https://github.com/italiancpp/cppday17/blob/master/Immediate%20Mode%20User%20Interface%20in%20C%2B%2B%20-%20Stefano%20Cristiano.pdf" target="_blank" rel="noopener noreferrer"><img loading="lazy" class="alignnone wp-image-3669 size-full" src="http://www.italiancpp.org/wp-content/uploads/2014/10/slides_icon-e1423585085875.png" alt="slides" width="142" height="83" /></a>    <a href="https://youtu.be/Sx7vPcUVQX4" target="_blank" rel="noopener noreferrer"><img loading="lazy" class="alignnone wp-image-5060" src="http://www.italiancpp.org/wp-content/uploads/2015/05/video-icon.png" alt="video-icon" width="149" height="84" srcset="http://192.168.64.2/wordpress/wp-content/uploads/2015/05/video-icon.png 456w, http://192.168.64.2/wordpress/wp-content/uploads/2015/05/video-icon-300x169.png 300w, http://192.168.64.2/wordpress/wp-content/uploads/2015/05/video-icon-250x141.png 250w" sizes="(max-width: 149px) 100vw, 149px" /></a>

<h5 style="text-align: justify;">
</h5>

<h5 style="text-align: justify;">
  <a id="2"></a><br /> <span style="color: #ffffff;"> </span>
</h5>

* * *

#### <span style="color: #2945a4;">Intelligenza Artificiale oggi</span>

##### [Sebastiano Galazzo](http://italiancpp.org/speakers#sgalazzo)

<p style="text-align: justify;">
  Sessione prettamente teorica, avrà lo scopo di approfondire cosa è realmente, ma soprattutto cosa non è, l&#8217;intelligenza artificiale ad oggi.<br /> Verrà esploso in dettaglio lo stato dell&#8217;arte ad oggi su questo tema per passare ad approfondimenti teorici dettagliati sui principali algoritmi di machine learning in uso come regressione logistica e reti neurali, quindi un approfondimento di implementazioni da zero di una rete neurale in C++.
</p>

##### <span style="color: #339966;">Talk da 60&#8242;</span>

<a href="https://github.com/italiancpp/cppday17/blob/master/Intelligenza%20Artificiale%20Oggi%20-%20Sebastiano%20Galazzo.pptx" target="_blank" rel="noopener noreferrer"><img loading="lazy" class="alignnone wp-image-3669 size-full" src="http://www.italiancpp.org/wp-content/uploads/2014/10/slides_icon-e1423585085875.png" alt="slides" width="142" height="83" /></a>    <a href="https://youtu.be/I7KtY4lACLQ" target="_blank" rel="noopener noreferrer"><img loading="lazy" class="alignnone wp-image-5060" src="http://www.italiancpp.org/wp-content/uploads/2015/05/video-icon.png" alt="video-icon" width="149" height="84" srcset="http://192.168.64.2/wordpress/wp-content/uploads/2015/05/video-icon.png 456w, http://192.168.64.2/wordpress/wp-content/uploads/2015/05/video-icon-300x169.png 300w, http://192.168.64.2/wordpress/wp-content/uploads/2015/05/video-icon-250x141.png 250w" sizes="(max-width: 149px) 100vw, 149px" /></a>

<span style="color: #ffffff;"> </span>  
<a id="3"></a>  
<span style="color: #ffffff;"> </span>

* * *

#### <span style="color: #2945a4;">(Slightly) Smarter smart pointers<br /> </span>

##### <a href="http://italiancpp.org/speakers#carlo-pescio" target="_blank" rel="noopener noreferrer">Carlo Pescio</a>

<p style="text-align: justify;">
  L&#8217;uso degli smart pointers rende la scrittura del codice C++ più rapida e sicura, e più in generale permette una progettazione robusta delle politiche di ownership ed una rappresentazione esplicita di tali politiche nel nostro codice.<br /> Tuttavia gli smart pointers a cui siamo abituati (mi riferisco in particolare ai puntatori con reference count, pensati per risorse condivise) hanno un overhead non trascurabile, sia in termini di spazio che di tempo. D&#8217;altra parte, dopo tutti questi anni sembra improbabile migliorare in modo significativo le performance degli shared pointers.<br /> Per chi non vuole arrendersi, una buona notizia arriva da una serie di esperimenti, che di fatto forniscono una specie di meccanica statistica dei reference count nei programmi object oriented, da cui possiamo trarre ispirazione per creare uno smart pointer piuttosto interessante, che in media occupa meno spazio ed ha prestazioni migliori (ad es., in un benchmark misto con uso di algoritmi e contenitori STL, risulta oltre 2 volte piu&#8217; veloce rispetto a std::shared_ptr).<br /> Il talk riprende le più comuni implementazioni di shared pointers, inclusa ovviamente quella standard, le confronta con alcuni semplici benchmark, spiega le basi statistiche e mostra le parti più rilevanti dell&#8217;implementazione dello shared pointer alternativo, ma anche il processo &#8220;creativo&#8221; che ha portato, in realtà con un percorso piuttosto lungo, a concepire questa nuova implementazione.
</p>

<h5 style="text-align: justify;">
  <span style="color: #339966;">Talk da 60&#8242;</span>
</h5>

<a href="https://github.com/italiancpp/cppday17/blob/master/(Slightly)%20Smarter%20Smart%20Pointers%20-%20Carlo%20Pescio.pdf" target="_blank" rel="noopener noreferrer"><img loading="lazy" class="alignnone wp-image-3669 size-full" src="http://www.italiancpp.org/wp-content/uploads/2014/10/slides_icon-e1423585085875.png" alt="slides" width="142" height="83" /></a>    <a href="https://youtu.be/Ywehms9PtVY" target="_blank" rel="noopener noreferrer"><img loading="lazy" class="alignnone wp-image-5060" src="http://www.italiancpp.org/wp-content/uploads/2015/05/video-icon.png" alt="video-icon" width="149" height="84" srcset="http://192.168.64.2/wordpress/wp-content/uploads/2015/05/video-icon.png 456w, http://192.168.64.2/wordpress/wp-content/uploads/2015/05/video-icon-300x169.png 300w, http://192.168.64.2/wordpress/wp-content/uploads/2015/05/video-icon-250x141.png 250w" sizes="(max-width: 149px) 100vw, 149px" /></a>

<span style="color: #ffffff;"> <a id="4"></a></span>

<span style="color: #ffffff;"> </span>

* * *

#### <span style="color: #2945a4;">C/C++ interoperability with other languages<br /> </span>

##### <a href="http://italiancpp.org/speakers#abignotti" target="_blank" rel="noopener noreferrer">Alberto Bignotti</a>

<p style="text-align: justify;">
  La comunità C/C++ è molto vasta e lo standard corrente (C++ 17) è il risultato di anni di miglioramenti. Inoltre, gli strumenti di sviluppo integrati vengono costantemente arricchiti e quindi esistono librerie per affrontare qualsiasi problema informatico. Tuttavia esistono linguaggi alternativi e complementari che possono offrire caratteristiche interessanti (come semplicità d&#8217;uso e scalabilità) e vantano comunità significative.
</p>

L&#8217;obbiettivo è quello di studiare con esempi pratici un prodotto che offra una base C++ e possa essere esteso usando i linguaggi di programmazione più diffusi (ad esempio Java, JavaScript, C# ecc&#8230;). Nel corso della sessione, vedremo come implementare un server C/C++ che espone un set di servizi GIS, una App Web based (pure HTML/JavaScript) che li richiama e mostra i risultati su una mappa geografica.

<h5 style="text-align: justify;">
  <span style="color: #339966;">Talk da 60&#8242;</span>
</h5>

<a href="https://github.com/italiancpp/cppday17/blob/master/C%2B%2B%20interoperability%20with%20other%20languages%20-%20Alberto%20Bignotti.pdf" target="_blank" rel="noopener noreferrer"><img loading="lazy" class="alignnone wp-image-3669 size-full" src="http://www.italiancpp.org/wp-content/uploads/2014/10/slides_icon-e1423585085875.png" alt="slides" width="142" height="83" /></a>    <a href="https://youtu.be/_wSs8J4ZBrU" target="_blank" rel="noopener noreferrer"><img loading="lazy" class="alignnone wp-image-5060" src="http://www.italiancpp.org/wp-content/uploads/2015/05/video-icon.png" alt="video-icon" width="149" height="84" srcset="http://192.168.64.2/wordpress/wp-content/uploads/2015/05/video-icon.png 456w, http://192.168.64.2/wordpress/wp-content/uploads/2015/05/video-icon-300x169.png 300w, http://192.168.64.2/wordpress/wp-content/uploads/2015/05/video-icon-250x141.png 250w" sizes="(max-width: 149px) 100vw, 149px" /></a>

<span style="color: #ffffff;"> </span>  
<a id="5"></a>  
<span style="color: #ffffff;"> </span>

* * *

#### <span style="color: #2945a4;">C++ e UI: un approccio alternativo</span>

##### <a href="http://italiancpp.org/speakers#dpallastrelli" target="_blank" rel="noopener noreferrer">Daniele Pallastrelli</a>

<p style="text-align: justify;">
  Nel mio intervento propongo una soluzione alternativa all&#8217;annoso problema delle UI per applicazioni desktop, che ultimamente ho adottato con successo in diversi progetti reali.<br /> Mostrerò come declinarla nel caso di applicazioni C++ e descriverò com&#8217;è possibile organizzare questo tipo di software.
</p>

##### <span style="color: #339966;">Talk da 60&#8242;</span>

<a href="https://github.com/italiancpp/cppday17/blob/master/C%2B%2B%20and%20UI%20un%20approccio%20alternativo%20-%20Daniele%20Pallastrelli.pdf" target="_blank" rel="noopener noreferrer"><img loading="lazy" class="alignnone wp-image-3669 size-full" src="http://www.italiancpp.org/wp-content/uploads/2014/10/slides_icon-e1423585085875.png" alt="slides" width="142" height="83" /></a>    <a href="https://youtu.be/9buNhizFmzc" target="_blank" rel="noopener noreferrer"><img loading="lazy" class="alignnone wp-image-5060" src="http://www.italiancpp.org/wp-content/uploads/2015/05/video-icon.png" alt="video-icon" width="149" height="84" srcset="http://192.168.64.2/wordpress/wp-content/uploads/2015/05/video-icon.png 456w, http://192.168.64.2/wordpress/wp-content/uploads/2015/05/video-icon-300x169.png 300w, http://192.168.64.2/wordpress/wp-content/uploads/2015/05/video-icon-250x141.png 250w" sizes="(max-width: 149px) 100vw, 149px" /></a>