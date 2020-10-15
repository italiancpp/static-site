---
id: 7312
title: CPPRest Casablanca for Facebook API , strano errore LNK1104 e dubbi affini
date: 2017-01-18T12:49:20+01:00
author: kenhero
layout: revision
guid: http://www.italiancpp.org/2017/01/18/7307-revision-v1/
permalink: /2017/01/18/7307-revision-v1/
---
Buongiorno a tutti,  
spero di aver postato nella sezione più corretta.  
Devo prepararmi per un colloquio di lavoro all&#8217;utilizzo di questa SDK &#8220;Casablanca&#8221; di Microsoft. Essenzialmente è un project per la programmazione di API asincrona client-server cloud based.  
Le caratteristiche di base sono le seguenti:  
Features &#8211; HTTP client/server, JSON, URI, asynchronous streams, WebSockets client, oAuth  
PPL Tasks &#8211; A powerful model for composing asynchronous operations based on C++ 11 features  
Platforms &#8211; Windows desktop, Windows Store, Windows Phone, Ubuntu, OS X, iOS, and Android  
Support for Visual Studio 2012, 2013, and 2015 with debugger visualizers  
NuGet package with binaries for Windows and Android platforms

Il sito ufficiale da cui scaricare la solution per VS2013 è Codeplex ma è stato spostato su GitHub.  
Purtroppo nè su CodePlex nè sul forum di VS mi rispondono per cui sono praticamente alla mia ultima spiaggia &#x1f642;

All&#8217;interno della solution scaricabile da qui:

[](https://github.com/Microsoft/cpprestsdk/)

Esistono degli esempi che spiegano il funzionamento generale per progettare questi servizi REST in C++ ,come per esempio progettare dei client HTTP che gestiscono la comunicazione tramite programmazione asincrona con il lato server dotato di API.

Qui c&#8217;è una breve spiegazione degli esempi che possono essere buildati  
[](https://github.com/Microsoft/cpprestsdk/wiki/Samples)

In particolare i miei problemi sorgono con l&#8217;utilizzo dell&#8217;esempio della C++ API per connettersi a Facebook  
[](https://blogs.msdn.microsoft.com/vcblog/2013/03/21/connecting-to-facebook-with-the-c-rest-sdk/)

Per utilizzare questa API devo loggarmi al mio account Fb,e registrarmi come developer (basta andare su http://developers.facebook.com.)

Devo creare una mia APP di test e settare alcuni parametri ,come spiegato nella guida.  
Essenzialmente mi serve per ottenere la App ID e la API key che mi servono per poter effettuare la connessione HTTP. I problemi sorgono successivamente e sono due :  
1)Se buildo la intera solution o due errori del linker ,e sono anche strani (allego immagine)

![VS error](//s29.postimg.org/j8cav7o7n/issue.png[/img][/url]) 

\[url=https://postimg.org/image/j8cav7o7n/\]\[img\]https://s29.postimg.org/646qiiw5z/issue.png\[/img\]\[/url\][url=https://postimage.org/index.php?lang=italian]free image hosting[/url]

Dalla solution nn mi pare ci sia un legame tra il Project oggetto dell&#8217;errore (cpprestsdk120.winrt) e il Project di riferimento (FacebookDemo120) per cui escludendolo dalla compilazione worka.

Si avvia finalmente FacebookDemo120 ma nel momento in cui provo a loggarmi sul mio account (cliccando su login) ho il seguente errore.

![Error runtime](//s24.postimg.org/5ukb8zrf5/issue2.png[/img][/url]) 

\[url=https://postimg.org/image/5ukb8zrf5/\]\[img\]https://s24.postimg.org/mv37ho4gl/issue2.png\[/img\]\[/url\][url=https://postimage.org/index.php?lang=italian]upload immagini[/url]

Purtroppo essendo programmazione parallela è anche difficile (almeno per le mie conosenze attuali) fare testing per cui se qualcuno ha qualche dritta o suggerimento in merito mi toglierebbe un po&#8217; di disperazione &#x1f642;