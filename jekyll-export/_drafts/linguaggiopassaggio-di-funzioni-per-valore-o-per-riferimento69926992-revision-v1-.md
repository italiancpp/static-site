---
id: 6995
date: 2016-11-02T16:28:14+01:00
author: Manlio
layout: revision
guid: http://www.italiancpp.org/2016/11/02/6992-revision-v1/
permalink: /2016/11/02/6992-revision-v1/
---
Una prima osservazione è che non c&#8217;è bisogno di scrivere:

[cce\_cpp]useFunction2(&square, 3);[/cce\_cpp]

Nel contesto in cui lo stai utilizzando, il simbolo &#8216;&&#8217; di fronte al nome di funzione ha il significato di _address-of operator_.

Visto che:

[cce\_cpp]int (*f)(int) = &square;[/cce\_cpp]

è equivalente a:

[cce\_cpp]int (*f)(int) = square;[/cce\_cpp]

la useFunction2 riceve un puntatore a funzione comunque.

&#8212;

Con la prima chiamata (useFunction) viene creata una std::function a partire da un puntatore a funzione. Un po&#8217; come se scrivessi:

[cce_cpp]int useFunction(int (*fun)(int), int val)  
{  
std::function<int(int)> tmp(fun);

cout << tmp(val) << endl;  
}[/cce_cpp]

Nel secondo caso (useFunction2) viene comunque creato un oggetto temporaneo di tipo std::function (a partire da un puntatore) che verrà utilizzato tramite un riferimento costante. Un po&#8217; come se scrivessi:

[cce_cpp]int useFunction2(int (*fun)(int), int val)  
{  
std::function<int(int)> tmp(fun);  
const std::function<int(int)> &cr(tmp);

cout << cr(val) << endl;  
}[/cce_cpp]

Di fatto, nell&#8217;esempio che proponi, non c&#8217;è grande differenza.

Può essere interessante osservare che, in entrambi i casi, lo standard garantisce quella che viene chiamata _small object optimization_: non c&#8217;è allocazione dinamica di memoria (il puntatore al _target_ viene memorizzato all&#8217;interno dell&#8217;oggetto tmp).

&#8212;

In una situazione di questo genere:

[cce_cpp]int main()  
{  
std::function<int(int)> f(square);

useFunction(f, 4);  
useFunction2(f, 3);  
}[/cce_cpp]

potrebbe esserci qualche differenza (in base alla dimensione dell&#8217;oggetto std::function).

Le varie librerie implementano std::function in maniera assai diversa, quindi è tutto da misurare.

In ogni caso non mi aspetterei differenze importanti: nel primo caso verranno copiati 32 byte o giù di lì, nell&#8217;altro 8.

&#8212;

[cce_cpp]int main()  
{  
std::array<char, 65536> arr;  
auto lambda = \[arr\](){};  
std::function<void()> f = lambda;

useFunction(f, 4);  
useFunction2(f, 3);  
}[/cce_cpp]

Qui la situazione è diversa: copiare f comporta uno sforzo sensibile.

&#8212;

In generale è una buona idea considerare un oggetto std::function come semplice da muovere (std::move) e potenzialmente oneroso da copiare.

Questo perchè std::function non è un semplice puntatore ma anche un meccanismo per gestire la memoria dell&#8217;oggetto chiamabile.

Sicuramente ogni volta che c&#8217;è bisogno di memorizzare una std::function, è meglio un passaggio per valore (in modo da poter effettuare una successiva std::move):

[cce_cpp]  
class object  
{  
public:  
using m_func = std::function<int(int)>;

object(m\_func f) : f\_(std::move(f)) {}

private:  
m\_func f\_;  
};

object o1( [](int x){ return x * x; } ); // qui basta move  
object o2(square); // qui bisogna copiare  
[/cce_cpp]

&#8212;

Se l&#8217;obiettivo è la massima efficienza, allora qualcosa del genere:

[cce_cpp]template<class Functor>  
void useFunction3(Functor &&f, int val)  
{  
cout << std::forward<Functor>(f)(val) << &#8216;\n&#8217;;  
}[/cce_cpp]

permette maggiori possibilità di ottimizzazione al compilatore.