---
id: 7463
title: problemi in compilazione includendo la mia classe (undefined reference)
date: 2017-01-31T14:01:53+01:00
author: ma
layout: revision
guid: http://www.italiancpp.org/2017/01/31/7462-revision-v1/
permalink: /2017/01/31/7462-revision-v1/
---
Chiedo venia per il titolo, ma non avevo altre idee più chiare.  
Ad ogni modo:  
ho la seguente struttura di cartelle:  
/Json  
|-lib  
|-include  
|-hjson.h  
|-hjson.cpp  
|-main\_json\_test.cpp

Il codice hjson.h:  
[cce_cpp]  
#include <iostream>  
#include <sstream>  
#include <typeinfo>  
#include <string>  
#include <vector>

namespace HJSON{

enum class ItemTypes { jSTRING = 0, jNUMBER, jBOOLEAN, jCOLLECTION, jOBJECT };

class IJsonBaseObject {  
public:  
~IJsonBaseObject() {}  
virtual std::string GetTitle() { return this->Title; };  
virtual void SetTitle(std::string title) { this->Title = title; }  
virtual ItemTypes GetItemType() { return Type; }  
virtual void SetItemTypes(ItemTypes type) { this->Type = type; }

protected:  
ItemTypes Type;  
std::string Title;

};

// &#8220;title&#8221; : number  
// &#8220;title&#8221; : &#8220;string&#8221;  
// &#8220;title&#8221; : true/false  
class jItem : public IJsonBaseObject {  
public:  
jItem();  
std::string Value;  
std::string GetTitle() { return this->Title; };  
void SetTitle(std::string title) { this->Title = title; }  
ItemTypes GetItemType() { return Type; }  
void SetItemTypes(ItemTypes type) { this->Type = type; }

};

std::istream &operator>>(std::istream &is, jItem &item);  
std::ostream &operator<<(std::ostream &os, jItem &item);

class jObject : public IJsonBaseObject {  
public:  
jObject();  
std::vector<IJsonBaseObject> Attributes;  
std::string GetTitle() { return this->Title; };  
void SetTitle(std::string title) { this->Title = title; }  
ItemTypes GetItemType() { return Type; }  
void SetItemTypes(ItemTypes type) { this->Type = type; }

};

std::istream &operator>>(std::istream &is, jObject &obj);  
std::ostream &operator<<(std::ostream &os, jObject &obj);

class jCollection : public IJsonBaseObject {  
public:  
jCollection();  
std::vector<jObject> Objects;  
std::string GetTitle() { return this->Title; };  
void SetTitle(std::string title) { this->Title = title; }  
ItemTypes GetItemType() { return Type; }  
void SetItemTypes(ItemTypes type) { this->Type = type; }

};

std::istream &operator>>(std::istream &is, jCollection &coll);  
std::ostream &operator<<(std::ostream &os, jCollection &coll);

}  
[/cce_cpp]

hjson.cpp:  
[cce_cpp]  
#include &#8220;hJson.h&#8221;

