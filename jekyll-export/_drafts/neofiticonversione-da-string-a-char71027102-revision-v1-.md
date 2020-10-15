---
id: 7103
date: 2016-11-25T14:14:14+01:00
author: marco
layout: revision
guid: http://www.italiancpp.org/2016/11/25/7102-revision-v1/
permalink: /2016/11/25/7102-revision-v1/
---
Pre-C++17 teoricamente no perché non è permesso modificare il buffer interno della stringa. Dal C++17 string::data() ha un overload che torna char\* invece di const char\* quindi è fattibile.

Il &#8220;teoricamente&#8221; è dovuto al fatto che puoi sempre fare una porcata e togliere la constness con un cast:

[cce_cpp]  
// non portabile pre-C++71  
strtok(const\_cast<char*>(str.data()), delims);[/cce\_cpp]

Resta una porcata&#8230;E comunque strtok cambia la stringa originale (e.g. infila degli \0 al posto dei delimitatori), il che non è sempre quello che vuoi.