---
id: 6643
title: const o non const
date: 2016-08-29T09:32:59+02:00
author: ma
layout: revision
guid: http://www.italiancpp.org/2016/08/29/6642-revision-v1/
permalink: /2016/08/29/6642-revision-v1/
---
Mi scuso subito per il titolo del post, ma non mi è venuto in mente nulla di meglio, ad ogni modo:  
sto seguendo il libro di stroustrup ed mi ritrovo con un errore in compilazione sugli esempi del capitolo 9. Ho la seguente definizione di classe:  
[cce_cpp]  
class Date{  
public:  
Date(int y, Month m, int d);  
Date();  
Month month() {return m};  
int day() {return d};  
int year() {return y};  
&#8230;  
private:  
int y, d;  
Month m;  
}  
[/cce_cpp]  
Dove Month è una enum class con i 12 mesi dell&#8217;anno.  
Come mi pare logico, nel libro si suggerisce di creare un metodo per settare il valore di default per i costruttori con meno di 3 argomenti, quindi:  
[cce_cpp]  
const Date& default_date(){  
staticDate dd{2000, Month::jan, 1};  
return dd;  
}  
[/cce_cpp]  
Però, quando vado a definire il costruttore di default:  
[cce_cpp]  
Date::Date() :  
y{default_date().year()}, // errore  
m{default_date().month()}, // errore  
d{default_date().day()} // errore  
{ }  
[/cce_cpp]  
Il compilatore mi dà il seguente errore sull&#8217;inizializzazione dei valori mese, giorno ed anno:  
The object has type qualifiers that are not compatible with the member function &#8220;Date::year&#8221;

togliendo il const alla definizione del metodo default_date() gli errore spariscono, ma non capisco il perchè:  
secondo la mia logica, evidentemente errata, il const fa riferimento all&#8217;oggetto Date e non ai suoi membri, indi: perchè questa segnalazione?  
Grazie  
Sergio