---
id: 6725
date: 2016-09-09T16:41:05+02:00
author: Andrea
layout: revision
guid: http://www.italiancpp.org/2016/09/09/6716-revision-v1/
permalink: /2016/09/09/6716-revision-v1/
---
Ciao scusate ancora il disturbo, ma ho un problema sicuramente molto stupido&#8230; Nel programma, vorrei che se si inserisse un valore che non è compreso tra 1 e 3 (il range delle scelte che l&#8217;utente può fare), apparisse un messaggio di errore e si riaprisse la schermata per reinserire la scelta.. Il problema è che il programma va in loop e non so come bloccarlo. Posto il codice aggiornato della zona interessata:  
[cce_cpp]int main()  
{  
int scelta=0;  
do{

system(&#8220;cls&#8221;);  
cout <<&#8221; \___\___\___\___\___\___\___\___\___\___\___\___\___\___\___\___&#8221;<< endl;  
cout <<&#8220;| EQUAZIONI DI 1 E 2 GRADO |&#8221;<< endl; //INSERISCI COMANDO PER PULIRE SCHERMO  
cout <<&#8220;|\___\___\___\___\___\___\___\___\___\___\___\___\___\___\___\___|&#8221;<< endl;  
cout <<&#8220;| |&#8221;<< endl; //GUARDA PREFERITI PER EVITARE CHE UTENTE INSERISCA LETTERE O STRONZATE  
cout <<&#8220;| 1. Equazione di 1* grado. |&#8221;<< endl; // FARE IF PER FARE IMMETTERE SOLO VALORI COMPRESI TRA 1 E 3 NELLE VARIE TENDINE  
cout <<&#8220;| 2. Equazione di 2* grado. |&#8221;<< endl; // Delta maggiore di 0 nelle eq di secondo grado obbligatoriamente!  
cout <<&#8220;| 3. Esci |&#8221;<< endl;  
cout <<&#8220;| |&#8221;<< endl;  
cout <<&#8220;|\___\___\___\___\___\___\___\___\___\___\___\___\___\___\___\___|&#8221;<< endl;

cin >> scelta;

switch(scelta)  
{case(1):  
system (&#8220;cls&#8221;);  
eseguifunzione1(); // Richiamo funzione per equazione primo grado.  
break;  
case (2):  
system (&#8220;cls&#8221;);  
eseguifunzione2(); // Richiamo funzione per equazione terzo grado.  
break;  
case (3):  
exit(0);  
default:  
cout << &#8220;Inserisci dei parametri corretti.&#8221;<<endl;  
break;  
}  
}while (scelta!=1, scelta!=2, scelta != 3);  
system(&#8220;pause&#8221;);  
return 0;}[/cce_cpp]