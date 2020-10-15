---
id: 6767
title: Problemi installazione C++ REST SDK (Casablanca) su VS2013
date: 2016-09-18T17:53:16+02:00
author: marco
layout: revision
guid: http://www.italiancpp.org/2016/09/18/6756-revision-v1/
permalink: /2016/09/18/6756-revision-v1/
---
Salve a tutti,

in ottica di una offerta di lavoro in remote devo implementare un http client in c++ tramitela libreria c++ sdk casablanca.  
Sto avendo un po&#8217; di difficoltà a trovare la procedura corretta per poterla installare ed iniziare a fare delle prove.  
In particolare ho scaricato questo esempio di http client da questo link

http://www.drdobbs.com/windows/using-the-microsoft-c-rest-sdk/240164544?pgno=2  
[](http://www.drdobbs.com/windows/using-the-microsoft-c-rest-sdk/240164544?pgno=2)

ma ho dei problemi in fase di compilazione con visual studio ossia degli errori del genere

Error 1 error LNK2019: unresolved external symbol &#8220;\_\_declspec(dllimport) public: \_\_thiscall web::uri::uri(wchar\_t const *)&#8221; (\\_\_imp\_??0uri@web@@QAE@PB\_W@Z) referenced in function &#8220;class Concurrency::task \_\_cdecl HTTPGetAsync(void)&#8221; (?HTTPGetAsync@@YA?AV?$task@X@Concurrency@@XZ) flickr.obj

Error 2 error LNK2019: unresolved external symbol &#8220;\_\_declspec(dllimport) public: \_\_thiscall web::uri::uri(class std::basic\_string,class std::allocator > const &)&#8221; (\\_\_imp\_??0uri@web@@QAE@ABV?$basic\_string@\_WU?$char\_traits@\_W@std@@V?$allocator@\_W@2@@std@@@Z) referenced in function &#8220;public: class Concurrency::task \_\_thiscall web::http::client::http\_client::request(class std::basic\_string,class std::allocator > const &,class std::basic\_string,class std::allocator > const &,class Concurrency::cancellation\_token const &)&#8221; (?request@http\_client@client@http@web@@QAE?AV?$task@Vhttp\_response@http@web@@@Concurrency@@ABV?$basic\_string@\_WU?$char\_traits@\_W@std@@V?$allocator@\_W@2@@std@@0ABVcancellation\_token@6@@Z) flickr.obj

qualcuno in grado di darmi delle dritte?  
Ringrazio anticipatamente