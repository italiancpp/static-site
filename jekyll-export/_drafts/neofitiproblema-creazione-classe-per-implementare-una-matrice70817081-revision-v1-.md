---
id: 7082
date: 2016-11-19T18:46:19+01:00
author: Stefano Famà
layout: revision
guid: http://www.italiancpp.org/2016/11/19/7081-revision-v1/
permalink: /2016/11/19/7081-revision-v1/
---
Ciao,  
nell&#8217;altro thread mi avevi chiesto se valeva la pena creare una classe per le matrici, bè dipende, se stai imparando, come me, ne vale la pena sicuramente &#x1f642;

Non ho provato il codice ma ad occhio credo che il problema sia nel vettore.  
Hai un **vector<vector<int>>** ok.

**Ma di che dimensioni?**

E&#8217; vero che vector cresce dinamicamente ma non come fai tu.  
Nella classe **initializeMatrix** accedi alla matrice con l&#8217;operatore **[ ]**.  
Ma tu tenti di accedere ad un vector di dimensioni non definite.  
Ti consiglio di usare la funzione <a href="http://en.cppreference.com/w/cpp/container/vector/resize" target="_blank">resize()</a>.