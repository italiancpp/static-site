---
id: 6465
title: Visual C++ 2015 Unit Test Nativo
date: 2016-08-05T15:37:26+02:00
author: Stefano Famà
layout: revision
guid: http://www.italiancpp.org/2016/08/05/6464-revision-v1/
permalink: /2016/08/05/6464-revision-v1/
---
Buon pomeriggio,  
sto usando Visual Studio 2015 Community Edition.  
Ho creato un Progetto Vuoto non gestito per il C++.  
Dopo ho aggiunto alla soluzione un Progetto di Test Nativo.  
Il progetto si presenta così:  
![Project](http://i67.tinypic.com/nly9g5.png) 

Ho aggiunto al progetto Test un riferimento al progetto BankSimulation.  
Se provo ad eseguire un Test tipo:  
[cce\_cpp]Assert::IsFalse(false);[/cce\_cpp]  
il Test risulta nell&#8217;elenco dei Test e passa con successo, niente errori.  
Se invece provo anche solo a fare:  
[cce_cpp]  
Money m;  
Assert::IsFalse(false);[/cce_cpp]  
Mi esce un errore:  
Errore LNK2019 riferimento al simbolo esterno &#8220;public: \_\_thiscall Money::Money(void)&#8221; (??0Money@@QAE@XZ) non risolto nella funzione &#8220;public: void \_\_thiscall Test::UnitTest1::TestMethod1(void)&#8221; (?TestMethod1@UnitTest1@Test@@QAEXXZ) Test C:\Users\famas\OneDrive\documenti\visual studio 2015\Projects\C++\BankSimulation\Test\unittest1.obj 1

Nelle proprietà di Test ho **Tipo Configurazione &#8211; Libreria Dinamica (.dll)**

Se invece cambio in .lib compila, ma i test non vengono rilevati né eseguiti.  
Non capisco dove sia il problema, sinceramente&#8230;  
Il problema sorge anche se rimuovo il riferimento al progetto BankSimulation.