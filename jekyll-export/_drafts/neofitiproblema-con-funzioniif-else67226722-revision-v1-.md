---
id: 6723
date: 2016-09-09T15:49:25+02:00
author: Stefano Famà
layout: revision
guid: http://www.italiancpp.org/2016/09/09/6722-revision-v1/
permalink: /2016/09/09/6722-revision-v1/
---
Scrivi pure quanto vuoi, mi piace aiutare, poi non credere ch&#8217;io sappia chissà cosa, tutti hanno questi problemi all&#8217;inizio.

Se posti del codice hai 2 modi:  
1 &#8211; premi il pulsante **code**, incolli il codice, ripremi il tasto **/code**  
2 &#8211; incolli il codice, selezioni tutto, premi il pulsante **code**

Perché così tu hai dimenticato di chiudere un tag, e infatti è tutto come testo normale.

Detto ciò, il programma diventa un po&#8217; grosso per un unico file.  
Ti consiglio di suddividere il tutto in **header** e **source**.

La **dichiarazione** la scrivi nel file **header**.  
La **definizione** la scrivi nel file **source**.

Così diventa più semplice da mantenere.

Per il discorso dell&#8217;input, ecco tu hai questo problema qua:  
La tua variabile è un **char**.  
Un **char** contiene **1** carattere soltanto.  
Infatti se tu inserisci solo **1** carattere per volta, tutto funziona bene.  
Ma se inserisci qualcosa come _10_ _20_ _30_? Perché funziona male?

Ecco qui succede questo:  
**char** _scelta_ = &#8216;****&#8216;;  
**cin** >> _scelta_; // Supponiamo che l&#8217;utente inserisce **12**  
**cout** << _scelta_; // Stampa **1**

Ma il numero 2 dov&#8217;è finito?? Eh, non è scomparso&#8230;

Se infatti scrivessi del codice tipo questo, inserendo sempre **12**:  
**char** _scelta_ = &#8216;****&#8216;;

**cin** >> _scelta_;  
**cout** << _scelta_;

**cin** >> _scelta_;  
**cout** << _scelta_;

Nel primo **cin** il computer dice, guarda che mi serve **1** carattere, tu ne inserisci quanti ne vuoi, lui però cosa fa, prende il **primo** carattere, perché ne vuole **1** solo, ma gli altri **non li butta** perché tu gli hai inseriti, non può sapere se sono importanti o meno, allora li mette da parte.

La **seconda** volta che tu gli vai a chiedere ancora dell&#8217;input con **cin**, il computer vede che aveva messo da parte qualcosa! Allora prende quello che gli serve da lì! Ecco perché ti fa questi problemi.

Una possibile soluzione sarebbe l&#8217;uso di <a href="http://en.cppreference.com/w/cpp/string/basic_string" target="_blank"><string></a> come scelta.  
Così tutti i caratteri che andrai ad inserire saranno usati e non metterà da parte nulla.

Il codice l&#8217;ho modificato un attimo, non più di tanto a dire il vero.

Main.cpp  
[cce_cpp]#include <iostream>  
#include <cstdlib>  
#include <conio.h>

#include &#8220;Menu.hpp&#8221;  
#include &#8220;Intestazione.hpp&#8221;

#include <string>

using namespace std;

