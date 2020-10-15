---
id: 7224
date: 2016-12-24T15:40:04+01:00
author: Stefano Famà
layout: revision
guid: http://www.italiancpp.org/2016/12/24/7223-revision-v1/
permalink: /2016/12/24/7223-revision-v1/
---
Buondì.  
Avete già trovato un modo per stampare questi caratteri, basta usare l&#8217;escape \xNN, sostituite ad NN le cifre esadecimali e siete a posto &#x1f642;

Vi consiglio questa pagina che contiene i caratteri ascii: <a href="http://www.asciitable.com/" target="_blank">ASCII Table</a>.

Comunque qua rientriamo in situazioni particolari in quanto dovete assicurarvi che il terminale che usate (la finestra nera, prompt dei comandi in Windows) supporti questi caratteri.  
Windows necessita dei caratteri di escape, dunque dovete per forza usare \xNN.  
Linux invece permette di usare direttamente il carattere.

Su una macchina Windows, viene stampato correttamente quello Escape.  
Su Linux invece è l&#8217;opposto.

[cce_cpp]#include <iostream>  
int main(){  
std::cout << &#8220;Escape: \x8a&#8221; << std::endl;  
std::cout << &#8220;Regular: è&#8221; << std::endl;  
}[/cce_cpp]