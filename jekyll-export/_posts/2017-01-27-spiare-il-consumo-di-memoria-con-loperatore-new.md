---
id: 7318
title: 'Spiare il consumo di memoria con l&#8217;operatore new'
date: 2017-01-27T19:42:17+01:00
author: stefano
layout: post
guid: http://www.italiancpp.org/?p=7318
permalink: /2017/01/27/spiare-il-consumo-di-memoria-con-loperatore-new/
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
categories:
  - Hands-on
---
 

_Un grazie speciale a_ **_Marco Alesiani_** _per le sue correzioni e suggerimenti._

_International reader? Read [the post in English](http://www.italiancpp.org/?p=7387)._

* * *

Quando diciamo “efficienza”, quasi sempre pensiamo “tempo”. Prima il codice fa il suo lavoro, più è efficiente.

E la memoria? Certo, oggi anche un portatile da quattro soldi arriva con “un secchio di RAM“… ma non basta mai. Il mio PC “sperpera” 1.4GB solo per restare acceso. Apro un browser, altri 300MB che se ne vanno<a href="javascript:void(0);" data-target="#nota1" data-toggle="collapse">*</a>.

<div id="nota1" class="collapse inlineNote" data-target="#nota1" data-toggle="collapse">
  &#8230;e chiediamo scusa per gli errori “Allowed memory size of &#8230; bytes exhausted “ o le pagine bianche che potreste vedere ogni tanto su ++It. Capite perchè il tema “memoria” ci sta a cuore.
</div>

Oltre il danno, la beffa: usare la memoria è anche una delle operazioni più lente sui sistemi attuali<a href="javascript:void(0);" data-target="#nota2" data-toggle="collapse">*</a>.

<div id="nota2" class="collapse inlineNote" data-target="#nota2" data-toggle="collapse">
  Daniele Maccioni: <a href="http://www.italiancpp.org/sessioni-cppday16/#cpp17">Data Oriented Design: alte performance in C++</a>
</div>

Ma non è semplice capire a quale riga del codice dare la colpa. Le new che scriviamo noi stessi? Qualche allocazione nascosta in una libreria? O è colpa di oggetti temporanei?

_Come trovare facilemente la parte di codice che usa più memoria?_

Questo articolo raccoglie qualche esperimento personale. Tutti gli errori sono &#8220;merito&#8221; dell&#8217;autore.

#### Usiamo un po&#8217; di memoria

Il programma-giocattolo di oggi non ha nulla di particolare, se non una gran varietà di allocazioni di memoria con operator new.

[snippet]  
/* Programma che alloca memoria a casaccio.  
Niente delete, questo non e&#8217; un articolo sui memory leak.*/  
#include <string>  
#include <memory>  
#include <boost/shared_ptr.hpp>  
#include <boost/make_shared.hpp>  
#include "UnaClasseDelProgramma.h"

//  
void h() {  
UnaClasseDelProgramma * t = new UnaClasseDelProgramma();  
}  
void g() { h(); }  
void f() { g(); }  
void CreaUnaClasseDelProgramma() { f(); }

//  
int main(int argc, char **argv) {  
int * numero = new int(89);  
std::string * test = new std::string("abc");  
//  
UnaClasseDelProgramma * oggetto = new UnaClasseDelProgramma();  
CreaUnaClasseDelProgramma();  
//  
boost::shared\_ptr<UnaClasseDelProgramma> smartPointer = boost::make\_shared<UnaClasseDelProgramma>();  
std::shared\_ptr<UnaClasseDelProgramma> stdSmartPointer = std::make\_shared<UnaClasseDelProgramma>();  
return 0;  
}  
[/snippet]

Compila, apri e… circa 42MB (misurati &#8220;alla buona&#8221; con <span class="inlineCode">/usr/bin/time -v</span>).

_Chi consuma tutta questa memoria?_

#### Il modo corretto: memory profiler

Il concetto è familiare: il profiler “classico” indica per quanto tempo gira ogni funzione. Il memory profiler invece indica dove, quando e quanta memoria usa il programma.  
Per esempio, ecco una parte di quello che Massif <a href="javascript:void(0);" data-target="#nota3" data-toggle="collapse">*</a> dice del nostro programma.

<div id="nota3" class="collapse inlineNote" data-target="#nota3" data-toggle="collapse">
  <a href="http://valgrind.org/docs/manual/ms-manual.html">http://valgrind.org/docs/manual/ms-manual.html</a><br /> Ma se lavorate in Windows: <a href="https://blogs.msdn.microsoft.com/vcblog/2015/10/21/memory-profiling-in-visual-c-2015/">https://blogs.msdn.microsoft.com/vcblog/2015/10/21/memory-profiling-in-visual-c-2015/</a>
</div>

Per iniziare, otteniamo (in ASCII art!) come l’uso della memoria cresce nel “tempo” &#8211; in realtà come cresce col numero di istruzioni eseguite:

<pre>MB
38.23^                                                           ::::::::::::#
     |                                                           :           #
     |                                                           :           #
     |                                                           :           #
     |                                                           :           #
     |                                               :::::::::::::           #
     |                                               :           :           #
     |                                               :           :           #
     |                                               :           :           #
     |                                               :           :           #
     |                                   @@@@@@@@@@@@:           :           #
     |                                   @           :           :           #
     |                                   @           :           :           #
     |                                   @           :           :           #
     |                                   @           :           :           #
     |                       ::::::::::::@           :           :           #
     |                       :           @           :           :           #
     |                       :           @           :           :           #
     |                       :           @           :           :           #
     |                       :           @           :           :           #
   0 +----------------------------------------------------------------------->Mi
     0                                                                   6.203
</pre>

Poi dei resoconti più dettagliati (le annotazioni &#8220;A&#8221;, &#8220;B&#8221; e &#8220;C&#8221; sono nostre):

<pre>--------------------------------------------------------------------------------
  n        time(i)         total(B)   useful-heap(B) extra-heap(B)    stacks(B)
--------------------------------------------------------------------------------
...
  9      4,313,116       30,080,056       30,072,844         7,212            0
99.98% (30,072,844B) (heap allocation functions) malloc/new/new[], --alloc-fns, etc.
-&gt;99.73% (30,000,000B) 0x407F68: __gnu_cxx::new_allocator&lt;char&gt;::allocate(unsigned long, void const*) (new_allocator.h:104)
| -&gt;99.73% (30,000,000B) 0x407EDA: std::allocator_traits&lt;std::allocator&lt;char&gt; &gt;::allocate(std::allocator&lt;char&gt;&, unsigned long) (alloc_traits.h:491)
|   -&gt;99.73% (30,000,000B) 0x407E80: std::_Vector_base&lt;char, std::allocator&lt;char&gt; &gt;::_M_allocate(unsigned long) (stl_vector.h:170)
|     -&gt;99.73% (30,000,000B) 0x407DFB: std::_Vector_base&lt;char, std::allocator&lt;char&gt; &gt;::_M_create_storage(unsigned long) (stl_vector.h:185)
|       -&gt;99.73% (30,000,000B) 0x407D27: std::_Vector_base&lt;char, std::allocator&lt;char&gt; &gt;::_Vector_base(unsigned long, std::allocator&lt;char&gt; const&) (stl_vector.h:136)
|         -&gt;99.73% (30,000,000B) 0x407CB6: std::vector&lt;char, std::allocator&lt;char&gt; &gt;::vector(unsigned long, std::allocator&lt;char&gt; const&) (stl_vector.h:278)
|           -&gt;99.73% (30,000,000B) 0x407C45: UnaClasseDelProgramma::UnaClasseDelProgramma() (UnaClasseDelProgramma.cpp:4)
|   A ===>   -&gt;33.24% (10,000,000B) 0x406611: main (main.cpp:20)
|             | 
|   B ===>    -&gt;33.24% (10,000,000B) 0x406541: h() (main.cpp:10)
|             | -&gt;33.24% (10,000,000B) 0x40656F: g() (main.cpp:12)
|             |   -&gt;33.24% (10,000,000B) 0x40657B: f() (main.cpp:13)
|             |     -&gt;33.24% (10,000,000B) 0x406587: CreaUnaClasseDelProgramma() (main.cpp:14)
|             |       -&gt;33.24% (10,000,000B) 0x40661A: main (main.cpp:21)
|             |         
|   C ===>    -&gt;33.24% (10,000,000B) 0x406A72: _ZN5boost11make_sharedI21UnaClasseDelProgrammaIEEENS_6detail15sp_if_not_arrayIT_E4typeEDpOT0_ (make_shared_object.hpp:254)
|               -&gt;33.24% (10,000,000B) 0x406626: main (main.cpp:23)
|                 
->00.24% (72,844B) in 1+ places, all below ms_print's threshold (01.00%)
</pre>

Vediamo subito che un terzo della memoria si spende alla riga 20 del main (A), dove c&#8217;è uno dei nostri new. Un altro 30% (B) lo alloca h() &#8211; che Massif mostra nello stack delle chiamate registrato al momento dell’allocazione. Seguendolo arriviamo alla chiamata a CreaUnaClasseDelProgramma() nel main. Massif cattura anche le allocazioni con shared pointer (C).

L&#8217;allocazione alla riga 24 non si vede perchè non è stata ancora eseguita e “intercettata” da Massif. Potrebbe comparire in uno snapshot successivo. Le altre allocazioni nel main sono &#8220;piccole&#8221; e aggregate nell&#8217;ultima riga.

Si vede subto che è il caso di dare un&#8217;occhiata al costruttore di UnaClasseDelProgramma. Che farà mai con uno std::vector che occupa il 99% della memoria?

Questo è già un ottimo aiuto, con poco sforzo. Volendo, Massif può fare di più. Può misurare la memoria usata &#8220;di nascosto&#8221; dal sistema per gestire l’heap (extra-heap – 7,212 byte nell’esempio), misurare lo stack&#8230;

#### Il metodo fai-da-te: override di operator new

In C++ si può sostituire l’operazione di creazione di un oggetto (new) con la propria.<a href="javascript:void(0);" data-target="#nota4" data-toggle="collapse">*</a>

<div id="nota4" class="collapse inlineNote" data-target="#nota4" data-toggle="collapse">
  <a href="http://en.cppreference.com/w/cpp/memory/new/operator_new">http://en.cppreference.com/w/cpp/memory/new/operator_new</a>
</div>

Quasi nessuno ha una buona ragione per farlo, ma noi si: <span style="text-decoration: line-through;">non sappiamo usare il profiler</span> intercettare le allocaioni nello heap.

Semplificando, basta definire la nostra versione di operator new (e dei suoi overload) in qualunque file del programma.

Se il memory profiler equivale al “time” profiler, questo trucco è paragonabile al classico snippet <span class="inlineCode">cout << tempoFine - tempoInizio;</span>. Non magnificamente dettagliato e accurato, ma semplice e comunque utile.

Bastano poche righe di codice per avere qualcosa di rozzo, ma utilizzabile. E’ meglio compilare con i simboli di debug. Il codice per scrivere lo stack trace è valido probabilmente solo su Linux<a href="javascript:void(0);" data-target="#nota5" data-toggle="collapse">*</a>.

<div id="nota5" class="collapse inlineNote">
  <!-- No collapse on click, altrimenti non si può cliccare per fare copia e incolla del codice. -->
  
  <br /> Non c&#8217;è niente di portabile a così basso livello.</p> 
  
  <p>
    Per chi lavora nel mondo Microsoft: <a href="https://msdn.microsoft.com/en-us/library/windows/desktop/bb204633%28v=vs.85%29.aspx">https://msdn.microsoft.com/en-us/library/windows/desktop/bb204633%28v=vs.85%29.aspx</a>.
  </p>
  
  <p>
    Sarebbe a dire:
  </p>
  
  <p>
    [snippet]<br /> #include <iostream><br /> //<br /> #include <Windows.h> // Cattura degli stack trace.<br /> #include <Dbghelp.h> // Lettura simboli di debug.
  </p>
  
  <p>
    //<br /> void StackTrace() {<br /> /* Cattura lo stack trace vero e proprio. */<br /> const ULONG doNotSkipAnyFrame = 0;<br /> const ULONG takeTenFrames = 10;<br /> const PULONG doNotHash = nullptr;<br /> PVOID stackTrace[takeTenFrames];<br /> const USHORT framesCaptured = CaptureStackBackTrace(<br /> doNotSkipAnyFrame,<br /> takeTenFrames,<br /> stackTrace,<br /> doNotHash<br /> );<br /> //<br /> /* Prepara la tabella dei simboli per tradurre da indirizzi a righe di codice. */<br /> const HANDLE thisProcess = GetCurrentProcess();<br /> SymInitialize(thisProcess, NULL, TRUE); // Linkare Dbghelp.lib<br /> //<br /> for (ULONG i = 0; i < framesCaptured; i++) {<br /> /*Estrae il nome della funzione. */<br /> const size_t nameStringSize = 256;<br /> SYMBOL_INFO * functionData = (SYMBOL_INFO*)malloc(sizeof(SYMBOL_INFO) + (nameStringSize + 1) * sizeof(char)); // +1 per il \0<br /> functionData->MaxNameLen = nameStringSize;<br /> functionData->SizeOfStruct = sizeof(SYMBOL_INFO);<br /> SymFromAddr(thisProcess, (DWORD64)(stackTrace[i]), 0, functionData);<br /> //<br /> /* Va a cercare il file corrispondende alla chiamata.*/<br /> DWORD displacementInLine;<br /> IMAGEHLP_LINE64 lineOfCode;<br /> lineOfCode.SizeOfStruct = sizeof(IMAGEHLP_LINE64);<br /> SymGetLineFromAddr64(thisProcess, (DWORD)(stackTrace[i]), &displacementInLine, &lineOfCode);<br /> //<br /> std::cout << functionData->Name << " at "<br /> << lineOfCode.FileName << ":" << lineOfCode.LineNumber << std::endl;<br /> }<br /> }<br /> [/snippet]
  </p>
</div>

.

[snippet]  
// Il nostro new deve poter allocare la memoria…  
#include <cstdio>  
#include <cstdlib>  
// &#8230;ma anche ispezionare lo stack e salvarlo in output.  
#include <execinfo.h>  
#include <unistd.h>  
#include <fstream>  
// Contiene std::bad_alloc &#8211; da lanciare in caso di errori.  
#include <new>  
//  
/* Apre (una sola volta) e restituisce il file stream per salvare  
gli stack. */  
std::ofstream& filePerRisultati() {  
static std::ofstream memoryProfile;  
static bool open = false; // Init on 1st use, classico.  
if (! open) {  
memoryProfile.open ("allocations.txt");  
open = true;  
}  
// Else, gestire gli errori, chiudere il file…  
// Omettiamo per semplicità.  
return memoryProfile;  
}  
//  
/* Questa funzione &#8220;fa la magia&#8221; e scrive nel file lo stack trace al momento della chiamata  
(compreso il suo stesso frame). */  
void segnaLoStackTrace(std::ofstream& memoryProfile) {  
// Registriamo 15 puntatori agli stack frame (bastano per il programma di prova).  
const int massimaDimensioneStack = 15;  
void *callStack[massimaDimensioneStack];  
size_t frameInUso = backtrace(callStack, massimaDimensioneStack);  
// A questo punto callStack è pieno di puntatori. Chiediamo i nomi delle  
// funzioni corrispondenti a ciascun frame.  
char ** nomiFunzioniMangled = backtrace_symbols(callStack, frameInUso);  
// Scrive tutte le stringhe con i nomi delle funzioni nello stream per il debug.  
for (int i = 0; i < frameInUso; ++i)  
memoryProfile << nomiFunzioniMangled[i] << std::endl;  
// A essere precisi, dovremmo rilasciare nomiFunzioniMangled con free…  
}  
//  
/\* Finalmente abbiamo tutti gli elementi per costruire il nostro operator new. \*/  
void* operator new(std::size_t sz) {  
// Allochiamo la memoria che serve al chiamante.  
void * memoriaRichiesta = std::malloc(sz);  
if (! memoriaRichiesta)  
throw std::bad_alloc();

// Raccontiamo al mondo intero le nostre allocaioni.  
std::ofstream& memoryProfile = filePerRisultati();  
memoryProfile << "Allocation, size = " << sz << " at " << static_cast<void*>(memoriaRichiesta) << std::endl;  
segnaLoStackTrace(memoryProfile);  
memoryProfile << "&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;" << std::endl; // Separatore dei poveri&#8230;  
return memoriaRichiesta;  
}  
[/snippet]

Aggiungiamo l&#8217;operator new &#8220;taroccato&#8221; al nostro programma di prova. Questo è un esempio del risultato &#8211; riuscite a capire quale riga di codice alloca la memoria?

<pre>Allocation, size = 40 at 0x18705b0
./overridenew(_Z14dumpStackTraceRSt14basic_ofstreamIcSt11char_traitsIcEE+0x3c) [0x40672c]
./overridenew(_Znwm+0xaf) [0x406879]
./overridenew(_ZN9__gnu_cxx13new_allocatorISt23_Sp_counted_ptr_inplaceI9SomeClassSaIS2_ELNS_12_Lock_policyE2EEE8allocateEmPKv+0x4a) [0x405d9e]
./overridenew(_ZNSt16allocator_traitsISaISt23_Sp_counted_ptr_inplaceI9SomeClassSaIS1_ELN9__gnu_cxx12_Lock_policyE2EEEE8allocateERS6_m+0x28) [0x405bef]
./overridenew(_ZSt18__allocate_guardedISaISt23_Sp_counted_ptr_inplaceI9SomeClassSaIS1_ELN9__gnu_cxx12_Lock_policyE2EEEESt15__allocated_ptrIT_ERS8_+0x21) [0x4059e2]
./overridenew(_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEC2I9SomeClassSaIS4_EJEEESt19_Sp_make_shared_tagPT_RKT0_DpOT1_+0x59) [0x4057e1]
./overridenew(_ZNSt12__shared_ptrI9SomeClassLN9__gnu_cxx12_Lock_policyE2EEC2ISaIS0_EJEEESt19_Sp_make_shared_tagRKT_DpOT0_+0x3c) [0x4056ae]
./overridenew(_ZNSt10shared_ptrI9SomeClassEC2ISaIS0_EJEEESt19_Sp_make_shared_tagRKT_DpOT0_+0x28) [0x40560e]
./overridenew(_ZSt15allocate_sharedI9SomeClassSaIS0_EIEESt10shared_ptrIT_ERKT0_DpOT1_+0x37) [0x405534]
./overridenew(_ZSt11make_sharedI9SomeClassJEESt10shared_ptrIT_EDpOT0_+0x3b) [0x405454]
./overridenew(main+0x9c) [0x4052e8]
/lib/x86_64-linux-gnu/libc.so.6(__libc_start_main+0xf0) [0x7f83fe991830]
./overridenew(_start+0x29) [0x405079]
-----------
Allocation, size = 10000000 at 0x7f83fc9c3010
./overridenew(_Z14dumpStackTraceRSt14basic_ofstreamIcSt11char_traitsIcEE+0x3c) [0x40672c]
./overridenew(_Znwm+0xaf) [0x406879]
./overridenew(_ZN9__gnu_cxx13new_allocatorIcE8allocateEmPKv+0x3c) [0x406538]
./overridenew(_ZNSt16allocator_traitsISaIcEE8allocateERS0_m+0x28) [0x4064aa]
./overridenew(_ZNSt12_Vector_baseIcSaIcEE11_M_allocateEm+0x2a) [0x406450]
./overridenew(_ZNSt12_Vector_baseIcSaIcEE17_M_create_storageEm+0x23) [0x4063cb]
./overridenew(_ZNSt12_Vector_baseIcSaIcEEC1EmRKS0_+0x3b) [0x4062f7]
./overridenew(_ZNSt6vectorIcSaIcEEC2EmRKS0_+0x2c) [0x406286]
./overridenew(_ZN9SomeClassC1Ev+0x3d) [0x406215]
./overridenew(_ZN9__gnu_cxx13new_allocatorI9SomeClassE9constructIS1_JEEEvPT_DpOT0_+0x36) [0x405e3a]
./overridenew(_ZNSt16allocator_traitsISaI9SomeClassEE9constructIS0_JEEEvRS1_PT_DpOT0_+0x23) [0x405d51]
./overridenew(_ZNSt23_Sp_counted_ptr_inplaceI9SomeClassSaIS0_ELN9__gnu_cxx12_Lock_policyE2EEC2IJEEES1_DpOT_+0x8c) [0x405b4a]
./overridenew(_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEC2I9SomeClassSaIS4_EJEEESt19_Sp_make_shared_tagPT_RKT0_DpOT1_+0xaf) [0x405837]
./overridenew(_ZNSt12__shared_ptrI9SomeClassLN9__gnu_cxx12_Lock_policyE2EEC2ISaIS0_EJEEESt19_Sp_make_shared_tagRKT_DpOT0_+0x3c) [0x4056ae]
./overridenew(_ZNSt10shared_ptrI9SomeClassEC2ISaIS0_EJEEESt19_Sp_make_shared_tagRKT_DpOT0_+0x28) [0x40560e]

...
</pre>

&#8230;io non ci riesco. Dove sta &#8220;main+0xa8&#8221; nel mio programma? Fortunatamente, nel &#8220;mondo gnu/Linux&#8221; ci sono strumenti per fare il de-mangling e trovare i punti del codice corrispondenti agli indirizzi. Possiamo usarli, per esempio, in un semplice <a href="javascript:void(0);" data-target="#nota6" data-toggle="collapse">script</a>.

<div id="nota6" class="collapse inlineNote">
  [snippet]<br /> #!/usr/bin/python<br /> #<br /> # C++filt fa il demangling dei nomi.<br /> #<br /> # addr2line converte i puntatori a codice (es. indirizzi di funzioni)<br /> # alla coppia file:riga col codice corrispondente (se ci sono i simboli di debug).<br /> #<br /> # Il codice python dovrebbe essere portabile, ma non le utility a riga di comando.<br /> #</p> 
  
  <p>
    import re<br /> import subprocess<br /> #
  </p>
  
  <p>
    # Apre un sottoprocesso e gli passa dei comandi per la shell, poi ritorna il risultato in una stringa.<br /> # Non molto efficiente, ma semplice.<br /> def run_shell(command):<br /> return subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0]<br /> #<br /> #<br /> if __name__ == &#8220;__main__&#8221;:<br /> total_size = 0;<br /> #<br /> # L&#8217;output ha 2 tipi di righe: quella con la dimensione dell&#8217;allocazione, e quella con uno stack frame.<br /> size_line = re.compile(&#8220;Allocation, size = (\d+) at (\d+)&#8221;) # Allocation, size = <bytes> at <punto dell&#8217;heap><br /> stack_line = re.compile(&#8220;.*\((.*)\+.*\) \[(.*)\]&#8221;) # <immondizia>(nome mangled) [<puntatore al codice>]<br /> #<br /> allocations_file = open(&#8220;allocations.txt&#8221;)<br /> for line in allocations_file:<br /> match_size = size_line.match(line)<br /> match_stack = stack_line.match(line)<br /> #<br /> # A scopo dimostrativo, accumulo il totale della memoria allocata.<br /> # Un esempio di quello che si puo&#8217; fare quando si controlla new!<br /> if (match_size):<br /> allocation_size = int(match_size.group(1))<br /> total_size += allocation_size<br /> print &#8220;Allocati &#8221; + str(allocation_size)<br /> #<br /> elif (match_stack):<br /> mangled_name = match_stack.group(1)<br /> line_address = match_stack.group(2)<br /> demangled_name = run_shell(["c++filt", "-n", mangled_name])<br /> line_number = run_shell([&#8220;addr2line", &#8220;-e&#8221;, &#8220;./overridenew&#8221;, line_address])<br /> #<br /> # La formattazione non e&#8217; molto professionale. Il -1 "gratuito" e&#8217; per togliere un newline.<br /> print&#8221;\t&#8221; + demangled_name[:-1] + &#8220;\n\t\t&#8221; + line_number,<br /> #<br /> # Rimette i separatori esattamente dov&#8217;erano.<br /> else:<br /> print line<br /> #<br /> print &#8220;\n total allocated size &#8221; + str(total_size)<br /> [/snippet]
  </p>
</div>

In alternativa, si può fare tutto a run time, con le utility di demangling dei compilatori. Per esempio [quella di gcc](https://gcc.gnu.org/onlinedocs/libstdc++/manual/ext_demangling.html). Personalmente preferisco tenere il codice di misurazione il più semplice possibile e &#8220;sbrigarmela&#8221; off-line. Con il mio script ottengo:

<pre>Allocati 40
    segnaLoStackTrace(std::basic_ofstream&lt;char, std::char_traits&lt;char&gt; &gt;&)
        /home/stefano/projects/overrideNew/InstrumentedNew.cpp:31
    operator new(unsigned long)
        /home/stefano/projects/overrideNew/InstrumentedNew.cpp:51
    __gnu_cxx::new_allocator&lt;std::_Sp_counted_ptr_inplace&lt;UnaClasseDelProgramma, std::allocator&lt;UnaClasseDelProgramma&gt;, (__gnu_cxx::_Lock_policy)2&gt; &gt;::allocate(unsigned long, void const*)
        /usr/include/c++/5/ext/new_allocator.h:105

   ... stack delle chiamate "interne" di shared_ptr...

    std::shared_ptr&lt;UnaClasseDelProgramma&gt; std::allocate_shared&lt;UnaClasseDelProgramma, std::allocator&lt;UnaClasseDelProgramma&gt;&gt;(std::allocator&lt;UnaClasseDelProgramma&gt; const&)
        /usr/include/c++/5/bits/shared_ptr.h:620
    std::shared_ptr&lt;UnaClasseDelProgramma&gt; std::make_shared&lt;UnaClasseDelProgramma&gt;()
        /usr/include/c++/5/bits/shared_ptr.h:636
    main
        /home/stefano/projects/overrideNew/main.cpp:25
    __libc_start_main
        ??:0
    _start
        ??:?
-----------

Allocati 10000000
    segnaLoStackTrace(std::basic_ofstream&lt;char, std::char_traits&lt;char&gt; &gt;&)
        /home/stefano/projects/overrideNew/InstrumentedNew.cpp:31
    operator new(unsigned long)
        /home/stefano/projects/overrideNew/InstrumentedNew.cpp:51
    __gnu_cxx::new_allocator&lt;char&gt;::allocate(unsigned long, void const*)
        /usr/include/c++/5/ext/new_allocator.h:105

         ... stack delle chiamate interne di vector...

    std::vector&lt;char, std::allocator&lt;char&gt; &gt;::vector(unsigned long, std::allocator&lt;char&gt; const&)
        /usr/include/c++/5/bits/stl_vector.h:279
    UnaClasseDelProgramma::UnaClasseDelProgramma()
        /home/stefano/projects/overrideNew/UnaClasseDelProgramma.cpp:4 (discriminator 2)
...
</pre>

La prima allocazione sono 40 byte chiesti da make_shared. 24 per UnaClasseDelProgramma (che contiene un vector come membro &#8211; sizeof(vector) è 24), i restanti dovrebbero essere il control block dello shared pointer. La seconda allocazione sono i 10MB del famigerato costruttore di UnaClasseDelProgramma.

Bisogna faticare un po&#8217; per decifrare gli stack, ma si riesce a capire che la riga misteriosa era <span class="inlineCode">std::shared_ptr<UnaClasseDelProgramma> stdSmartPointer = std::make_shared<UnaClasseDelProgramma>();</span> &#8211; dalle parti del return a main.cpp:25.

Compito per casa: quante allocazioni ci sarebbero con <span class="inlineCode">std::shared_ptr<UnaClasseDelProgramma> notSoSmartPointer(new UnaClasseDelProgramma());<br /> ?</span><a href="javascript:void(0);" data-target="#nota7" data-toggle="collapse">*</a>

<div id="nota7" class="collapse inlineNote" data-target="#nota7" data-toggle="collapse">
  Tre, e si usano 8 byte in più.<br /> In un test ho misurato:<br /> 24 byte per l&#8217;istanza di UnaClasseDelProgramma<br /> 10 MB per il contenuto del vector<br /> 24 byte per lo shared pointer.</p> 
  
  <p>
    Giudiacando dalle <a href="en.cppreference.com/w/cpp/memory/shared_ptr">implementation notes</a>, penso che la differenza sia nel contenuto del control_block dello shared pointer. </div> 
    
    <hr />
    
    <h4>
      Riassumendo&#8230;
    </h4>
    
    <p>
      I programmatori combattono da sempre con la memoria, vuoi perché è poca, vuoi perché è lenta. Come per tutti i colli di bottiglia, non ci si può fidare dell’istinto. Abbiamo visto che esistono strumenti appropriati (i memory profiler) per misurare il consumo di memoria. Abbiamo scoperto che, male che vada, esistono strumenti &#8220;casarecci&#8221; che possiamo costruirci da soli con il &#8220;classico hack da C++&#8221;, manipolando operator new.
    </p>
    
    <p>
      <em>Trovate il codice degli esempi &#8220;pronto da compilare&#8221; <a href="https://github.com/italiancpp/code/tree/master/spy-memory-with-new">sul repo GitHub di ++It<a>.</em></p>