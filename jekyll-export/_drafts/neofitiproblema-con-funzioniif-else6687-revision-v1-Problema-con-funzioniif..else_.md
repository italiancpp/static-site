---
id: 6690
title: Problema con funzioni/if..else
date: 2016-09-05T23:12:26+02:00
author: Andrea
layout: revision
guid: http://www.italiancpp.org/2016/09/05/6687-revision-v1/
permalink: /2016/09/05/6687-revision-v1/
---
Salve a tutti, mi stavo dilettando nel fare un programma che calcolasse equazioni di primo/secondo grado, ma sono inceppato in diverse difficoltà. Adesso metterò il codice, ma prima vi pongo i miei dilemmi.  
1) Una volta finito il calcolo dell&#8217;equazione, come devo impostare il ciclo per far si che l&#8217;utente possa tornare alla &#8220;home&#8221; per selezionare un nuovo calcolo?  
2) Se provo a calcolare le soluzioni dell&#8217;equazione di primo grado inserendo come parametro a=3 e b=9, invece di fermarsi mostra anche la schermata dell&#8217;equazione di secondo grado.. cosa che non gli altri numeri non fa. Non capisco a cosa sia dovuto ciò..  
EDIT: Ho risolto il punto due mettendo subito dopo la riga 41 l&#8217;istruzione break, se c&#8217;è un altro modo per risolvere il problema non esitate a scrivere!  
3) Potreste dirmi come fare per semplificare una frazione nel momento in cui il numeratore (b) sia minore di (a), nel caso in cui sia possibile?  
Grazie mille! Se le domande vi risultano ambigue non esitate a chiedere, anche se guardando il codice dovreste capire autonomamente.  
P.S. Mi scuso se il codice risulta essere macchinoso o non ottimizzato, ma ancora è in fase di elaborazione (stavo giusto iniziando l&#8217;equazioni di secondo grado mentre mi sono accorto del problema) e sono ancora alle prime armi! Ecco qui il codice:  
[cce_cpp]#include <iostream>

using namespace std;

int eq1(int x, int y);

int main()  
{

int i,a1,b1,riseq1,j,a2,b2,c=0;

cout << &#8220;\___\___\___\___\___\___\___\___\___\___\___\___\___\___\___\___&#8221;<< endl;  
cout <<&#8220;| EQUAZIONI DI 1 E 2 GRADO |&#8221;<< endl;  
cout <<&#8220;|\___\___\___\___\___\___\___\___\___\___\___\___\___\___\___\___|&#8221;<< endl;  
cout <<&#8220;| |&#8221;<< endl;  
cout <<&#8220;| 1. Equazione di 1* grado. |&#8221;<< endl;  
cout <<&#8220;| 2. Equazione di 2* grado. |&#8221;<< endl;  
cout <<&#8220;| 3. Esci |&#8221;<< endl;  
cout <<&#8220;| |&#8221;<< endl;  
cout <<&#8220;|\___\___\___\___\___\___\___\___\___\___\___\___\___\___\___\___|&#8221;<< endl;

cin >> i;  
switch(i)  
case(1):  
{  
cout << &#8220;\___\___\___\___\___\___\___\___\___\___\___\___\___\___\___\___&#8221;<< endl;  
cout <<&#8220;| EQUAZIONE DI 1* GRADO |&#8221;<< endl;  
cout <<&#8220;|\___\___\___\___\___\___\___\___\___\___\___\___\___\___\___\___|&#8221;<< endl;  
cout <<&#8220;| |&#8221;<< endl;  
cout <<&#8220;| |&#8221;<< endl;  
cout <<&#8220;| ax+b=0 |&#8221;<< endl;  
cout <<&#8220;| |&#8221;<< endl;  
cout <<&#8220;| |&#8221;<< endl;  
cout <<&#8220;|\___\___\___\___\___\___\___\___\___\___\___\___\___\___\___\___|&#8221;<< endl;

cout << &#8220;Inserire i parametri a e b interposti da uno spazio.&#8221;<< endl;  
cin >> a1;  
cin >> b1;  
riseq1=eq1(a1,b1); // Richiamo la funzione int eq1  
//if(b1%a1!=0)  
// (-(b1)) << &#8220;/&#8221; << a1;  
// else  
// (-(b1/a1));  
if(b1%a1==0){  
if(b1>0)  
cout << &#8220;La soluzione dell&#8217;equazione &#8220;<< a1<< &#8220;x+&#8221;<<b1 <<&#8220;=0 e&#8217; pari a x=&#8221;<< (-(b1/a1));  
else  
cout << &#8220;La soluzione dell&#8217;equazione &#8220;<< a1<< &#8220;x&#8221;<<b1 <<&#8220;=0 e&#8217; pari a x=&#8221;<< (-(b1/a1));  
}  
else  
{if(b1>0)  
cout << &#8220;La soluzione dell&#8217;equazione &#8220;<< a1<< &#8220;x+&#8221;<<b1 <<&#8220;=0 e&#8217; pari a x=&#8221;<< (-b1)<< &#8220;/&#8221; << a1<< endl;  
else  
cout << &#8220;La soluzione dell&#8217;equazione &#8220;<< a1<< &#8220;x&#8221;<<b1 <<&#8220;=0 e&#8217; pari a x=&#8221;<< (-b1)<< &#8220;/&#8221; << a1<< endl;  
break;  
}  
case (2):  
cout << &#8220;\___\___\___\___\___\___\___\___\___\___\___\___\___\___\___\___&#8221;<< endl;  
cout <<&#8220;| EQUAZIONE DI 2* GRADO |&#8221;<< endl;  
cout <<&#8220;|\___\___\___\___\___\___\___\___\___\___\___\___\___\___\___\___|&#8221;<< endl;  
cout <<&#8220;| |&#8221;<< endl;  
cout <<&#8220;| |&#8221;<< endl;  
cout <<&#8220;| ax^2+bx+c=0 |&#8221;<< endl;  
cout <<&#8220;| |&#8221;<< endl;  
cout <<&#8220;| |&#8221;<< endl;  
cout <<&#8220;|\___\___\___\___\___\___\___\___\___\___\___\___\___\___\___\___|&#8221;<< endl;  
cout << &#8220;La tua equazione disponde di tutti i parametri (a,b,c), o solamente di due?&#8221;<< endl;  
cout << &#8220;1. Dispone di tutti i parametri.&#8221;<< endl;  
cout << &#8220;2. Dispone del parametro a e b&#8221;<< endl;  
cout << &#8220;3. Dispone del parametro a e c&#8221;<< endl;  
/* switch(j){ QUI MI SON FERMATO PER CHIEDERVI AIUTO  
case (1):

}  
*/

return 0;  
}

//Funzione eq 1° grado  
// Dichiarazione della funzione  
int eq1(int x, int y)  
{  
int ris1=0;  
ris1 = (-(y/x));[/cce_cpp]