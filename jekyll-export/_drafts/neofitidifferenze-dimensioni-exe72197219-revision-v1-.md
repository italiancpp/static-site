---
id: 7220
date: 2016-12-23T13:38:17+01:00
author: Stefano Famà
layout: revision
guid: http://www.italiancpp.org/2016/12/23/7219-revision-v1/
permalink: /2016/12/23/7219-revision-v1/
---
Provo a spiegare in maniera un po&#8217; astratta e grossolana (chiedo venia &#x1f641; ).  
Una **libreria** può essere vista come un **libro**.  
Le **parole** del libro sono il suo codice.  
Lo scopo del libro è di essere letto più volte senza doverlo copiare ogni volta, lo scrivi 1 volta sola e poi lo rileggi quante volte vuoi.

Banalmente, scrivere un programma, consiste nel scrivere un nuovo libro.  
Dunque, va da se, che puoi utilizzare delle librerie già esistenti per non dover riscrivere tutto da capo.  
L&#8217;uso di librerie si divide principalmente in 2 modi (qua rientriamo nel lavoro del Linker se non erro)

  1. Collegamento **Dinamico**
  2. Collegamento **Statico**

Collegamento **Dinamico**  
Il codice del tuo programma e della libreria è &#8220;separato&#8221;.  
In poche parole tu dici, guarda che &#8220;in questo punto qua&#8221;, devo usare il codice della libreria.  
Ok, allora viene caricata in memoria la **DLL**, e viene eseguito il suo codice.  
Le dimensioni dell&#8217;eseguibile variano a seconda di quanto codice c&#8217;è scritto!  
Dunque, va da se, che se colleghi in maniera **dinamica** qualche libreria, il tuo eseguibile ha una specie di &#8220;collegamento&#8221;.  
Pensalo come un link ad una pagina web, piuttosto che copiare ed incollare il contenuto di una pagina, metti direttamente il link.

Collegamento **Statico**  
Nel collegamento statico invece, si ha l&#8217;opposto del dinamico.  
In pratica il codice della libreria viene **aggiunto** al tuo eseguibile!  
Quindi stai &#8220;copiando ed incollando&#8221; il codice della libreria nel tuo eseguibile, ecco perché risulta più grande!

Le differenze non sono tutte qua, in realtà bisognerebbe entrare più nel dettaglio, cosa che io non posso fare perché non ho conoscenze così profonde di questo argomento, comunque trovi più informazioni su Internet.

Ah, tornando a noi.  
Sostanzialmente Visual Studio collega dinamicamente il programma, mentre Code::Blocks lo fa staticamente &#x1f642;

Spero tu abbia capito &#x1f642;