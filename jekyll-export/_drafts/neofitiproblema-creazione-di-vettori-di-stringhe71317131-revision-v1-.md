---
id: 7132
date: 2016-11-26T20:49:49+01:00
author: Matteo
layout: revision
guid: http://www.italiancpp.org/2016/11/26/7131-revision-v1/
permalink: /2016/11/26/7131-revision-v1/
---
Ciao Lorenzo,  
anche io sono ai primi passi col C++ e bazzico spesso con i vettori.  
Ciò che distingue pricipalmente i vettori dagli array, è la possibilià di aumentare o diminuire le dimensioni del vettore. Quindi è su questo che devi lavorare. Per creare string a partire da int, puoi usare la funzione introdotta dal C++11, std::to_string().

Esempio:  
[cce_cpp]  
#include <iostream>  
#include <string>

int main()  
{  
std::cout << &#8220;Insert a number: &#8220;;  
int a;  
std::cin >> a;

std::string str = std::to_string(a);  
cout << &#8220;This is a string &#8221; << str << std::endl;

return 0;  
}  
[/cce_cpp]