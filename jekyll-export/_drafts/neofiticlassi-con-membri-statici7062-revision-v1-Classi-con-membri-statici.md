---
id: 7063
title: Classi con membri statici
date: 2016-11-14T09:33:24+01:00
author: Marco
layout: revision
guid: http://www.italiancpp.org/2016/11/14/7062-revision-v1/
permalink: /2016/11/14/7062-revision-v1/
---
Ciao a tutti, scusate la domanda banale ma ho un problema con l&#8217;utilizzo di membri static in C++.  
Ho creato la seguente classe di test:

[cce_cpp]  
// GlobalClass.h

class GlobalClass  
{  
public:  
~GlobalClass(void);  
GlobalClass(void);  
static int _counter;  
};  
[/cce_cpp]

con la relativa implementazione:

[cce_cpp]  
// GlobalClass.cpp  
#include &#8220;GlobalClass.h&#8221;

GlobalClass::GlobalClass(void)  
{  
GlobalClass::_counter = 0;  
}  
// &#8230;  
[/cce_cpp]

ma quando vado a compilare mi viene restituito questo errore:

> Errore 1 error LNK2001: simbolo esterno &#8220;public: static int GlobalClass::\_counter&#8221; (?\_counter@GlobalClass@@2HA) non risolto c:\documents and settings\epyplus\documenti\visual studio 2010\Projects\DemoCpp\DemoCpp\GlobalClass.obj DemoCpp  
> Errore 2 error LNK1120: 1 esterni non risolti c:\documents and settings\epyplus\documenti\visual studio 2010\Projects\DemoCpp\Debug\DemoCpp.exe DemoCpp 

Qualcuno saprebbe aiutarmi?

Grazie mille a tutti.

Marco