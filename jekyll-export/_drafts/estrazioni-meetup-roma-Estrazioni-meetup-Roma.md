---
id: 5000
title: Estrazioni meetup Roma
date: 2015-10-24T11:29:19+02:00
author: marco
layout: post
guid: http://www.italiancpp.org/?p=5000
permalink: /?p=5000
---
[compiler]

<pre>static const int ESTRAZIONE = 0;

#include &lt;iostream&gt;
#include &lt;random&gt;
#include &lt;vector&gt;
#include &lt;algorithm&gt;
#include &lt;iterator&gt;

using namespace std;

extern vector&lt;string&gt; names;

int main()
{ 
    if (!ESTRAZIONE) {
        sort(begin(names), end(names));
        for (auto& n : names)
            cout &lt;&lt; n &lt;&lt; endl;
    } else {

        auto engine = std::default_random_engine(std::random_device{}());

        shuffle(begin(names), end(names), engine);

        cout &lt;&lt; "And the winner is..." &lt;&lt; endl;
        cout &lt;&lt; names[ESTRAZIONE] &lt;&lt; endl;
    }
}

vector&lt;string&gt; names = {
"valentino alessandroni",
"Alessio pinato",
"Valentino Picotti",
"Federico Guerra",
"Donato Taronna",
"Andrea Properzi",
"Giorgio Tedesco",
"stefano artuso",
"Marzia Dominici",
"holsi hasanaj",
"Emiliano D'Ortenzi",
"Fabrizio Barcaroli",
"Luca Calabria",
"Andrea Iuliano",
"Valerio Cestarelli",
"Annalisa Pagnozzi",
"Antonio D'Angelico",
"Nino Magazzù",
"Alfredo Di Napoli",
"Paolo Manco",
"andrea barbadoro",
"Franco Milicchio"
};
</pre>

[/compiler]