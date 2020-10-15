---
id: 6661
date: 2016-08-31T16:02:16+02:00
author: Stefano Famà
layout: revision
guid: http://www.italiancpp.org/2016/08/31/6660-revision-v1/
permalink: /2016/08/31/6660-revision-v1/
---
Io ho fatto così:  
[cce_cpp]#include <iostream>

using namespace std;

enum Currency { USD, EUR, CHK };

class M {  
public:  
M(Currency c) : cur(c) {};  
Currency cur;  
Currency get_cur() const { return cur; }  
};

ostream& operator<<(ostream& os, Currency& c) {  
if (c == Currency::EUR)  
return os << &#8220;EUR&#8221;;  
if (c == Currency::USD)  
return os << &#8220;USD&#8221;;  
if (c == Currency::CHK)  
return os << &#8220;CHK&#8221;;  
}

// versione 1 -> stampa un intero  
ostream& operator<<(ostream& os, M& m) {  
return os << m.get_cur() << m.cur;  
}

int main() {  
M m{ Currency::EUR };  
std::cout << m << std::endl;

getchar();  
}[/cce_cpp]

Semplicemente ho aggiunto **<< m.cur;**

P.S.  
Costruttori e/o include vari sono stati aggiunti x compilare.