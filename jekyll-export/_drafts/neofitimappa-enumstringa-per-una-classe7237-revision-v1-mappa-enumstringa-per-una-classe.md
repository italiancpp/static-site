---
id: 7238
title: mappa enum/stringa per una classe
date: 2017-01-02T11:26:02+01:00
author: vix
layout: revision
guid: http://www.italiancpp.org/2017/01/02/7237-revision-v1/
permalink: /2017/01/02/7237-revision-v1/
---
ciao a tutti,  
questo è il mio primo post in questa community, ma spero sia solo l&#8217;inizio.  
Credo che la mia necessità sia abbastanza comune, ma pur avendo cercato un po&#8217;, non ho trovato una soluzione soddisfacente.

Devo creare una classe che rappresenti un tipo di dato enum; un esempio potrebbe essere il colore.  
[cce_cpp]class Colore{  
public:  
enum col {  
Rosso,  
Bianco,  
Nero  
};  
};[/cce_cpp]  
Ogni volta che la classe viene istanziata, lo specifico colore viene memorizzato assegnando il corretto valore all&#8217;enum.  
Vorrei però avere la possibilità di ottenere la rappresentazione del colore come stringa, ad esempio con una funzione membro tipo Colore::getStringa() che mi ritorni &#8220;Rosso&#8221;, &#8220;Bianco&#8221;, &#8230;

Un&#8217;idea potrebbe essere una mappa globale che leghi enum e rappresentazione testuale, ma non sono sicuro che questa sia la scelta migliore in c++.  
Come alternativa ho trovato riferimenti alla libreria <a href="https://github.com/aantron/better-enums" target="_blank">Better Enums</a>, che forse potrebbe essere quello che sto cercando.

Potete darmi qualche suggerimento?  
Grazie