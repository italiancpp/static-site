---
id: 6482
date: 2016-08-05T19:06:47+02:00
author: Stefano Famà
layout: revision
guid: http://www.italiancpp.org/2016/08/05/6481-revision-v1/
permalink: /2016/08/05/6481-revision-v1/
---
Purtroppo ora ho un altro problema.  
Errore C2338 Test writer must define specialization of ToString<const Q& q> for your class . Test c:\program files (x86)\microsoft visual studio 14.0\vc\unittest\include\cppunittestassert.h 66

Ho cercato su Internet e tutti dicono che basterebbe specializzare il template:  
da così:  
[cce_cpp]template <typename Q> static std::wstring ToString(const Q& q){}  
template <typename Q> static std::wstring ToString(const Q* q){}  
template <typename Q> static std::wstring ToString(Q* q){}[/cce_cpp]  
a così:  
[cce_cpp]template<> static std::wstring ToString<Bank::Money>(const Bank::Money& m);  
template<> static std::wstring ToString<Bank::Money>(const Bank::Money* m);  
template<> static std::wstring ToString<Bank::Money>(Bank::Money* m);[/cce_cpp]  
Io ho creato un **header**ed un **sorgente** **MoneyToString.h/.cpp  
** Ho messo **#include &#8220;MoneyToString.h&#8221;** nel mio **UnitTest.cpp**

La definizione è questa (ho usato anche -> per i puntatori)  
[cce_cpp]std::wstringstream ret;  
ret << m.getInteger() << &#8220;,&#8221; << m.getDecimal();  
ret.str();[/cce_cpp]

Però mi da comunque l&#8217;errore, non capisco perché&#8230;

Nel caso posto i file:  
MoneyToString.h  
[cce_cpp]#pragma once  
#include &#8220;stdafx.h&#8221;  
#include &#8220;CppUnitTest.h&#8221;

namespace Microsoft {  
namespace VisualStudio {  
namespace CppUnitTestFramework {  
template<> static std::wstring ToString<Bank::Money>(const Bank::Money& m);  
template<> static std::wstring ToString<Bank::Money>(const Bank::Money* m);  
template<> static std::wstring ToString<Bank::Money>(Bank::Money* m);  
}  
}  
}  
[/cce_cpp]UnitTest.cpp  
[cce_cpp]#include &#8220;stdafx.h&#8221;  
#include &#8220;CppUnitTest.h&#8221;  
#include &#8220;MoneyToString.h&#8221;

using namespace Microsoft::VisualStudio::CppUnitTestFramework;

namespace Test  
{  
TEST_CLASS(UnitTest1)  
{  
public:

TEST_METHOD(TestMethod1)  
{  
Bank::Money m;  
Assert::AreEqual((int64_t)0, m.getInteger());  
}

};  
}[/cce_cpp]