---
id: 6479
date: 2016-08-05T18:17:01+02:00
author: Stefano Famà
layout: revision
guid: http://www.italiancpp.org/2016/08/05/6477-revision-v1/
permalink: /2016/08/05/6477-revision-v1/
---
Ciao Andrea,  
quando posti del codice usa il tag code, lo trovi appena sopra quando scrivi un post.

Detto ciò, ti consiglio di farlo sotto forma di funzione piuttosto che IF così, così è già pronto.

Io ho fatto così:  
[cce_cpp]int compareTo(const Data& data1, const Data& data2) {  
if (data1.anno < data2.anno) {  
return -1;  
}  
else if (data1.anno > data2.anno) {  
return 1;  
}  
else { // anno uguale  
if (data1.mese < data2.mese) {  
return -1;  
}  
else if (data1.mese > data2.mese) {  
return 1;  
}  
else { // mese uguale  
if (data1.giorno < data2.giorno) {  
return -1;  
}  
else if (data1.giorno > data2.giorno) {  
return 1;  
}  
else { // giorno uguale  
return 0;  
}  
}  
}  
}[/cce_cpp]

Ho notato ora che sei incappato in uno degli errori classici 😛

if(d1.m **=** d2.m)

Nel C, C++ e altri linguaggi (non tutti) questa espressione risulterà sempre VERA.  
Perché tu non stai comparando, stai assegnando.  
Hai solo dimenticato un **=**

Suggerimenti:  
vorrei solo aggiungere che quando fai tante comparazioni con gli IF, usa in maniera più completa il costrutto IF-ELSE.  
Cioè, tu stai controllando l&#8217;anno?  
Anno1 > Anno2 -> falso  
Anno1 < Anno2 -> falso  
Allora sicuramente è uguale.

Non so se l&#8217;avete già fatto ma il costrutto if-else funziona in 3 modi:  
**Primo**  
[cce_cpp]if(condizione){  
// fa qualcosa  
}[/cce_cpp]  
**Secondo**  
[cce_cpp]if(condizione){  
// fa qualcosa  
} else {  
// altrimenti fai questo  
}  
[/cce_cpp]  
**Terzo**  
[cce_cpp]if(condizione){  
// fa qualcosa  
} else if(condizione){  
// fai altro  
} else if(condizione){  
// fai altro 2.0  
} else {  
// altrimenti fai questo  
}[/cce_cpp]

Nel primo caso se la condizione è vera, esegue il codice all&#8217;interno del IF e poi continua l&#8217;esecuzione.  
Nel secondo caso esegue SICURAMENTE uno dei due, perché l&#8217;ELSE viene eseguito ogni qual volta l&#8217;IF è falso.  
Nel terzo caso puoi usare più ELSE IF per testare tutte le condizioni che vuoi.

Ti ho detto ciò perché tu controlli solo con IF, dunque fai delle comparazioni in più non necessarie, es.:  
if(anno1 > anno2) printf(&#8220;1&#8221;);  
if(anno1 < anno2) printf(&#8220;-1&#8221;);  
if(anno1 == anno2) printf(&#8220;0&#8221;);

Qui fai 3 comparazioni, ma in realtà 1 sola di esse sarà vera.

Spero di esserti stato utile 🙂