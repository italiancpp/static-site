---
id: 6909
title: Gotoxy creare spazio delimitato
date: 2016-10-21T15:58:17+02:00
author: Michelangelo
layout: revision
guid: http://www.italiancpp.org/2016/10/21/6907-revision-v1/
permalink: /2016/10/21/6907-revision-v1/
---
Ciao ragazzi. Non ho ampie conoscenza di C++. Sto elaborando un programma che è una sorta di lavagna, con la funzione gotoxy che ho rinominato &#8216;posizione&#8217;, e che ha i parametri x e y (coordinate). In questo programma ci sono tre modalità: scrittura, cancellatura, e movimento. Lo spostamento del puntatore avviene attraverso un ciclo do-while infinito e lasciando una scia si &#8216;+&#8217; dietro al puntatore; la cancellatura avviene più o meno nello stesso modo lasciando quindi una scia si spazi vuoti; avrei bisogno quindi di due aiuti molto importanti. Non so minimamente come creare la modalità movimento: voglio che ci sia un simbolo che si muova all&#8217;interno dell&#8217;interfaccia ma che non cancelli niente e che non scriva. Il secondo aiuto che vorrei da voi è come delimitare lo spazio dello spostamento&#8230; Spero che mi sappiate aiutare.

[cce_cpp]  
#include<iostream.h>  
#include<conio.h>//usare getch()  
//#include<cstdlib>  
#include<windows.h>//usare gotoxy  
using namespace std;

void posizione(short x, short y)  
{  
COORD pos={x,y};  
SetConsoleCursorPosition(GetStdHandle(STD\_OUTPUT\_HANDLE), pos);  
}

void output_lavagna()  
{  
int k;

posizione(0,9); cout<<&#8221; #&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;#&#8221;;//bordo superiore  
posizione(0,50); cout<<&#8221; #&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;#&#8221;;//bordo inferiore  
posizione(0,1); cout<<&#8220;\t LAVAGNA&#8221;;  
posizione(0,7); cout<<&#8220;\t 0=esci &#8211; 1=Scrivi &#8211; 2=Cancella &#8211; 3=Muovi&#8221;;

for(k=10;k<50;k++)//bordo sinistro  
{  
posizione(9,k); cout<<&#8220;|&#8221;;  
}  
for(k=10;k<50;k++)//bordo destro  
{  
posizione(70,k); cout<<&#8220;|&#8221;;  
}  
}

int main()  
{  
int tasto;  
int x=40, y=28;//coordinate  
int modalita=1;//0=esci &#8211; 1=penna &#8211; 2=gomma &#8211; 3=muovi  
char strumento=&#8217;+&#8217;;//oggetto che si muove  
bool esci=false;

system(&#8220;color 0f&#8221;);//colore sfondo/testo

output_lavagna();

//INIZIO CICLO FINCHE NON VIENE PREMUTO 0  
do{  
posizione(0,3); cout<<&#8220;\t Coordinate: (&#8220;<<x<<&#8220;,&#8221;<<y<<&#8220;)&#8221;;  
posizione(0,5); cout<<&#8220;\t Modalita&#8217; attuale: &#8220;;  
if(modalita==1)cout<<&#8220;Scrivi&#8221;;  
if(modalita==2)cout<<&#8220;Cancella&#8221;;  
if(modalita==3)cout<<&#8220;Muovi&#8221;;  
posizione(x,y); cout<<strumento;//per disegnare

//INPUT TASTO  
tasto=getch();

switch (tasto)  
{  
case 48:  
esci=true;  
break;  
case 49:  
modalita=1;  
break;  
case 50:  
modalita=2;  
break;  
case 51:  
modalita=3;  
break;  
}

if(x>9 && x<70)  
{  
if(y>9 && y<50)  
{  
//MODALITA SCRITTURA  
if(modalita==1)  
{  
strumento=&#8217;+&#8217;;

if(tasto==72)y&#8211;;//su  
if(tasto==80)y++;//giu  
if(tasto==77)x++;//destra  
if(tasto==75)x&#8211;;//sinistra  
posizione(x,y); cout<<strumento;//per disegnare  
}

//MODALITA CANCELLATURA  
if(modalita==2)  
{  
strumento=&#8217;O&#8217;;  
switch (tasto)  
{  
case 72:  
y&#8211;;  
posizione(x,y+1); cout<<&#8221; &#8220;;  
break;  
case 80:  
y++;  
posizione(x,y-1); cout<<&#8221; &#8220;;  
break;  
case 77:  
x++;  
posizione(x-1,y); cout<<&#8221; &#8220;;  
break;  
case 75:  
x&#8211;;  
posizione(x+1,y); cout<<&#8221; &#8220;;  
break;  
}  
posizione(x,y); cout<<strumento;//per disegnare  
}

//MODALITA MOVIMENTO  
/*if(modalita==3)  
{  
strumento=&#8217;+&#8217;;  
}*/  
}  
}

}while(!esci);//FINE CICLO FINCHE NON VIENE PREMUTO 0  
}  
[/cce_cpp]