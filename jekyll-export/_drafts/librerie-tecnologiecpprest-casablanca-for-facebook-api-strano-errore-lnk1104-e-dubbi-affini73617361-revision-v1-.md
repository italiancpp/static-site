---
id: 7376
date: 2017-01-21T21:45:53+01:00
author: Raffaele Rialdi
layout: revision
guid: http://www.italiancpp.org/2017/01/21/7361-revision-v1/
permalink: /2017/01/21/7361-revision-v1/
---
L&#8217;errore del linker credo sia dovuto a un problema con i tuoi setting (cartella errata, disco pieno, o similare).  
Il modo più semplice per referenziare il REST SDK è quello di aggiungere le reference via nuget (plugin di pacchettizzazione di Microsoft) oppure il più recente VCPkg:  
https://github.com/Microsoft/vcpkg/tree/master/ports/cpprestsdk  
La demo che avevo fatto l&#8217;anno scorso alla ItalianCpp conference usava nuget ma attualmente viene spinto di più VCPkg perché risolve alcune problematiche. Ti consiglio di provare con questo (segui le istruzioni in home).

Per quanto riguarda l&#8217;asincrono, ti converrebbe usare co_await (anche questo presentato nella conference) perché ti risparmia molti grattacapi.

Infine occhio a non confondere le librerie desktop per quelle winrt. Sono mondi diversi e non li devi mischiare.

Io comunque uso Casablanca /REST SDK in produzione in diversi progetti senza grossi problemi. Il codice che mi funziona usa diverse parti dell&#8217;sdk:  
&#8211; json serializzazione / deserializzazione  
&#8211; http listener  
&#8211; http client  
&#8211; websocket client  
&#8211; utility varie

La parte di autenticazione l&#8217;ho fatta a mano e non ho provato l&#8217;integrazione con FB.