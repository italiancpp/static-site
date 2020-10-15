---
id: 7457
title: Programma per testare numeri primi va in loop per numeri molto elevati
date: 2017-01-30T21:23:54+01:00
author: marco
layout: revision
guid: http://www.italiancpp.org/2017/01/30/7456-revision-v1/
permalink: /2017/01/30/7456-revision-v1/
---
Buonasera a tutti, posto un programma che mi perseguita ormai da giorni. Il programma prende in input un numero naturale e stabilisce se questo è primo oppure no. Non ho problemi per numeri piccoli, ma per numeri con 10-11 cifre o più il programma entra in loop senza più uscirne e non riesco proprio a capire perché.

Ecco il codice:

[cce_cpp]  
#include <iostream>  
#include <math.h>  
using namespace std;

void isPrime(long int n) {  
if (n < 0) {  
long int m;  
cout << &#8220;Devi inserire un numero positivo!&#8221; << endl << &#8220;Inserisci un altro numero:&#8221; << endl << endl;  
cin >> m;  
cout << endl << endl;  
isPrime(m);  
}  
switch (n) {  
case 0:  
cout << &#8220;0 non e un numero primo&#8221; << endl << endl;  
break;  
case 1:  
cout << &#8220;1 non e un numero primo&#8221; << endl << endl;  
break;  
case 2:  
cout << &#8220;2 e un numero primo&#8221; << endl << endl;  
break;  
default:  
bool prime = true;  
for (long int i = 2; i < sqrt(n) + 1; i++) {  
if (n % i == 0) {  
cout << n << &#8221; non e un numero primo&#8221; << endl << endl;  
prime = false;  
break;  
}  
}  
if (prime == true) {  
cout << n << &#8221; e un numero primo&#8221; << endl << endl;  
}  
}  
}

int repeatProgram() {  
char answer;  
cout << &#8220;Vuoi continuare? s/n&#8221; << endl << endl;  
cin >> answer;  
cout << endl << endl;  
switch (answer) {  
case &#8216;s&#8217;:  
long int p;  
cout << &#8220;Inserisci un altro numero naturale:&#8221; << endl << endl;  
cin >> p;  
cout << endl << endl;  
isPrime(p);  
repeatProgram();  
break;  
case &#8216;n&#8217;:  
return 0;  
break;  
default:  
cout << &#8220;La tua scelta non e valida! Riprova:&#8221; << endl << endl;  
repeatProgram();  
}  
}

int main(){  
long int num;  
cout << &#8220;Inserisci un numero naturale:&#8221; << endl << endl;  
cin >> num;  
cout << endl << endl;  
if (num > 1000000000) {  
long int t;  
cout << &#8220;Attualmente il programma non puo gestire numeri così grandi:&#8221; << endl << &#8220;Inserisci un altro numero:&#8221; << endl << endl;  
cin >> t;  
cout << endl << endl;  
isPrime(t);  
repeatProgram();  
}  
else {  
isPrime(num);  
repeatProgram();  
}  
}  
[/cce_cpp]

ho provato di tutto, ma non è servito a niente.