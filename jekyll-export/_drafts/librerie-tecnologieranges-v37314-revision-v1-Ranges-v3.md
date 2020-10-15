---
id: 7315
title: Ranges v3
date: 2017-01-19T12:52:41+01:00
author: marco
layout: revision
guid: http://www.italiancpp.org/2017/01/19/7314-revision-v1/
permalink: /2017/01/19/7314-revision-v1/
---
Ciao a tutti, sto studiando la libreria (e i concetti sottesi) Ranges V3. Mi affascina molto il concetto di range. Ho letto anche qualche articolo, come suggerito e la specifica (che fatica!) di Niebler. Cosi ho importato nel mio Gcc 6 l&#8217;header e ho iniziato a fare qualche esempio. Mi sono trovato davanti a uno snippet che non riesco a comprendere appieno:

[cce_cpp]std::vector<int> vii =  
view::for_each(view::ints(1,10), [](int i){  
return yield\_from(view::repeat\_n(i,i));  
});[/cce_cpp]

Ora, quello che non mi è chiaro è &#8220;yield\_from&#8221;. Ho provato il codice anche senza il metodo e funziona allo stesso modo. Sono andato a guardarmi il codice sorgente (che non è proprio semplice per quanto mi riguarda). Ora se ho capito bene, yield\_from altro non è che un &#8220;alias&#8221; (non saprei come chiamarlo) a yield\_from\_fn che mi sembra un funtore. 

[cce\_cpp]/// \relates yield\_fn  
/// \ingroup group-views  
RANGES\_INLINE\_VARIABLE(yield_fn, yield)

struct yield\_from\_fn  
{  
template<typename Rng, CONCEPT\_REQUIRES\_(View<Rng>())>  
Rng operator()(Rng rng) const  
{  
return rng;  
}  
};[/cce_cpp]

Mi sembra di capire che ritorni un range da una vista, visto il concept, sbaglio? però, come detto il primo snippet funziona anche senza yield_from. Mi potete illuminare?

Cristiano