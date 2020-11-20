---
id: 5411
title: Primi passi con Boost.Python
date: 2015-12-02T19:12:00+01:00
author: stefano
layout: post
guid: http://www.italiancpp.org/?p=5411
permalink: /2015/12/02/primi-passi-con-boost-python/
categories: Articoli
---
### &#8220;Finalmente un linguaggio più moderno e funzionale&#8221;

Chi fra noi non vorrebbe programmare in un linguaggio multiparadigma, altamente espressivo, in piena evoluzione e con una vastissima libreria standard? Stiamo parlando, ovviamente, di&#8230; Python.

Ci sono casi in cui il nostro solito campione (C++11), non è la scelta migliore. Per un prototipo da sviluppare in fretta, uno script “usa e getta”, il server di un&#8217;applicazione web, del codice di ricerca&#8230; la complessità del C++ è più un peso che un vantaggio.

Come possiamo continuare a sfruttare l&#8217;efficienza del C++ o riutilizzare codice già esistente senza passare per cavernicoli fuori moda?

L&#8217;interprete Python può caricare moduli scritti in C, compilati in librerie dinamiche. Boost.Python ci aiuta, enormemente, a prepararli. Uniamo la potenza di Boost e C++ alla semplicità di Python.

Attenzione: anche se tutti gli esempi compilano, girano e passano i test questa non è la guida definiva su Boost.Python. Il codice è illustrativo, riflette solo la nostra (scarsa) esperienza con Boost.Python. Non esitate a segnalarci errori.

#### Un problema di velocità

