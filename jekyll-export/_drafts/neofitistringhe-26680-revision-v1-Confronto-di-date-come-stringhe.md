---
id: 6683
title: Confronto di date come stringhe
date: 2016-09-02T11:24:01+02:00
author: marco
layout: revision
guid: http://www.italiancpp.org/2016/09/02/6680-revision-v1/
permalink: /2016/09/02/6680-revision-v1/
---
Buongiorno,  
avrei bisogno di un aiuto.  
Per risolvere un esercizio in c++ ho creato una lista dinamica (i cui nodi sono formati in questo modo &#8211;> struct nodo { biglietto info; nodo*next;}; dove biglietto è un nuovo tipo di capo creato con apposita struttura contenente anche il capo char DataEvento [11]; preciso che la traccia richiede specificamente che sia una stringa nel formato gg-mm-aaaa) e successivamente devo creare una funzione che, data la lista e due date mi dia il biglietto venduto al max prezzo fra quelle due date. Ma come faccio a confrontare le date? Fossero stati caratteri avrei usato strcmp, ma essendo una stringa contenente numeri non so come fare.  
Grazie mille.