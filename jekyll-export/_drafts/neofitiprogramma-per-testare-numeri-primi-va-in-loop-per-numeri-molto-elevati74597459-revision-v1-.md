---
id: 7461
date: 2017-01-31T09:11:02+01:00
author: vix
layout: revision
guid: http://www.italiancpp.org/2017/01/31/7459-revision-v1/
permalink: /2017/01/31/7459-revision-v1/
---
Butto là un&#8217;idea: il programma calcola **sqrt(n)** sulla variabile **n** che è un **long int**.  
Può essere che **n** venga convertito in **double** prima di eseguire la radice quadrata? Magari questo può dare problemi.  
Hai provato a verificare la condizione **i*i<n**, gestendo l&#8217;eventuale overflow di **i*i**?