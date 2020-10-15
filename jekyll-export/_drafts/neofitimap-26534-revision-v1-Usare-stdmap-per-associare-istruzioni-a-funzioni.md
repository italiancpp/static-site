---
id: 6535
title: Usare std::map per associare istruzioni a funzioni
date: 2016-08-15T12:39:53+02:00
author: marco
layout: revision
guid: http://www.italiancpp.org/2016/08/15/6534-revision-v1/
permalink: /2016/08/15/6534-revision-v1/
---
Buongiorno.  
Come da titolo io volevo chiedervi un consiglio sull&#8217;utilizzo di una mappa per chiamare delle funzioni fornendo una stringa.  
In pratica, quando torno dalle vacanze, vorrei creare la mia versione di QtSPIM.  
Per chi non lo conoscesse su tratta di un emulatore del microprocessore MIPS.  
Dato che l&#8217;utente scriverà in Assembly, dovrò eseguire le istruzioni man mano che faccio il parsing.

Ecco, io avevo pensato di salvare in una mappa il nome della funzione, che corrisponderà all&#8217;istruzione MIPS, e un puntatore alla funzione corrispondente.

Es:  
[cce_cpp]  
map<string, function> m;  
m.insert(make_pair(&#8220;add&#8221;,function<void(int, int, int)>));  
m\[&#8220;add&#8221;\]($0,$1,$2);[/cce_cpp]

Secondo voi è fattibile una cosa del genere?

Grazie,  
Stefano