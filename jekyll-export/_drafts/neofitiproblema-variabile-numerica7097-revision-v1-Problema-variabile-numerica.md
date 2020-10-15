---
id: 7098
title: Problema variabile numerica
date: 2016-11-24T15:58:36+01:00
author: Alessandro
layout: revision
guid: http://www.italiancpp.org/2016/11/24/7097-revision-v1/
permalink: /2016/11/24/7097-revision-v1/
---
Ciao a tutti, sto facendo un piccolo programma in cui si danno due numeri e si scrive l&#8217;operazione da eseguire per poi essere eseguita. Ho creato delle variabili : num1, num2 e num3. in num3 ho scritto che deve essere la somma di num1 e num2, pensando che usasse i dati che gli scrivono, ma invece mi mette un numero a caso. Spero che qualcuno mi possa aiutare.

> #include <iostream>  
> #include <string>  
> using namespace std;
> 
> int main()
> 
> {  
> int num1;  
> int num2;  
> int num3 = num1 + num2;  
> char operazione[0];
> 
> cout << &#8220;Inserisci primo numero: &#8220;;  
> cin >> num1;
> 
> cout << &#8220;Inserisci secondo numero: &#8220;;  
> cin >> num2;
> 
> cout << &#8220;Inserisci operazione: &#8220;;  
> cin >> operazione;
> 
> if (strcmp(&#8220;addizione&#8221;, operazione) == 0)  
> {  
> cout<< num3;  
> }
> 
> }
> 
> >