int main()  
{  
string scelta{ &#8220;0&#8221; };  
do  
{  
//system(&#8220;cls&#8221;);

printMainMenu();

cin >> scelta;  
switch (scelta.at(0))  
{  
case&#8217;1&#8242;:  
system(&#8220;cls&#8221;);  
eseguifunzione1(); // Richiamo funzione per equazione primo grado.  
break;  
case &#8216;2&#8217;:  
system(&#8220;cls&#8221;);  
eseguifunzione2(); // Richiamo funzione per equazione terzo grado.  
break;  
case &#8216;3&#8217;:  
//Esce  
break;  
default:  
cout << &#8220;Inserisci dei parametri corretti.&#8221; << endl;  
break;  
}  
} while (scelta.at(0) != &#8216;3&#8217;);  
system(&#8220;pause&#8221;);  
return 0;  
}[/cce_cpp]  
Menu.hpp  
[cce_cpp]#pragma once

void printMainMenu();

void printEq1Menu();

void printEq2Menu();

void printEqPura();

void printEqSpuria();[/cce_cpp]  
Menu.cpp  
[cce_cpp]#include &#8220;Menu.hpp&#8221;

#include <iostream>

void printMainMenu() {  
std::cout << &#8221; \___\___\___\___\___\___\___\___\___\___\___\___\___\___\___\___&#8221; << std::endl;  
std::cout << &#8221; | EQUAZIONI DI 1 E 2 GRADO | &#8221; << std::endl; //INSERISCI COMANDO PER PULIRE SCHERMO  
std::cout << &#8221; | \___\___\___\___\___\___\___\___\___\___\___\___\___\___\___\___ | &#8221; << std::endl;  
std::cout << &#8221; | | &#8221; << std::endl; //GUARDA PREFERITI PER EVITARE CHE UTENTE INSERISCA LETTERE O STRONZATE  
std::cout << &#8221; | 1. Equazione di 1 * grado. | &#8221; << std::endl; // FARE IF PER FARE IMMETTERE SOLO VALORI COMPRESI TRA 1 E 3 NELLE VARIE TENDINE  
std::cout << &#8221; | 2. Equazione di 2 * grado. | &#8221; << std::endl; // Delta maggiore di 0 nelle eq di secondo grado obbligatoriamente!  
std::cout << &#8221; | 3. Esci | &#8221; << std::endl;  
std::cout << &#8221; | | &#8221; << std::endl;  
std::cout << &#8221; | \___\___\___\___\___\___\___\___\___\___\___\___\___\___\___\___ | &#8221; << std::endl;  
}

void printEq1Menu() {  
std::cout << &#8220;\___\___\___\___\___\___\___\___\___\___\___\___\___\___\___\___&#8221; << std::endl;  
std::cout << &#8221; | EQUAZIONE DI 1 * GRADO | &#8221; << std::endl;  
std::cout << &#8221; | \___\___\___\___\___\___\___\___\___\___\___\___\___\___\___\___ | &#8221; << std::endl;  
std::cout << &#8221; | | &#8221; << std::endl;  
std::cout << &#8221; | | &#8221; << std::endl;  
std::cout << &#8221; | ax + b = 0 | &#8221; << std::endl;  
std::cout << &#8221; | | &#8221; << std::endl;  
std::cout << &#8221; | | &#8221; << std::endl;  
std::cout << &#8221; | \___\___\___\___\___\___\___\___\___\___\___\___\___\___\___\___ | &#8221; << std::endl;  
std::cout << &#8220;Inserire i parametri a e b interposti da uno spazio : &#8221; << std::endl;;  
}

void printEq2Menu() {  
std::cout << &#8220;\___\___\___\___\___\___\___\___\___\___\___\___\___\___\___\___&#8221; << std::endl;  
std::cout << &#8221; | EQUAZIONE DI 2 * GRADO | &#8221; << std::endl;  
std::cout << &#8221; | \___\___\___\___\___\___\___\___\___\___\___\___\___\___\___\___ | &#8221; << std::endl;  
std::cout << &#8221; | | &#8221; << std::endl;  
std::cout << &#8221; | | &#8221; << std::endl;  
std::cout << &#8221; | ax ^ 2 + bx + c = 0 | &#8221; << std::endl;  
std::cout << &#8221; | | &#8221; << std::endl;  
std::cout << &#8221; | | &#8221; << std::endl;  
std::cout << &#8221; | \___\___\___\___\___\___\___\___\___\___\___\___\___\___\___\___ | &#8221; << std::endl;  
std::cout << &#8220;La tua equazione disponde di tutti i parametri(a, b, c), o solamente di due ? &#8221; << std::endl;  
std::cout << &#8220;1.Dispone di tutti i parametri.&#8221; << std::endl;  
std::cout << &#8220;2.Dispone del parametro a e b&#8221; << std::endl;  
std::cout << &#8220;3.Dispone del parametro a e c(IN MANUTENZIONE)&#8221; << std::endl;  
}

void printEqPura() {  
std::cout << &#8220;\___\___\___\___\___\___\___\___\___\___\___\___\___\___\___\___&#8221; << std::endl;  
std::cout << &#8221; | EQUAZIONE PURA DI 2 * GRADO | &#8221; << std::endl;  
std::cout << &#8221; | \___\___\___\___\___\___\___\___\___\___\___\___\___\___\___\___ | &#8221; << std::endl;  
std::cout << &#8221; | | &#8221; << std::endl;  
std::cout << &#8221; | | &#8221; << std::endl;  
std::cout << &#8221; | ax ^ 2 + c = 0 | &#8221; << std::endl;  
std::cout << &#8221; | | &#8221; << std::endl;  
std::cout << &#8221; | | &#8221; << std::endl;  
std::cout << &#8221; | \___\___\___\___\___\___\___\___\___\___\___\___\___\___\___\___ | &#8221; << std::endl;  
std::cout << &#8220;Inserire i parametri a e c interposti da uno spazio : &#8221; << std::endl;  
}

void printEqSpuria() {  
std::cout << &#8220;\___\___\___\___\___\___\___\___\___\___\___\___\___\___\___\___&#8221; << std::endl;  
std::cout << &#8221; | EQUAZIONE SPURIA DI 2 * GRADO | &#8221; << std::endl;  
std::cout << &#8221; | \___\___\___\___\___\___\___\___\___\___\___\___\___\___\___\___ | &#8221; << std::endl;  
std::cout << &#8221; | | &#8221; << std::endl;  
std::cout << &#8221; | | &#8221; << std::endl;  
std::cout << &#8221; | ax ^ 2 + bx = 0 | &#8221; << std::endl;  
std::cout << &#8221; | | &#8221; << std::endl;  
std::cout << &#8221; | | &#8221; << std::endl;  
std::cout << &#8221; | \___\___\___\___\___\___\___\___\___\___\___\___\___\___\___\___ | &#8221; << std::endl;  
std::cout << &#8220;Inserire i parametri a e b interposti da uno spazio : &#8221; << std::endl;  
}[/cce_cpp]  
Funzioni.hpp  
[cce_cpp]#pragma once

int eq1(int x, int y);

int matrice(int a2, int b2, int c2);

void eseguifunzione1();

void eseguifunzione2();

void Eqspuria();

void Eqpura();[/cce_cpp]  
Funzioni.cpp

[cce_cpp]#include &#8220;Intestazione.hpp&#8221;

#include &#8220;Menu.hpp&#8221;

#include <iostream>

using namespace std;

void eseguifunzione1()  
{  
int a1 = 0;  
int b1 = 0;  
int riseq1 = 0;

printEq1Menu();

cin >> a1;  
cin >> b1;  
riseq1 = eq1(a1, b1); // Richiamo la funzione int eq1  
if (b1%a1 == 0) {  
if (b1>0) {  
system(&#8220;cls&#8221;);  
cout << &#8220;La soluzione dell&#8217;equazione &#8221; << a1 << &#8220;x + &#8221; << b1 << &#8221; = 0 e&#8217; pari a x = &#8221; << (-(b1 / a1)) << endl;;  
}  
else {  
system(&#8220;cls&#8221;);  
cout << &#8220;La soluzione dell&#8217;equazione &#8221; << a1 << &#8220;x&#8221; << b1 << &#8221; = 0 e&#8217; pari a x = &#8221; << (-(b1 / a1)) << endl;;  
}  
}  
else  
{  
if (b1>0)  
{  
system(&#8220;cls&#8221;);  
cout << &#8220;La soluzione dell&#8217;equazione &#8221; << a1 << &#8220;x + &#8221; << b1 << &#8221; = 0 e&#8217; pari a x = &#8221; << (-b1) << &#8221; / &#8221; << a1 << endl;  
}  
else  
system(&#8220;cls&#8221;);  
cout << &#8220;La soluzione dell&#8217;equazione &#8221; << a1 << &#8220;x&#8221; << b1 << &#8221; = 0 e&#8217; pari a x = &#8221; << (-b1) << &#8221; / &#8221; << a1 << endl;  
}  
}

//Funzione eq 1° grado  
// Dichiarazione della funzione  
int eq1(int x, int y)  
{  
int ris1 = 0;  
ris1 = (-(y / x));  
return ris1;  
}

void eseguifunzione2()  
{  
int j, a2, b2, c2, delta, x = 0;

printEq2Menu();

cin >> j;  
switch (j) {  
case (1):  
{  
cout << &#8220;Inserire i parametri a, b, c interposti da uno spazio : &#8221; << endl;  
cin >> a2;  
cin >> b2;  
cin >> c2;  
system(&#8220;cls&#8221;);  
delta = matrice(a2, b2, c2); //Richiamo funzione matrice  
break;  
}  
case (2):  
system(&#8220;cls&#8221;);  
Eqspuria();  
break;  
case (3):  
system(&#8220;cls&#8221;);  
Eqpura();  
break;  
default:  
cout << &#8220;Inserisci dei parametri corretti.&#8221;;  
break;  
}  
}  
//Funzione matrice— Dichiarazione  
int matrice(int a2, int b2, int c2)  
{  
int prod = a2*c2;  
int argomento1 = (b2\*b2) &#8211; (4 \* prod);  
int radice = sqrt((b2\*b2) &#8211; (4 \* prod));  
int argomento2 = sqrt((b2\*b2) &#8211; (4 \* prod));  
int risultato1 = (-(b2)+(radice)) / (2 * a2);  
int risultato2 = (-(b2)-radice) / (2 * a2);  
cout << &#8220;La soluzione dell&#8217;equazione di secondo grado &#8221; << a2 << &#8220;x ^ 2 + (&#8221; << b2 << &#8220;)x + (&#8221; << c2 << &#8220;) = 0 e&#8217;:&#8221; << endl;  
if (radice*radice == argomento1) // SE IL QUADRATO è PERFETTO  
{  
if (((-b2) + (radice)) % (2 * a2) == 0)//SE LA DIVISIONE è &#8220;PERFETTA&#8221;  
{  
cout << &#8220;x1 = &#8221; << risultato1 << endl;  
}  
else {  
cout << &#8220;x1 = &#8221; << (-(b2)+radice) << &#8221; / &#8221; << (2 * a2) << endl;  
}  
}  
else  
{  
cout << &#8220;x1 = [&#8221; << -b2 << &#8221; + (&#8221; << argomento1 << &#8220;) ^ 1 / 2] / &#8221; << (2 * a2) << endl;  
}  
if (radice*radice == argomento2) // SE IL QUADRATO è PERFETTO  
{  
if (((-b2) &#8211; (radice)) % (2 * a2) == 0)//SE LA DIVISIONE è &#8220;PERFETTA&#8221;  
{  
cout << &#8220;x2 = &#8221; << risultato2 << endl;  
}  
else {  
cout << &#8220;x2 = &#8221; << (-(b2)-radice) << &#8221; / &#8221; << (2 * a2) << endl;  
}  
}  
else  
{  
cout << &#8220;x2 = [&#8221; << -b2 << &#8221; + (&#8221; << b2\*b2 + (4 \* prod) << &#8220;) ^ 1 / 2] / &#8221; << (2 * a2) << endl;  
}

return 0;  
}  
void Eqspuria()  
{  
int a3, b3 = 0;

printEqSpuria();

cin >> a3;  
cin >> b3;  
system(&#8220;cls&#8221;);  
cout << &#8220;Le soluzioni dell&#8217;equazione &#8221; << a3 << &#8220;x ^ 2 + (&#8221; << b3 << &#8220;)x = 0 sono:&#8221; << endl;  
cout << &#8220;x = 0&#8221; << endl;  
if ((b3%a3) == 0)  
cout << &#8220;x2 = &#8221; << -(b3 / a3) << endl;  
else  
cout << &#8220;x2 = &#8221; << (-b3) << &#8221; / &#8221; << a3 << endl;  
}  
void Eqpura()  
{  
int a4, c4 = 0;

printEqPura();

cin >> a4;  
cin >> c4;  
// Nuova finestra: 1)Il termine a è > o < di 0?  
int radicee = sqrt(c4 / -a4);  
int argomentoo1 = (c4 / -a4); // risultato1 quando c4<0 a4>0  
int radicee2 = sqrt(-c4 / a4);  
int argomentoo2 = (-c4 / a4);  
int risultatoo2 = (radicee);  
if (a4<0 && c4>0)  
{  
if (radicee*radicee == argomentoo1) // SE IL QUADRATO è PERFETTO  
if (c4%-a4 == 0)//SE LA DIVISIONE è &#8220;PERFETTA&#8221;  
{  
system(&#8220;cls&#8221;);  
cout << &#8220;Le soluzioni dell&#8217;equazione&#8221; << a4 << &#8220;x ^ 2 + &#8221; << c4 << &#8221; = 0 sono:&#8221; << endl;  
cout << &#8220;x1 = &#8221; << radicee << endl;  
cout << &#8220;x2 = &#8221; << -radicee << endl;  
}  
else  
{  
system(&#8220;cls&#8221;);  
cout << &#8220;Le soluzioni dell&#8217;equazione&#8221; << a4 << &#8220;x ^ 2 + &#8221; << c4 << &#8221; = 0 sono:&#8221; << endl;  
cout << &#8220;x1 = (&#8221; << c4 << &#8221; / &#8221; << -a4 << &#8220;) ^ 1 / 2]&#8221; << endl;  
cout << &#8220;x2 = (&#8221; << c4 << &#8221; / &#8221; << -a4 << &#8220;) ^ 1 / 2]&#8221; << endl;  
}  
}  
else  
if (c4<0 && a4>0)  
{  
if (radicee2*radicee2 == argomentoo2) // SE IL QUADRATO è PERFETTO  
if (-c4%a4 == 0)//SE LA DIVISIONE è &#8220;PERFETTA&#8221;  
{  
system(&#8220;cls&#8221;);  
cout << &#8220;Le soluzioni dell&#8217;equazione&#8221; << a4 << &#8220;x ^ 2&#8243; << c4 << &#8221; = 0 sono:&#8221; << endl;  
cout << &#8220;x1 = &#8221; << risultatoo2 << endl;  
cout << &#8220;x2 = &#8221; << -risultatoo2 << endl;  
}  
else  
{  
system(&#8220;cls&#8221;);  
cout << &#8220;Le soluzioni dell&#8217;equazione&#8221; << a4 << &#8220;x ^ 2&#8243; << c4 << &#8221; = 0 sono:&#8221; << endl;  
cout << &#8220;x1 = (&#8221; << -c4 << &#8221; / &#8221; << a4 << &#8220;) ^ 1 / 2]&#8221; << endl;  
cout << &#8220;x2 = (&#8221; << -c4 << &#8221; / &#8221; << a4 << &#8220;) ^ 1 / 2]&#8221; << endl;  
}  
}  
else {  
system(&#8220;cls&#8221;);  
cout << &#8220;Le soluzioni dell&#8217;equazione&#8221; << a4 << &#8220;x ^ 2&#8243; << c4 << &#8221; = 0 sono:&#8221; << endl;  
cout << &#8220;L&#8217;equazione non ha valori di x appartenenti ai numeri reali.&#8221; << endl;  
}  
}[/cce_cpp]

Ti ricordo che nel C++ non è necessario dichiarare le funzioni prima del loro uso, come nel C.