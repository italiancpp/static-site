---
id: 7021
title: ricerca ricorsiva su struttura ad albero
date: 2016-11-04T09:55:12+01:00
author: ma
layout: revision
guid: http://www.italiancpp.org/2016/11/04/7019-revision-v1/
permalink: /2016/11/04/7019-revision-v1/
---
Ciao a tutti,  
dopo aver superato la stampa, ora stavo provando a scrivere una classe per implementare la serializzazione/deserializzazione json, so che sarebbe superfluo viste le decine di librerie già esistenti ma il mio vuole essere solo un esercizio, per il momento&#8230; &#x1f600;

Ad ogni modo, ho queste classi:  
[cce_cpp]  
//HJson.h

class Item {  
public:  
std::string Title;  
ItemTypes Type;  
std::string Value;

std::vector<Item> Childs;  
Item* findByTitle(std::string title);  
};

class HJson  
{  
public:  
HJson();  
HJson(std::string jsonString);  
~HJson();

void AddItem(Item &item);  
std::string ToString();  
Item * findByTitle(std::string title);

private:  
Item root;  
std::string Jsonize(Item &item);

};

std::istream& operator >> (std::istream& is, Item& item);  
std::ostream& operator << (std::ostream& os, Item& item);  
[/cce_cpp]  
ed il mio problema è sulla implementazione del metodo find dell&#8217;Item(la cui intenzione era trovare il nodo corretto e riportarmi su il riferimento allo specifico Item nello stack fino al primo chiamante):  
[cce_cpp]  
Item * HJson::findByTitle(std::string title) {  
Item * node;  
node = root.findByTitle(title);  
return node;  
}

Item* Item::findByTitle(std::string title)  
{  
if (this->Title == title) {  
return this;  
}  
else {  
for each (Item child in this->Childs)  
{  
Item* childItem = child.findByTitle(title);  
if (childItem != nullptr) {  
return childItem;  
}  
}  
}  
return nullptr;  
}  
[/cce_cpp]  
Ovviamente non funge, l&#8217;item viene trovato ma si perde nei meandri dei ritorni ricorsivi, ho provato a fare delle modifiche, provando con riferimenti, cloni ed altro, ma non ne sono venuto a capo, c&#8217;è qualcosa che non riesco a cogliere, indi: cosa mi perdo? quale sarebbe una implementazione corretta e funzionante?

Per completezza aggiungo il codice di test  
[cce_cpp]  
HJson root = HJson();  
Item it;  
it.Title = &#8220;Config&#8221;;  
it.Type = ItemTypes::COLLECTION;

Item child1;  
child1.Title = &#8220;ServerIpAddress&#8221;;  
child1.Type = ItemTypes::STRING;  
child1.Value = &#8220;127.0.0.1&#8221;;  
it.Childs.push_back(child1);

Item child2;  
child2.Title = &#8220;RdpFilePath&#8221;;  
child2.Type = ItemTypes::STRING;  
child2.Value = &#8220;C:\\Users\\&#8230;.\\MyFiles\\macchina outlook.rdp&#8221;;  
//child2.Value = &#8220;PATH\_TO\_RDP&#8221;;  
it.Childs.push_back(child2);

Item child3;  
child3.Title = &#8220;Issuer&#8221;;  
child3.Type = ItemTypes::STRING;  
child3.Value = &#8220;History in da LA&#8221;;  
//child2.Value = &#8220;PATH\_TO\_RDP&#8221;;  
it.Childs.push_back(child3);

root.AddItem(it);

Item * configServerIpAddress = root.findByTitle(&#8220;ServerIpAddress&#8221;);  
[/cce_cpp]

Sergio