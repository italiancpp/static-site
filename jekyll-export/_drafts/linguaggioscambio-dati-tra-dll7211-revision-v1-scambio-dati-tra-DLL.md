---
id: 7212
title: scambio dati tra DLL
date: 2016-12-21T18:35:46+01:00
author: Giorgio
layout: revision
guid: http://www.italiancpp.org/2016/12/21/7211-revision-v1/
permalink: /2016/12/21/7211-revision-v1/
---
Devo &#8220;ristrutturare&#8221; un&#8217;applicazione composta da diverse DLL che tra di loro si devono condividere una grossa mole di dati. Attualmente come tecnica di condivisione vengono utilizzati file XML, ma naturalmente i tempi di esecuzione delle fasi di lettura e scrittura rallentano notevolmente l&#8217;esecuzione dell&#8217;applicazione. L&#8217;idea è quindi quella di eliminare i file XML, in alternativa quale può essere la tecnica / strumento migliore a livello di prestazioni per condividere questi dati?

Grazie