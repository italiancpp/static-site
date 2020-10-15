---
id: 6800
date: 2016-09-22T16:56:38+02:00
author: Stefano
layout: revision
guid: http://www.italiancpp.org/2016/09/22/6799-revision-v1/
permalink: /2016/09/22/6799-revision-v1/
---
Ho esultato troppo presto vedendo il post, ma in realtà non funziona.

Humm invece no, sono stato porecipitoso pensavo di aver capito come funzionava la cosa, ma mi da errori di compilazione.

ho incluso

[cce_cpp]#include <iostream>  
#include <string>[/cce_cpp]

e messo lo using solito per lo standard

[cce\_cpp]using namespace std;[/cce\_cpp]

ora se ho capito bene come funziona la cosa le funzioni citate del tipo to_string dovrebbero stare in &#8220;string&#8221;

quindi se ho una funzione che setta un nome del tipo

[cce\_cpp]void SetName(const string &valore); //setta un dato membro al valore tipo nome = valore[/cce\_cpp]

e ho un numero intero del tipo

[cce\_cpp]int numTest = 1; //numero a random per spiegazione[/cce\_cpp]

se faccio un chiamata alla funzione precedente del tipo

[cce\_cpp]SetName(&#8220;Cliente#&#8221; + to\_string(numTest));[/cce_cpp]

dovrebbe settare il nome a una cosa del tipo&#8230;

Cliente#1

giusto?

quello che ottengo al momento è un errore in cui &#8220;to_string&#8221; non è definita nonostante le #include a string.

Sto usando CodeBlocks 13.12 con attivati i controlli per lo standard C++11 in compilazione

Cosa mi sfugge?