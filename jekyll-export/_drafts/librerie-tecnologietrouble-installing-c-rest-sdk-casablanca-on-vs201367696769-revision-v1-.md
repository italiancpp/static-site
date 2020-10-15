---
id: 6770
date: 2016-09-18T21:18:11+02:00
author: kenhero
layout: revision
guid: http://www.italiancpp.org/2016/09/18/6769-revision-v1/
permalink: /2016/09/18/6769-revision-v1/
---
purtroppo si,ho aggiunto il pacchetto nel mio progetto dopo averlo installato da nuget package manager ma ho ancora errori del genere

Error 9 error LNK2019: unresolved external symbol &#8220;\_\_declspec(dllimport) public: void \_\_thiscall web::http::details::\_http\_request::set\_request\_uri(class web::uri const &)&#8221; (\_\_imp\_?set\_request\_uri@\_http\_request@details@http@web@@QAEXABVuri@4@@Z) referenced in function &#8220;public: void \\_\_thiscall web::http::http\_request::set\_request\_uri(class web::uri const &)&#8221; (?set\_request\_uri@http\_request@http@web@@QAEXABVuri@3@@Z) C:\Users\Documents\Visual Studio 2013\Projects\flickr\flickr\flickr.obj flickr

web::http::client::http_client è la classe che mi dovrebbe dar problemi credo.  
Purtroppo uso visual studio da pochi mesi e non sono praticissimo