namespace HJSON{

std::istream &operator>>(std::istream &is, jItem &item) {  
char ch1;  
is >> ch1;  
if (std::string(ch1,1) != &#8220;\&#8221;&#8221;) {  
// commento per apparare il doppio apice qui sopra &#8221;  
is.unget();  
is.clear(std::ios::ios_base::failbit);  
return is;  
}

std::string title;  
char ch2;  
char firstValueChar;  
std::string value;  
std::string type;

is >> title >> ch2;  
if (!is || std::string(ch2,1) != &#8220;\&#8221;&#8221;) {  
// commento per apparare il doppio apice qui sopra &#8221;  
printf(&#8220;Error 1 109 26 1: %s&#8221;, title.c_str());  
return is;  
}  
is >> firstValueChar;  
if (!is) {  
printf(&#8220;Error 1 109 26 2 A&#8221;);  
return is;  
};  
if (std::string(firstValueChar,1) != &#8220;\&#8221;&#8221;) {  
// commento per apparare il doppio apice qui sopra &#8221;  
item.SetItemTypes(HJSON::ItemTypes::jSTRING);

std::string jsonValue;  
const char *closing = &#8220;\&#8221;&#8221;;  
std::getline(is, jsonValue, *closing);

item.Value = jsonValue;

} else if (firstValueChar == &#8216;t&#8217; || firstValueChar == &#8216;f&#8217;) {  
item.SetItemTypes(HJSON::ItemTypes::jBOOLEAN);

std::string jsonValue;  
std::getline(is, jsonValue);  
item.Value = jsonValue;  
} else if (isdigit(firstValueChar)) {  
// se ho trovato un valore numerico, riposiziono il carattere appena letto  
// nello stream  
is.unget();  
item.SetItemTypes(HJSON::ItemTypes::jNUMBER);

is >> value;  
if (!is) {  
printf(&#8220;Error 1 109 26 2 A&#8221;);  
return is;  
};

item.Value = value;  
} else {  
printf(&#8220;Error 1 509 26 3&#8221;);  
return is;  
}  
is >> ch2;  
if (!is || ch2 != &#8216;}&#8217;) {  
printf(&#8220;Error 1 109 26 3&#8243;);  
return is;  
};  
item.SetTitle(title.substr(1, title.size() &#8211; 2));

return is;  
}

std::ostream &operator<<(std::ostream &os, jItem &item) {  
// TODO: insert return statement here  
os << &#8221; \&#8221;&#8221; << item.GetTitle() << &#8220;\&#8221; : &#8220;;  
if (item.GetItemType() == HJSON::ItemTypes::jSTRING) {  
os << &#8220;&#8216;&#8221; << item.Value << &#8220;&#8216;&#8221;;  
}  
if (item.GetItemType() == HJSON::ItemTypes::jNUMBER) {  
os << item.Value;  
}  
if (item.GetItemType() == ItemTypes::jBOOLEAN) {  
os << item.Value;  
}

os << &#8221; } &#8220;;  
return os;  
}

// &#8220;title&#8221; : { item[,item,&#8230;]}  
std::istream &operator>>(std::istream &is, jObject &obj) {  
char ch1;  
is >> ch1;  
if (std::string(ch1,1) != &#8220;\&#8221;&#8221;) {  
is.unget();  
is.clear(std::ios::ios_base::failbit);  
return is;  
}  
std::string title;  
char ch2; // &#8221;  
char ch3; // {  
std::string value;  
std::string type;

is >> title >> ch2;  
if (!is || std::string(ch2,1) != &#8220;\&#8221;&#8221;) {  
printf(&#8220;Error 1 109 26 1: %s&#8221;, title.c_str());  
return is;  
}  
obj.SetTitle(title);  
is >> ch3;  
if (!is || std::string(ch3,1) != &#8220;{&#8220;) {  
printf(&#8220;Error 1 109 26 1 C: %s&#8221;, title.c_str());  
return is;  
}

char ch4; // }  
char ch5; // ,

do {  
//is >> child;  
if( typeid(obj).name() == std::string(&#8220;jCollection&#8221;)){  
jCollection& type\_coll = dynamic\_cast<jCollection &>(obj);  
is >> type_coll;  
obj.Attributes.push\_back(type\_coll);  
}  
else if( typeid(obj).name() == std::string(&#8220;jObject&#8221;)){  
jObject& type\_obj = dynamic\_cast<jObject &>(obj);  
is >> type_obj;  
obj.Attributes.push\_back(type\_obj);  
}  
else if( typeid(obj).name() == std::string(&#8220;jItem&#8221;)){  
jItem& type\_item = dynamic\_cast<jItem &>(obj);  
is >> type_item;  
obj.Attributes.push\_back(type\_item);  
}  
if (!is) {  
printf(&#8220;Error 1 109 26 2 F1&#8221;);  
return is;  
};

is >> ch5;  
} while (ch5 == &#8216;,&#8217;);

is >> ch4;  
if (!is || ch4 != &#8216;}&#8217;) {  
printf(&#8220;Error 1 109 26 3&#8243;);  
return is;  
};  
return is;  
}

std::ostream &operator<<(std::ostream &os, jObject &obj) {  
if (obj.GetItemType() == HJSON::ItemTypes::jOBJECT) {  
os << &#8221; \&#8221;&#8221; << obj.GetTitle() << &#8220;\&#8221; : &#8220;;  
os << &#8221; { &#8220;;  
bool first_attr = true;  
for(auto item : obj.Attributes){  
if(!first_attr){  
first_attr = false;  
}  
else{  
os << &#8221; , &#8220;;  
}  
os << &item;  
}  
os << &#8221; } &#8220;;  
}  
else{  
printf(&#8220;Error 1 167 0D 3&#8243;);  
}  
os << &#8221; } &#8220;;  
return os;  
}

std::ostream &operator<<(std::ostream &os, IJsonBaseObject &obj) {

if( typeid(obj).name() == std::string(&#8220;jCollection&#8221;)){  
jCollection& type\_coll = dynamic\_cast<jCollection &>(obj);  
os << type_coll;  
}  
else if( typeid(obj).name() == std::string(&#8220;jObject&#8221;)){  
jObject& type\_obj = dynamic\_cast<jObject &>(obj);  
os << type_obj;  
}  
else if( typeid(obj).name() == std::string(&#8220;jItem&#8221;)){  
jItem& type\_item = dynamic\_cast<jItem &>(obj);  
os << type_item;  
}  
else{  
printf(&#8220;Error 1 162 35 3&#8221;);  
}  
return os;  
}

// &#8220;title&#8221; : [ { item[,item,&#8230;]},&#8230; ]  
std::istream &operator>>(std::istream &is, jCollection &coll) {  
char ch1;  
is >> ch1;  
if (std::string(ch1,1) != &#8220;\&#8221;&#8221;) {  
is.unget();  
is.clear(std::ios::ios_base::failbit);  
return is;  
}  
std::string title;  
char ch2; // &#8221;  
char ch3; // [  
jObject *obj = new jObject();  
//std::string value;  
std::string type;

is >> title >> ch2;  
if (!is || std::string(ch2,1) != &#8220;\&#8221;&#8221;) {  
printf(&#8220;Error 1 109 26 1: %s&#8221;, title.c_str());  
return is;  
}  
is >> ch3;  
if (!is || std::string(ch3,1) != &#8220;[&#8220;) {  
printf(&#8220;Error 1 109 26 1 C: %s&#8221;, title.c_str());  
return is;  
}

char ch4; // ]  
char ch5; // ,

do {  
is >> *obj;  
if (!is) {  
printf(&#8220;Error 1 109 26 2 F1&#8221;);  
return is;  
};

is >> ch5;  
} while (ch5 == &#8216;,&#8217;);

//obj->Value = value;

is >> ch4;  
if (!is || std::string(ch4,1) != &#8220;]&#8221;) {  
printf(&#8220;Error 1 109 26 3&#8243;);  
return is;  
};  
obj->SetTitle(title.substr(1, title.size() &#8211; 2));

return is;  
}

std::ostream &operator<<(std::ostream &os, jCollection &coll) {  
// TODO: insert return statement here

if (coll.GetItemType() == HJSON::ItemTypes::jCOLLECTION) {  
os << &#8221; \&#8221;&#8221; << coll.GetTitle() << &#8220;\&#8221; : &#8220;;  
os << &#8221; [ &#8220;;  
bool first_attr = true;  
for(auto obj : coll.Objects){  
if(!first_attr){  
first_attr = false;  
}  
else{  
os << &#8221; , &#8220;;  
}  
os << obj;  
}  
os << &#8221; ] &#8220;;  
}  
else{  
printf(&#8220;Error 1 167 5D 3&#8243;);  
}  
os << &#8221; } &#8220;;  
return os;  
}

}  
[/cce_cpp]

ed infine main\_json\_text.cpp:  
[cce_cpp]  
#include <string>  
#include <vector>  
#include <iostream>  
#include <sstream>  
#include <typeinfo>  
#include &#8220;hjson.h&#8221;

using namespace HJSON;

int main(){

HJSON::jItem *item = new HJSON::jItem();  
item->SetItemTypes(HJSON::ItemTypes::jSTRING);  
item->SetTitle(&#8220;a&#8221;);  
item->Value = &#8220;test a&#8221;;

HJSON::jItem *item1 = new HJSON::jItem();  
item1->SetItemTypes(HJSON::ItemTypes::jNUMBER);  
item1->SetTitle(&#8220;b&#8221;);  
item1->Value = &#8220;123&#8221;;

HJSON::jItem *item\_child\_1 = new HJSON::jItem();  
item\_child\_1->SetItemTypes(HJSON::ItemTypes::jNUMBER);  
item\_child\_1->SetTitle(&#8220;b&#8221;);  
item\_child\_1->Value = &#8220;123&#8221;;

HJSON::jObject *child_1 = new HJSON::jObject();  
child_1->SetItemTypes(HJSON::ItemTypes::jOBJECT);  
child\_1->SetTitle(&#8220;child\_1&#8221;);  
child\_1->Attributes.push\_back(*item\_child\_1);

HJSON::jItem *item\_child\_2 = new HJSON::jItem();  
item\_child\_2->SetItemTypes(HJSON::ItemTypes::jNUMBER);  
item\_child\_2->SetTitle(&#8220;b&#8221;);  
item\_child\_2->Value = &#8220;123&#8221;;

HJSON::jObject *child_2 = new HJSON::jObject();  
child_2->SetItemTypes(HJSON::ItemTypes::jOBJECT);  
child\_2->SetTitle(&#8220;child\_2&#8221;);  
child\_2->Attributes.push\_back(*item\_child\_2);

HJSON::jCollection *coll = new HJSON::jCollection();  
coll->SetItemTypes(HJSON::ItemTypes::jCOLLECTION);  
coll->SetTitle(&#8220;collection&#8221;);  
coll->Objects.push\_back(*child\_1);  
coll->Objects.push\_back(*child\_2);

HJSON::jObject *root = new HJSON::jObject();  
root->SetItemTypes(HJSON::ItemTypes::jOBJECT);  
root->SetTitle(&#8220;root&#8221;);  
root->Attributes.push_back(*item);  
root->Attributes.push_back(*item1);  
root->Attributes.push_back(*coll);

std::cout << root;  
std::cin.get();

return 0;  
}  
[/cce_cpp]

per compilare il tutto uso i seguenti comandi:  
[cce_cpp]  
rem ############## compila in *.o ##############  
g++ -c ./hjson.cpp -Wall -Werror -Wformat -std=c++11 -o./lib/hjson.o  
rem ############## crea lib ##############  
ar cr ./lib/hjson.lib ./lib/hjson.o  
rem ############## cancella ./hjson.o ##############  
del .\..\Json\lib\hjson.o  
rem ############## compila con test ##############  
g++ -g ./main\_json\_test.cpp -l:./lib/hjson.lib -Wall -Werror -Wformat -std=c++11 ./lib/hjson.lib -o./lib/test_hjson.exe  
[/cce_cpp]

Il problema è che quando provo a compilare il main\_json\_text.cpp ricevo errori di tipo undefined reference nel file main\_json\_test.cpp per tuttli gli oggetti dichiarati nel hjson.h. Credo l&#8217;errore sia del linker, poichè alla fine recita: error: ld returned 1 exit status  
Sono su windows 10 e per installare i vari pacchetti ho utilizzato win-builds(v1.5.0)

Dove sbaglio?  
Qualche idea?

ps. credo si intuisca, comunque il desiderata è lo scrivere una classe per la serializzazione deserializzazione in json.