Vediamo un caso (non troppo) pratico. Ci sono numeri uguali alla somma dei loro divisori (6 = 3 + 2 + 1; [numeri perfetti](https://it.wikipedia.org/wiki/Numero_perfetto)). Il reparto marketing ha fiutato l&#8217;affare, ma è fondamentale calcolarne il più possibile prima della concorrenza. La velocità di sviluppo di Python è l&#8217;arma vincente, dopo 5 minuti rilasciamo Pefect 1.0<span style="font-family: Liberation Serif,serif;">®:</span>

[snippet]

<pre>def trova_divisori(numero):
	divisori = []
	for i in range(1, numero):
		if numero % i == 0:
			divisori.append(i)
	return divisori


def perfetto(numero):
	divisori = trova_divisori(numero)
	return numero == sum(divisori)


def trova_perfetti(quanti_ne_vuoi):
	trovati = 0
	numero_da_provare = 1
	while (trovati &lt; quanti_ne_vuoi):
		if perfetto(numero_da_provare):
			print numero_da_provare
			trovati += 1
		numero_da_provare += 1


if __name__ == "__main__":
	trova_perfetti(4) # Cercatene di più a vostro rischio e pericolo.
                        # L'attesa sarà lunga...
</pre>

[/snippet]

Questo codice non è perfettamente “pythonico” (<https://www.python.org/dev/peps/pep-0008/>), ma è stato veramente creato, testato e debuggato nel tempo che di solito spendiamo a leggere un&#8217;errore di compilazione<a class="sdfootnoteanc" href="#sdfootnote1sym" name="sdfootnote1anc"><sup>1</sup></a>.

Peccato che il tempo di esecuzione sia paragonabile: 6,5 secondi sulla mia macchina di prova (che non è la vostra, non è il server di produzione, non è il PC del Python-boy che a lui gira tutto in un picosecondo&#8230; è un esempio!).

Da bravi ingegneri cerchiamo il collo di bottiglia con il profiler:

[snippet]

<pre>import cProfile

... stesso codice di prima ...

if __name__ == "__main__":
	cProfile.run('trova_perfetti(4)')
</pre>

[/snippet]

Ed ecco il risultato:

<pre>ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    7.420    7.420 &lt;string&gt;:1()
     8128    0.709    0.000    7.326    0.001 purePython-profiler.py:15(perfetto)
        1    0.095    0.095    7.420    7.420 purePython-profiler.py:19(trova_perfetti)
     8128    5.190    0.001    6.523    0.001 purePython-profiler.py:8(trova_divisori)
    66318    0.819    0.000    0.819    0.000 {method 'append' of 'list' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
     8128    0.514    0.000    0.514    0.000 {range}
     8128    0.094    0.000    0.094    0.000 {sum}
</pre>

trova_divisori &#8220;ruba&#8221; quasi tutti i 6,5 secondi!

#### boost::python

Nessuno nega che si possa scrivere codice efficiente in Python (Java, VisualQualcosa, il linguaggio funzionale di questa settimana&#8230;), ma ottimizzare l&#8217;algoritmo di trova_divisori è fuori discussione: vogliamo mostrare Boost.Python, non fare una lezione di Algebra.

Per prima cosa, ci procuriamo Boost.Python. Su una macchina Linux è semplice quanto usare:

<pre>sudo apt-get install libboost-all-dev</pre>

Potreste dover installare anche i package “dev” di Python. Non è difficile trovare su internet istruzioni per tutte le piattaforme, ma installare (e compilare) può essere la parte più difficile. Non scoraggiatevi.

Questo è il codice C++:  
[snippet]

<pre>#include "boost/python.hpp"  // (1)

boost::python::list trovaDivisori(uint64_t numero) // (2)
{
	boost::python::list divisori;
	for (uint64_t i = 1; i &lt; numero; ++i)  // (3)
		if (numero % i == 0)
			divisori.append(i);
	return divisori;
}

BOOST_PYTHON_MODULE(divisori)
{
    using namespace boost::python;
    def("trova_divisori", trovaDivisori);  // (4)
}
</pre>

[/snippet]

  1. Includiamo Boost.Python. Deve essere incluso prima di ogni altro eventuale header per evitare warning alla compilazione.
  2. La funzione equivalente a quella che vogliamo sostituire in Python. Manteniamo la stessa segnatura (prende un intero, ritorna una lista) dell&#8217;originale in Python per rendere la sostituzione &#8220;trasparente&#8221;.
  3. Anche l&#8217;algoritmo è esattamente lo stesso. Cambia solo la sintassi, e neanche di molto. In questo caso tutta la differenza la fa, probabilmente, il runtime C++.
  4. Dichiariamo la funzione nel modulo python con “def” (&#8230;come in Python).

La guida ([http://www.boost.org/doc/libs/1\_59\_0/libs/python/doc/](http://www.boost.org/doc/libs/1_59_0/libs/python/doc/)) spiega molto chiaramente tutti dettagli.

La compilazione, purtroppo, non è esattamente elementare, dovrete probabilmente adattarla caso per caso. Vediamo l&#8217;esempio un passo alla volta (si tratta di una sola riga di comando, naturalmente):

<pre>g++ divisori.cpp			    compilo un file C++, qui tutto normale
 -o divisori.so  			    nome del file: Python esige sia lo stesso del modulo
-I /usr/include/python2.7/	            includo gli header di Python (ho Boost già nel path)
-l python2.7 -lboost_python -lboost_system  includo Python, Boost
-shared -fPIC -Wl,-export-dynamic           chiedo di creare una libreria dinamica
</pre>

stackoverflow.com farà il resto. Notare che, per “par condicio”, non stiamo usando le opzioni di ottimizzazione di g++.

Una volta che la nostra libreria è nel path di sistema (altrimenti Python non la trova) possiamo includerla nel codice Python:  
[snippet]

<pre>from divisori import trova_divisori

def perfetto(numero):
	divisori = trova_divisori(int(numero)) # Adesso chiama quella in C++
	return numero == sum(divisori)

… stesso codice di prima …
</pre>

[/snippet]

Tempo di esecuzione: poco meno di un secondo. Siamo testimoni del classico “l&#8217;80% del tempo si spreca nel 20% del codice”. Lo stesso algoritmo è 6 volte più veloce, ma l&#8217;unica parte su cui abbiamo perso tempo con la programmazione a basso livello (dopotutto, è ancora C++98!) è una sola funzione. Per tutto il resto possiamo ancora approfittare della praticità di Python.

#### Qualche possibilità in più

Boost.Python non si limita a convertire i tipi primitivi e a incapsulare le liste di Python in un adapter C++. Ecco una selezione dei casi “tipici” per chi programma nel “C con classi”:  
[snippet]

<pre>class RiutilizzabileInPython 
{
	public:
		RiutilizzabileInPython() {};
		RiutilizzabileInPython(int x, const std::string& y) {};
		int variabileIstanza;
		static void metodoStatico() {};
		void metodo() {}
};

BOOST_PYTHON_MODULE(oop)
{
    using namespace boost::python;
    class_&lt;RiutilizzabileInPython&gt;("implementata_in_CPP")	//(1)
	.def(init&lt;int, std::string&gt;())				//(2)
	.def_readwrite("variabile_istanza", &RiutilizzabileInPython::variabileIstanza)//(3)
	.def("metodo_statico", &RiutilizzabileInPython::metodoStatico).staticmethod("metodo_statico") //(4)
	.def("metodo", &RiutilizzabileInPython::metodo)		// (5)
    ;
}
</pre>

[/snippet]

  1. >Apriamo la dichiarazione della classe, passando la stringa con il nome Python.
  2. Traduzione del costruttore in Python (&#8230;init, ricorda niente?).
  3. La “tradizione” Python non disdegna le variabili di oggetto pubbliche. Eccone una.
  4. Solo una ripetizione del nome Python per esporre un metodo statico.
  5. Il classico, semplice metodo d&#8217;istanza.

Una volta compilato (&#8230;tra il dire e il fare&#8230;) possiamo usare la classe C++ in Python:

[snippet]

<pre>from oop import implementata_in_CPP

x = implementata_in_CPP()
y = implementata_in_CPP(3, "ciao")
x.variabil_istanza = 23
implementata_in_CPP.metodo_statico()
x.metodo()
</pre>

[/snippet]

Boost si preoccupa di convertire parametri, tipi di ritorno eccetera. Ci sono opzioni per l&#8217;“esportazione” diretta delle classi della STL (e se non ci sono è possibile definirle) e per le policy dei tipi ritornati (per reference, per copia&#8230;). Le possibilità sono moltissime, affidatevi alla guida ufficiale.

Quando il gioco si fa duro, Boost continua a giocare. Un assaggio:

[snippet]

<pre>class Problems
{
	public:
		void stampa() {
			std::cout &lt;&lt; "cout continua a funzionare" &lt;&lt; std::endl;
		}

		void eccezione() {
			throw std::runtime_error("Oh, no!!!");
		}

		void coreDump() {
			int * nullPointer = 0;
			*nullPointer = 24;
		}
};

BOOST_PYTHON_MODULE(oop)
{
    using namespace boost::python;

     class_&lt;Problems&gt;("Problems")
	.def("stampa", &Problems::stampa)
	.def("eccezione", &Problems::eccezione)
	.def("coreDump", &Problems::coreDump)
    ;
}

</pre>

[/snippet]

Il “test-driver” in Python, con un esempio di output:  
[snippet]

<pre>from oop import Problems
p = Problems()
p.stampa()
try:
	p.eccezione()
except RuntimeError as e:
	print "Il codice C++ non ha funzionato: " + str(e);
p.coreDump()

</pre>

[/snippet]

<pre>cout continua a funzionare				(1)
Il codice C++ non ha funzionato: Oh, no!!!	        (2)
Segmentation fault (core dumped)			(3)
</pre>

  1. Debuggare a colpi di std::cout non è una buona pratica&#8230; ma funziona!
  2. Le eccezioni sono perfettamente “inoltrate” al runtime Python.
  3. &#8230;pensavate di salvarvi, eh?

#### Multithreading

Boost.Python non è l&#8217;unica arma per affrontare problemi che richiedono efficienza. Il codice multi thread è un modo comune di aumentare le prestazioni, tanto per per trovare divisori che per minare Bitcoin o craccare password. Ecco una classe C++ che sta per saltare in un thread Python.

[snippet]

<pre>class JobTrovaDivisori {

	public:
		JobTrovaDivisori(uint64_t numero, uint64_t begin, uint64_t end) :
			numero(numero), begin(begin), end(end) {}
		
		boost::python::list trovaDivisori()
		{
			std::cout &lt;&lt; "Start" &lt;&lt; std::endl;

			boost::python::list divisori;
			for (uint64_t i = begin; i &lt; end; ++i)
				 if (numero % i == 0)
					divisori.append(i);

			std::cout &lt;&lt; "end" &lt;&lt; std::endl;
			return divisori;
		}

	private:
		uint64_t numero;
		uint64_t begin;
 		uint64_t end;
};

BOOST_PYTHON_MODULE(fattorizzare)
{
    using namespace boost::python;
    class_&lt;JobTrovaDivisori&gt;("JobTrovaDivisori", init&lt;uint64_t, uint64_t, uint64_t&gt;())
	.def("trova_divisori", &JobTrovaDivisori::trovaDivisori)
    ;
}
</pre>

[/snippet]

L&#8217;oggetto “JobTrovaDivisori” controlla se i numeri tra “begin” e “end” sono divisori di “numero”. Parallelizziamo il problema di trovare tutti i divisori in più “job” usando ogni oggetto su un intervallo diverso. Non ci sono dati condivisi, non abbiamo alcun problema di concorrenza. Questa è l&#8217;unica nota positiva di questa soluzione, ma ancora una volta tralasciamo la matematica (e l&#8217;ingegneria del software).

La chiamata in Python:  
[snippet]

<pre>from threading import Thread
from fattorizzare import JobTrovaDivisori

class Job():							# (1)
	def __init__(self, numero, begin, end):
		self.cppJob = JobTrovaDivisori(numero, begin, end)
		self.divisori = []
	
	def __call__(self):
		self.divisori = self.cppJob.trova_divisori()

		
def trova_divisori_parallelo(numero):			# (2)
	limite = numero / 2

	job1 = Job(numero, 1, limite)
	job2 = Job(numero, limite, numero)

	t1 = Thread(None, job1)
	t2 = Thread(None, job2)
	
	t1.start()
	t2.start()
	t1.join()
	t2.join()

	return [job1.divisori, job2.divisori]


if __name__ == "__main__":
	print trova_divisori_parallelo(223339244);	#(3)
</pre>

[/snippet]

  1. Incapsuliamo il Job C++ per “non complicarci la vita” cercando di esportare un callable C++.
  2. Questo metodo crea 2 job, esegue il “fork e join” (o, come dicono oggi, &#8220;map e reduce&#8221;), poi stampa il risultato.
  3. Fattorizziamo un numero qualunque.

Ecco l&#8217;output: ricordate le stampe di “Start” e “end” nella classe C++? Dopo circa 8 secondi e mezzo il calcolo termina, senza nessun parallelismo:

<pre>Start
end
Start
end
[[1L, 2L, 4L, 53L, 106L, 212L, 1053487L, 2106974L, 4213948L, 55834811L], [111669622L]]
</pre>

Non è un caso. Gli oggetti Python sono protetti dal Global Interpreter Lock (GIL). Spetta al programmatore di ciascun thread rilasciarlo per dare il “via libera” agli altri thread. L&#8217;accortezza è di non chiamare codice puramente Python quando non si possiede il lock.

Come al solito in C++ controlliamo le risorse col metodo RAII. L&#8217;idioma per il GIL è ([https://wiki.python.org/moin/boost.python/HowTo#Multithreading\_Support\_for\_my\_function](https://wiki.python.org/moin/boost.python/HowTo#Multithreading_Support_for_my_function)):  
[snippet]

<pre>class ScopedGILRelease
{
public:
    inline ScopedGILRelease(){
        m_thread_state = PyEval_SaveThread();
    }
    inline ~ScopedGILRelease()    
        PyEval_RestoreThread(m_thread_state);
        m_thread_state = NULL;
    }
private:
    PyThreadState * m_thread_state;
};
</pre>

[/snippet]

Rilasciamo il lock nella classe C++:  
[snippet]

<pre>boost::python::list trovaDivisori() {
	ScopedGILRelease noGil = ScopedGILRelease(); // (1)
	std::cout &lt;&lt; "Start" &lt;&lt; std::endl;
		
	boost::python::list divisori;
	for (uint64_t i = begin; i &lt; end; ++i)
		 if (numero % i == 0)  
			divisori.append(i); // (2) Possibile Core Dump!
	std::cout &lt;&lt; "end" &lt;&lt; std::endl;
	return divisori;
}
</pre>

[/snippet]

  1. Quando questa variabile esce dallo scope, il lock è ri-acquisito, come se fosse uno smart pointer &#8220;al contrario&#8221;.
  2. Qui è dove prenderemo il core dump. Ma solo in produzione.

Ricordate la clausola _“l&#8217;accortezza è di non chiamare codice puramente Python quando non si possiede il lock”_? La riga (2) potrebbe fare esattamente quello. Provate a far crescere la lista a dismisura (ad esempio, elimiate la “if (numero&#8230;” e salvate tutti i numeri nella lista). Credo che, probabilmente (affidatevi alle guide ufficiali per conoscere la vera risposta!) l&#8217;interprete Python deve allocare una lista più grossa, ma non avendo il lock qualcosa si corrompe.

Racchiudiamo la sezione parallelizzabile in uno scope a parte, salvando i numeri in una variabile non condivisa con Python:  
[snippet]

<pre>boost::python::list trovaDivisori() {
	std::cout &lt;&lt; "Start" &lt;&lt; std::endl;
	std::vector&lt;uint64_t&gt; divisoriTemp;
	{
	ScopedGILRelease noGil = ScopedGILRelease();
		for (uint64_t i = begin; i &lt; end; ++i)
			 if (numero % i == 0) 
				divisoriTemp.push_back(i);
		std::cout &lt;&lt; "end" &lt;&lt; std::endl;
	} // noGil esce dallo scope. Riprendiamo il lock.
	boost::python::list divisori;
	BOOST_FOREACH(uint64_t n, divisoriTemp) {
		divisori.append(n);
	}
	return divisori;
}
</pre>

[/snippet]  
Dopo 6 secondi e mezzo (-2 rispetto alla versione “accidentalmente sequenziale”) otteniamo l&#8217;interleaving previsto (Start Start &#8211; end end). Quei 2 secondi possiamo spenderli per pensare a una soluzione meno rimediata.

Questo conclude l&#8217;introduzione a Boost.Python. Ora conosciamo un modo per “incastrare” moduli C++ nelle applicazioni Python, sia per riutilizzarli che per ragioni di efficienza. Boost.Python connette i due mondi senza sacrificare la semplicità di Python e senza limitare le possibilità in C++, pur se è necessaria qualche accortezza. _Soprattutto, d&#8217;ora in avanti avremo l&#8217;ultima parola nel classico flame “Python vs C++” su tutti i forum del mondo!_

<div id="sdfootnote1">
  <p class="sdfootnote">
    <a class="sdfootnotesym" href="#sdfootnote1anc" name="sdfootnote1sym">1</a>E&#8217; vero che si fa prima a fare un programma in Python che aggiustare un solo bug C++.
  </p>
  
  <p>
    Fate la prova. Pronti, partenza, via:
  </p>
  
  <pre>
/usr/include/c++/4.8/bits/stl_map.h:646:7: note: no known conversion for argument 1 from 
‘int’ to ‘std::map<int, std::map<std::basic_string<char>, std::basic_string&lt
;char> > >::iterator {aka std::_Rb_tree_iterator<std::pair<const int, std::map<std::basic_string<char>, std::basic_string<char> > > >}’


<p class="sdfootnote">
  /usr/include/c++/4.8/bits/stl_map.h:670:9: note: template<class 
  _InputIterator> void std::map<_Key, _Tp, _Compare, _Alloc>::insert(_InputIterator, 
  _InputIterator) [with _InputIterator = _InputIterator; _Key = int; _Tp = 
  std::map<std::basic_string<char>, std::basic_string<char> >; _Compare 
  = std::less<int>; _Alloc = std::allocator<std::pair<const int, std::map<std::basic_string<char>, std::basic_string<char> > > >
  </pre>
  </div>