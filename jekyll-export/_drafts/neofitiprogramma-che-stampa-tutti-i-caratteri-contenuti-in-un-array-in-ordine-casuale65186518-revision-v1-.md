---
id: 6519
date: 2016-08-06T09:39:20+02:00
author: mydreamsarelies
layout: revision
guid: http://www.italiancpp.org/2016/08/06/6518-revision-v1/
permalink: /2016/08/06/6518-revision-v1/
---
Scusami se ti chiedo ancora informazioni e aiuti, ma il codice non viene compilato a causa di questo errore:  
[cce_cpp]  
12 9 C:\Users\renzo\Desktop\file del desktop\Informatica\C++\ScambiaArray.cpp [Error] reference to &#8216;max&#8217; is ambiguous  
6 5 C:\Users\renzo\Desktop\file del desktop\Informatica\C++\ScambiaArray.cpp [Note] candidates are: int max  
[/cce_cpp]  
Il codice che mi hai scritto nell&#8217;ultimo messaggio l&#8217;ho messo sotto forma di funzione:  
[cce_cpp]  
#include <iostream>  
#include <cstdlib>  
#include <ctime>  
using namespace std;

const int max=8;  
void InserimentoCaratteri(char[]);  
void ScambiaArray(char []);  
void Stampa(int, char []);

int main(){  
char s[max];  
InserimentoCaratteri(s);  
ScambiaArray(s);

fflush(stdin);  
getchar();  
return 0;  
}  
void InserimentoCaratteri(char s[]){  
for(int i=0; i<max-1; i++){  
cout<<&#8220;Inserisci il &#8220;<<i<<&#8220;^ carattere: &#8220;;  
cin>>s[i];  
}  
s[max-1]=&#8217;\0&#8242;;  
}  
void ScambiaArray(char s[]){  
srand(time(NULL));  
int n=0, x;  
for(; s[n]!=&#8217;\0&#8242;; n++){  
for(int k=0; k<n; k++){  
do{  
x=rand()%n;  
}while(s[x]==&#8217;\0&#8242;);  
cout<<s[x];  
s[x]==&#8217;\0&#8242;;  
}  
}  
for(int i=0; i<n; i++)  
cout<<s[i];  
}  
[/cce_cpp]