---
id: 6713
date: 2016-09-08T18:52:10+02:00
author: Stefano Famà
layout: revision
guid: http://www.italiancpp.org/2016/09/08/6712-revision-v1/
permalink: /2016/09/08/6712-revision-v1/
---
Ciao &#x1f642;  
Non ne sono sicuro, ma mi pare l&#8217;abbiano tolta col nuovo standard C++17, infatti è deprecata in C++14.  
Comunque qui puoi trovare la reference ufficiale: <a href="http://en.cppreference.com/w/cpp/algorithm/random_shuffle" target="_blank">std::shuffle</a>.

Prende un container che abbia un RandomAccessIterator e poi sistema in maniera casuale il contenuto.

Immagina di avere dei dadi ordinati:  
**1 2 3 4**  
Ora prendi i dadi, li metti in un bicchiere, agiti il tutto e li butti sul tavolo:  
**2 4 1 3**

Diciamo che il funzionamento è questo.

Tornando a spiegazioni più tecniche, questo algoritmo può usare anche dei generatori scelti dall&#8217;utente: <a href="http://en.cppreference.com/w/cpp/numeric/random" target="_blank">Pseudo-Random Generator</a>.  
Così puoi scegliere tu in che modo vengono &#8220;disordinati&#8221;.

Aggiungo anche un esempio:  
https://ideone.com/K9Et87

Come puoi vedere funziona anche con una stringa perché soddisfa i requisiti di shuffle.

Ti faccio anche notare però che il container viene **modificato**, ovverosia il **vector** e **string** che vado a passargli vengono modificati, l&#8217;ordinamento originale è perso.