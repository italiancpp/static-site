---
id: 6814
title: std::locale
date: 2016-09-26T22:26:28+02:00
author: ing82
layout: revision
guid: http://www.italiancpp.org/2016/09/26/6813-revision-v1/
permalink: /2016/09/26/6813-revision-v1/
---
Quanto sto per chiedere credo che sia un argomento abbastanza vasto, ma essendo la prima volta che mi ci scontro e non risucendo a chiarirmi le idee con la documentazione presente in rete, provo a formulare la domanda, ma credo che se qualcuno avrà tempo da dedicarmi sarà lui a farmi domande per indirazzarmi meglio a comprendere questo argomento: ci provo.  
Vorrei capire fino a quando posso continuare a trascurare le &#8220;impostazioni internazionali&#8221; del sistema operativo nei confronti del corretto funzionamento dei miei programmini e quando invece cominciare a trattare anche questo argomento.  
Faccio un esempio: io ho il pc con Windows 10, e il separatore dei decimali è la virgola.  
Quando sono nella console del programma che creo, dato che in automatico usa il suo standard locale, il separatore decimale è il punto.  
A questo punto credo che possa diventare un problema nel momento in cui dovrò andare a leggere/scrivere numeri con decimali su file di testo, ad esempio: se il numero sul file di testo è con la virgola, ma il programma viaggia col suo standard locale considerando il punto come separatore, credo che qualche problema possa nascere.  
Dato che i programmini che faccio mi sono da supporto per la mia attività lavorativa, ho predisposto una classe MyValidator, in cui ho implementato una serie di metodi statici read che mi permettono di validare l&#8217;input (per int, per unsigned int, per char, per double, ecc). Nell&#8217;esempio sopra citato, il mio metodo read, se scrivo 3,2 mi da errore, nonstante il SO sia impostato con la virgola, mentre mi valida l&#8217;input se scrivo 3.2.  
Altro problema potrebbe essere il fatto che i file di testo coi numeri da leggere potrebbero derivare da output di altri programmi, quindi potrebbero essere o con la virgola o col punto.  
Come si fa in questi casi?

Grazie