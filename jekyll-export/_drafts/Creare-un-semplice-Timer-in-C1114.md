---
id: 6088
title: Creare un semplice Timer in C++11/14
date: 2017-05-22T20:35:33+02:00
author: Elvis
layout: post
guid: http://www.italiancpp.org/?p=6088
permalink: /?p=6088
evolve_sidebar_position:
  - default
evolve_full_width:
  - 'no'
evolve_page_title:
  - 'yes'
evolve_page_breadcrumb:
  - 'yes'
evolve_widget_page:
  - 'no'
evolve_slider_position:
  - default
evolve_slider_type:
  - 'no'
wp_sponsor_link_behaviour:
  - "0"
---
&nbsp;

,In questo articolo vorrei condividere con voi una classe estremamente facile quanto utile ovvero un semplice Timer.

Per quanto semplice è difficile trovare una implementazione su un timer ad alta precisione che sia cross platform. Il nuovo standard di C++ ha semplificato molto introducendo strumenti per misurare durate nel tempo.

Tutte le funzionalità sono incapsulate nel namespace chrono. C++ introduce diversi concetti:

  1. **epoch**: un epoca rappresenta un punto di inizio. Ad esempio nel calendario gregoriano (il nostro) l&#8217;epoca è rappresentata dall&#8217;anno 0. Nei sistemi posix l&#8217;epoca inizia spesso 01/01/1970 00:00:00.
  2. **time_point**: rappresenta un periodo di tempo a partire da un&#8217;epoca specificata.
  3. **duration**: rappresenta un intervallo di tempo, rappresentata da un numero di &#8220;tick&#8221; di qualche unità di misura. Ad esempio 43s possono essere 43 tick di 1 secondo oppure 43000 da 1ms. Un tick può essere anche più strano come ad esempio 5/12us.
  4. **clock**: non è altro che un epoca e una frequenza di tick, ovvero il tempo che trascorre fra due tick consecutivi.

Con questi 4 semplici concetti possiamo rappresentare in modo estremamente generico e preciso durate nel tempo.

Il C++ ha introdotto i seguenti clock:

  * **system_clock**: realtime clock usato dal sistema operativo.
  * **steady_clock**: time monolitico: ovvero non può mai ritornare indietro nel tempo.
  * **high\_resolution\_clock**: orologio con la più alta risoluzione (ovvero con il minor tick rate).

Per un timer sembrerebbe che il clock migliore sia steady\_clock anche se in questo tutorial userò sempre l&#8217;high\_resolution_clock.

Dopo tanta teoria di seguito un piccolo esempio su come usarli.

[compiler]  
#include <iostream>  
#include <chrono>  
#include <thread>// usato per fare delle sleep

using namespace std;

int main()  
{  
using Clock = chrono::high\_resolution\_clock;  
auto t1 = Clock::now();  
this\_thread::sleep\_for(std::chrono::seconds(3));  
auto t2 = Clock::now();

auto elapsed = t2 &#8211; t1;

cout << &#8220;t2 &#8211; t1 = &#8221; << t1 << &#8221; &#8211; &#8221; << t2 << elapsed.count() << endl;  
return EXIT_SUCCESS;  
}  
[/compiler]

[compiler]  
#include <iostream>  
#include <chrono>  
#include <thread>// usato per fare delle sleep

using namespace std;

int main()  
{  
cout << &#8220;ciao mondo&#8221; << endl;  
return EXIT_SUCCESS;  
}  
[/compiler]

high\_resolution\_clock