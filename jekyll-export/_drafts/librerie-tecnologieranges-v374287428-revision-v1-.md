---
id: 7430
date: 2017-01-24T14:20:30+01:00
author: Marco Alesiani
layout: revision
guid: http://www.italiancpp.org/2017/01/24/7428-revision-v1/
permalink: /2017/01/24/7428-revision-v1/
---
Ciao Cristiano. 

Non sono un esperto in materia di ranges quindi prendi la mia opinione \*cum grano salis\*.

Ad un primo sguardo sembra che la sintassi e semantica di _yield\_from\_fn_ mimino un pò quella di _yield from_ in python (<a href="https://www.python.org/dev/peps/pep-0380/" target="_blank">https://www.python.org/dev/peps/pep-0380/</a>): ritornare una view dalla lambda al generatore padre. Se la lambda fosse stata una <a href="http://www.italiancpp.org/2016/11/02/coroutines-internals/" target="_blank">coroutine</a> la yield avrebbe trasferito il flusso di esecuzione e ritornato dati al chiamante. Dato che vi sono altre versioni come _yield\_if\_fn_ (che filtrano e/o applicano condizioni al valore di ritorno) è sensato averne una che in questo caso effettua solo il passaggio della view al chiamante. Ovviamente viene anche controllato che il range sia effettivamente una view (quindi non è soltanto un alias).