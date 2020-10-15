---
id: 6718
date: 2016-09-09T14:26:39+02:00
author: Stefano Famà
layout: revision
guid: http://www.italiancpp.org/2016/09/09/6717-revision-v1/
permalink: /2016/09/09/6717-revision-v1/
---
_Hai dimenticato di chiudere il tag /code_ &#x1f61b;

<a href="http://en.cppreference.com/w/cpp/io/manip/endl" target="_blank">std::endl</a> non pulisce lo schermo, guarda bene cosa fa.

Innanzitutto metti un **char** al posto di **int** come scelta, perché se no il programma si impianta.

Seconda cosa, io personalmente metto sempre **** (**zero**) come scelta per uscire, così nel **loop** mi basta mettere **scelta != &#8216;0&#8217;**, altrimenti come fai tu sei costretto a modificare la condizione del loop nel caso dovessi aggiungere una nuova funzionalità.

Ultimo appunto, benché non sia scorretto, credo sia più corretto non uscire con **exit(0);** nello **switch**, ma è solo un appunto personale.

Così funziona:  
[cce_cpp]char scelta = &#8216;0&#8217;;  
do {  
// PRINT MENU

cin >> scelta;  
switch (scelta)  
{  
case &#8216;1&#8217;:  
cout << &#8220;FUNC1&#8221; << endl;  
break;

case &#8216;2&#8217;:  
cout << &#8220;FUNC2&#8221; << endl;  
break;

case &#8216;0&#8217;:  
cout << &#8220;EXIT&#8221; << endl;  
break;

default:  
cout << &#8220;ERR&#8221; << endl;  
break;

}  
} while (scelta != &#8216;0&#8217;);[/cce_cpp]

Ah ho notato una cosa, che non avevo preso in considerazione.  
Se l&#8217;utente immette più di un carattere il loop viene eseguito N volte.  
Prova ad inserire nella scelta questo:  
**10**  
**abcde**