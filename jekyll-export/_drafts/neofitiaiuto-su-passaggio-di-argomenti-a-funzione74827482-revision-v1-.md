---
id: 7483
date: 2017-02-03T13:18:14+01:00
author: Stefano
layout: revision
guid: http://www.italiancpp.org/2017/02/03/7482-revision-v1/
permalink: /2017/02/03/7482-revision-v1/
---
Perchè nel primo caso quando chiami **elimina** la prima volta stai usando le variabili globali **num_esami** e **num_studenti** che hai _definito nel **main**_ e che sono **int**, quindi giustamente per avere un **int*** fai riferimento al loro indirizzo con **&**.  
Quando poi chiami l&#8217;altra funzione dall&#8217;interno di elimina num\_esami e num\_studenti sono nomi che si riferiscono _ai parametri della funzione **elimina** che sono già **int***_, ovvero gli indirizzi delle variabili globali che avevi passato prima.  
Per questo è sbagliato passarli usando &num_XXX perchè sarebbe praticamente passare un **int****, un puntatore a un puntatore, _non un int*_.  
Spero si capisca l&#8217;inghippo.