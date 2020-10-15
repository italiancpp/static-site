---
id: 7142
date: 2016-11-28T17:47:51+01:00
author: Stefano Famà
layout: revision
guid: http://www.italiancpp.org/2016/11/28/7141-revision-v1/
permalink: /2016/11/28/7141-revision-v1/
---
Ciao Luigi &#x1f642;  
Allora il problema è nel codice del ciclo.  
Prima incrementi la variabile e dopo esegui l&#8217;addizione, basta invertire le due operazioni 🙂  
[cce_cpp]#include <iostream>

int main()  
{  
int start = 3;  
int end = 8;  
int sum = 0;

while(start <= end){  
sum += start;  
++start;  
}

std::cout << sum;  
}[/cce_cpp]

Uso un ciclo while perché tanto non mi serve nessun&#8217;altra variabile!  
Posso tranquillamente usare l&#8217;estremo inferiore come contatore &#x1f642;  
Per la parte di prendere 2 numeri in input credo tu non abbia problemi, comunque basta usare std::cin >> nome_variabile.