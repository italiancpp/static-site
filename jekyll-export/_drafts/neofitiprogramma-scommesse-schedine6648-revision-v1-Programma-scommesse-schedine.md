---
id: 6650
title: Programma scommesse schedine
date: 2016-08-29T11:56:48+02:00
author: Federico
layout: revision
guid: http://www.italiancpp.org/2016/08/29/6648-revision-v1/
permalink: /2016/08/29/6648-revision-v1/
---
Salve, ho creato questo programma di scommesse(calcistiche) basandomi sul fatto che giocando tot soldi si ha un margine di vittoria in tutti i casi, eccezzion fatta se si verificano risultati di 0-0 o 1+ over 4.5. Questo sistema si basa sul combinare le quote multi gol 1-4 e x2+ over 3.5 di due partite, formando 4 schedine combinate. L&#8217;unico problema è che inserendo tutti gli input, la somma degli importi da giocare per schedina viene calcolata dal calcolatore sempre minore al reale importo. (Es: Gioco 50 euro, il calcolatore utilizza circa 47-48 euro). Vi inserisco il codice per eventuali aiuti, grazie in anticipo.

#include <iostream>  
using namespace std;  
int main(){  
double a;  
double b;  
double c;  
double d;  
double budjet;  
cout<<&#8220;inserire budget &#8220;;  
cin>>budjet;  
cout<<&#8220;quota multigol 1-4 squadra 1: &#8220;;  
cin>>a;  
cout<<&#8220;quota multigol 1-4 squadra 2: &#8220;;  
cin>>b;  
cout<<&#8220;quota x2+ov3.5 squadra 1: &#8220;;  
cin>>c;  
cout<<&#8220;quota x2+ov3.5 squadra 2: &#8220;;  
cin>>d;  
double sc1=1/(a*b);  
double sc2=1/(a*d);  
double sc3=1/(c*b);  
double sc4=1/(c*d);  
double x=sc1+sc2+sc3+sc4;  
if(x<0.99){  
cout<<&#8220;emissione giocate:&#8221;<<endl;  
cout<<&#8220;schedina 1:multi squadra 1 +multi squadra 2: &#8220;<<&#8220;quota: &#8220;<<a\*b<<&#8220;importo: &#8220;<< sc1\*budjet <<&#8220;euro&#8221;<< endl;  
cout<<&#8220;schedina 2:multi squadra 1 + x2 ov 3.5 squadra 2:&#8221;<<&#8220;quota: &#8220;<<a\*d<<&#8220;importo: &#8220;<<sc2\*budjet<<&#8220;euro&#8221;<<endl;  
cout<<&#8220;schedina 3:x2 ov 3.5 squadra 1 + multigol squadra 2: &#8220;<<&#8220;quota: &#8220;<<c\*b<<&#8220;importo: &#8220;<<sc3\*budjet<<&#8220;euro&#8221;<<endl;  
cout<<&#8220;schedina 4:x2 ov 3.5 squadra 1 + x2 ov 3.5 quadra 2: &#8220;<<&#8220;quota: &#8220;<<c\*d<<&#8220;importo: &#8220;<<sc4\*budjet<<&#8220;euro&#8221;<<endl;  
}  
else{  
cout<<&#8220;non conviene giocare\n&#8221;;  
}

return 0;  
}