---
id: 2809
title: C++11 in Azione (CDays14)
date: 2014-03-01T18:23:37+01:00
author: marco
layout: post
guid: http://www.italiancpp.org/?p=2809
permalink: /2014/03/01/c11-in-azione-cdays14/
categories: Articoli
---
<p style="text-align: center;">
  <a href="http://www.italiancpp.org/wp-content/uploads/2013/07/loveItalianCpp.jpg"><img loading="lazy" class=" wp-image-2802 aligncenter" alt="ILoveItalianCpp" src="http://www.italiancpp.org/wp-content/uploads/2013/07/loveItalianCpp.jpg" width="576" height="323" srcset="http://192.168.64.2/wordpress/wp-content/uploads/2013/07/loveItalianCpp.jpg 960w, http://192.168.64.2/wordpress/wp-content/uploads/2013/07/loveItalianCpp-300x168.jpg 300w, http://192.168.64.2/wordpress/wp-content/uploads/2013/07/loveItalianCpp-600x336.jpg 600w, http://192.168.64.2/wordpress/wp-content/uploads/2013/07/loveItalianCpp-250x140.jpg 250w" sizes="(max-width: 576px) 100vw, 576px" /></a>
</p>

<h4 style="text-align: center;">
  <a href="https://www.facebook.com/media/set/?set=oa.421537591314568" target="_blank">Guarda tutte le foto!</a>
</h4>

<p style="text-align: justify;">
  Lo scorso 26 Febbraio, ai <a href="http://communitydays.it/events/2014/" target="_blank">Community Days 2014</a>, abbiamo curato una traccia dedicata al C++. Il feedback è stato positivo e ci siamo divertiti molto. Come per l&#8217;<a href="http://www.italiancpp.org/2013/12/01/effective-code-transformations-in-cpp/" target="_blank">Agile Day</a>, scrivo un piccolo wrap-up del mio talk e della giornata in generale.
</p>

<p style="text-align: justify;">
  Ospite d&#8217;eccezione per la nostra track è stato <strong>Alessandro Contenti</strong> (Visual C++ Principal Development Manager @Microsoft Corp). La giornata inizia con tutti i nostri speaker sul palco della sala principale e <strong>Raffaele Rialdi </strong>(responsabile della nostra agenda e ambasciatore di <strong>++it</strong> per questo evento) presentando brevemente la nostra track e la community:
</p>

<p style="text-align: center;">
  <a href="http://www.italiancpp.org/wp-content/uploads/2014/03/italiancppOnStage.jpg"><img loading="lazy" class=" wp-image-2838 aligncenter" alt="italiancppOnStage" src="http://www.italiancpp.org/wp-content/uploads/2014/03/italiancppOnStage.jpg" width="384" height="384" srcset="http://192.168.64.2/wordpress/wp-content/uploads/2014/03/italiancppOnStage.jpg 640w, http://192.168.64.2/wordpress/wp-content/uploads/2014/03/italiancppOnStage-150x150.jpg 150w, http://192.168.64.2/wordpress/wp-content/uploads/2014/03/italiancppOnStage-300x300.jpg 300w, http://192.168.64.2/wordpress/wp-content/uploads/2014/03/italiancppOnStage-600x600.jpg 600w, http://192.168.64.2/wordpress/wp-content/uploads/2014/03/italiancppOnStage-250x250.jpg 250w" sizes="(max-width: 384px) 100vw, 384px" /></a>
</p>

<p style="text-align: justify;">
  Spostandoci in Sala 4 (la sala dedicata alla track C++), inizio io con la sessione sulle novità del linguaggio: &#8220;C++11 in Azione&#8221;.
</p>

<h3 style="text-align: justify;">
  C++11 in Azione
</h3>

<p style="text-align: justify;">
  Le slides sono sul <a href="http://www.communitydays.it/content/downloads/2014/cpp01_slides.zip" target="_blank">sito ufficiale dei CDays14</a>.
</p>

<p style="text-align: justify;">
  Il talk è un&#8217;introduzione ad alcune delle novità principali del C++11. Piuttosto che fare un mero elenco di features, ho preferito ripartire dalle meccaniche base del linguaggio e rivisitarle, mostrando come si &#8220;pensa direttamente in C++ oggi&#8221;. Ho diviso, quindi, la sessione in cinque macro-argomenti principali, di seguito descritti.
</p>

<h4 style="text-align: justify;">
  Inizializzazione
</h4>

<p style="text-align: justify;">
  Il C++11 offre nuovi strumenti che rendono possibile l&#8217;inizializzazione di variabili seguendo tre semplici regole. Gli ingredienti di queste regole sono, ovviamente: auto, initializer lists e uniform initialization.
</p>

  1. Per inizializzare un oggetto di tipo T (in ogni contesto &#8211; e.g. variabile locale, member-variable, &#8230;) usa la **{}-initialization**: <span style="color: #ffffff;"><br /> </span> [snippet]</p> 
    <pre>Developer dev{"Marco", 26};
auto dev = dev{"Marco", 26};</pre>
    
    <p style="text-align: justify;">
      [/snippet] Le due espressioni sono semanticamente differenti perché la seconda genera una copia (o move) da un temporaneo ma i compilatori sono bravi ad elidere questo passaggio rendendole, di fatto, equivalenti. Ho chiesto alla platea questa differenza e con grande piacere ho regalato un gadget ad un ragazzo preparato.<span style="color: #ffffff;">Le</span>
    </p>

  2. Le due eccezioni alla regola sopra, per le quali usare la **()-initialization**, sono: <span style="color: #ffffff;"> </span>  
    [snippet]</p> 
    <pre>auto x = int(2.5); // narrowing - comunque da evitare (è come un C-cast)
auto v = vector&lt;int&gt;(5, 1); // no init-list constructor</pre>
    
    [/snippet]<span style="color: #ffffff;"> </span></li> 
    
      * Per il tutto il resto usare **auto**: <span style="color: #ffffff;"><br /> </span> [snippet]</p> 
        <pre>auto file = GetFile("cdays14.txt");
auto sum = x+y;
const auto& elem = vec[0];</pre>
        
        [/snippet]</li> </ol> 
        
        #### Value semantics
        
        <p style="text-align: justify;">
          Quello che differenzia il C++ dagli altri linguaggi è la possibilità di<strong> controllare con precisione il lifetime degli oggetti</strong>. Normalmente gli oggetti sono passati <strong>per valore</strong> (per copia). Questo implica che un oggetto è diverso da un altro per il suo &#8220;contenuto&#8221; e non per un qualche genere di identificatore. Aggiungendo esplicitamente qualificatori è possibile adottare un&#8217;altra semantica (e.g. & per la <strong>reference semantics</strong>).
        </p>
        
        <p style="text-align: justify;">
          Obiettivo dei programmatori quanto dei compilatori è la <strong>minimizzazione</strong> di queste <strong>copie</strong>, con idiomi, ottimizzazioni, trucchi. Il C++11 rende finalmente disponibile ai programmatori la preziosa opportunità di avere a che fare con oggetti <strong>temporanei</strong>, ovvero &#8220;che stanno per essere distrutti&#8221; o che sono stati creati dal compilatore come passaggio intermedio di un&#8217;operazione più complessa.
        </p>
        
        <p style="text-align: justify;">
          Questa opportunità è data dalla <strong>move semantics</strong>, che rende possibile il controllo della costruzione di un oggetto a partire da un temporaneo. Si pensi, ad esempio, a quando un vector viene ritornato per valore da una funzione: anziché copiare, il compilatore preferisce &#8220;muovere&#8221; (se l&#8217;operatore è disponibile) il che è generalmente un&#8217;operazione economica e spesso exception-safe (e.g. swap di due puntatori). Nonostante i compilatori effettuino un&#8217;ottimizzazione della copia da decenni (e.g. copy-elision) questa non è garantita dallo standard.
        </p>
        
        <h4 style="text-align: justify;">
          Ownership e lifetime
        </h4>
        
        <p style="text-align: justify;">
          In C++ la <strong>distruzione</strong> degli oggetti è <strong>deterministica</strong>: il linguaggio garantisce che una variabile automatica (locale) venga distrutta appena esce dal suo scope di definizione. Questa garanzia forte dà vita all&#8217;idioma più importante del linguaggio: <strong>RAII (Resource Acquisition Is Initialization)</strong>. L&#8217;idea è di wrappare ogni risorsa (che in questo senso non vuol dire solo risorsa di sistema ma anche un oggetto del nostro dominio) di modo che essa venga acquisita quando il wrapper viene costruito e rilasciata quando esso viene distrutto:
        </p>
        
        <p style="text-align: justify;">
          [snippet]
        </p>
        
        <pre>vector&lt;string&gt; GetLines(const string& path)
{
   ifstream file{path}; // file.open();
   // ... get lines
} // file.close() automatico</pre>
        
        <p style="text-align: justify;">
          [/snippet]
        </p>
        
        <p style="text-align: justify;">
          Questa sintassi non è solo elegante e compatta ma anche <strong>exception-safe</strong>, grazie alla garanzia di distruzione di una variabile locale. Questo principio è alla base dell&#8217;ownership in C++. Da qui è possibile costruire policy di ownership in base alla semantica che si dà alle operazioni di copia (e ora anche di move).
        </p>
        
        <p style="text-align: justify;">
          Un wrapper non copiabile né movibile è detto <strong>guardia </strong>e modella l&#8217;ownership più semplice: quella di tipo <strong>scoped </strong>(una risorsa viene &#8220;posseduta&#8221; solo all&#8217;interno di uno scope, non può uscire). Un esempio tratto dalla libreria standard è quello del <strong>lock_guard</strong>.
        </p>
        
        <p style="text-align: justify;">
          Cosa fare se è necessario &#8220;passare&#8221; l&#8217;ownership da uno scope all&#8217;altro? Una soluzione ingenua potrebbe prevedere l&#8217;uso spudorato di allocazione dinamica e ownership &#8220;manuale&#8221;. Questo implicherebbe una serie di problemi discussi anche <a href="http://www.italiancpp.org/2013/08/23/puntatori-vivi-senza/" target="_blank">qui</a>. Ma come unire i benefici delle variabili automatiche (e della RAII) con l&#8217;allocazione dinamica? Utilizzati per decenni, il C++11 rende disponibili nuovi <strong>smart pointers </strong>non intrusivi, ovvero proxy a puntatori raw (&#8220;unmanaged&#8221;) che si prendono carico di gestirne la proprietà in base ad una ben precisa <strong>policy di ownership</strong>.
        </p>
        
        <p style="text-align: justify;">
          Gli <strong>shared_ptr</strong> modellano una policy di proprietà condivisa tramite ref-counting, mentre gli <strong>unique_ptr</strong> sfruttano la move semantics per modellare una policy di tipo <strong>unique</strong>. Da qui consegue che la move semantics non è solo un&#8217;opportunità di ottimizzazione e una rivoluzione stilistica ma anche lo strumento che permette di modellare una policy di unique ownership in modo elegante e compatto.
        </p>
        
        <p style="text-align: justify;">
          Le semplici regole dell&#8217;ownership in C++11 sono di seguito riportate:
        </p>
        
          1. <span style="line-height: 12px;">Proteggi le risorse con RAII;</span>
          2. Preferisci lifetime automatico e scoped ownership;
          3. Abilita copy/move, se necessarie;
          4. Se devi allocare dinamicamente ri-usa contenitori standard (e.g. smart pointers, containers, &#8230;) oppure scrivine uno confinando new e delete solo in costruttore/distruttore (o analoghi);
          5. Tendi alla <a href="http://flamingdangerzone.com/cxx11/2012/08/15/rule-of-zero.html" target="_blank">Rule of Zero</a>.
        
        <p style="text-align: justify;">
          La <strong>Rule of Zero</strong> è un&#8217;applicazione del <strong>Single Responsability Principle</strong> e afferma che se una classe ha a che fare <strong>esclusivamente</strong> con l&#8217;ownership allora <span style="text-decoration: underline;">può</span> personalizzare costruttore di copia e move, operatori di assegnazione/move e distruttore. Altrimenti non deve personalizzare alcuno di questi operatori (il compilatore crea per noi quelli di default, member-wise).
        </p>
        
        <p style="text-align: justify;">
          Due esempi: una classe <strong>File</strong> che abbia che fare con l&#8217;ownership di un FILE* (alla C) ha il permesso di personalizzare la semantica dei suoi operatori (e.g. disabilitando la copia, trasferendo l&#8217;ownership del FILE* tramite move e facendo una fclose in distruzione). Di contro, un repository di <strong>File</strong>, modellato solo con una member-variable di tipo <strong>vector<File></strong>, <strong>non</strong> deve personalizzare alcun operatore, perché il compilatore sintetizzerà una versione di default che andrà bene (chiamando gli operatori del <strong>vector<File></strong>).
        </p>
        
        <h4 style="text-align: justify;">
          Iterazione
        </h4>
        
        <p style="text-align: justify;">
          Iterazione in C++11 vuol dire, in molti casi, <strong>dimenticarsi degli iteratori</strong>. Per visitare tutti gli elementi di un <strong>range</strong> (e.g. una coppia begin-end) è possibile avvalersi del <strong>range-based for loop</strong>:
        </p>
        
        <p style="text-align: justify;">
          [snippet]
        </p>
        
        <pre>void Graph::Accept(IVisitor& visitor)
{
    for(auto& node : nodes) 	
    {
        visitor.Visit(node);
    }
}</pre>
        
        <p style="text-align: justify;">
          [/snippet]
        </p>
        
        <p style="text-align: justify;">
          Per cicli con <strong>logica</strong> è preferibile utilizzare un algoritmo, perché no, veicolato da una <strong>lambda</strong>:
        </p>
        
        <p style="text-align: justify;">
          [snippet]
        </p>
        
        <pre>auto evenCount = count_if(begin(nums), end(nums), [](int i) {
     return i%2 == 0;
});</pre>
        
        <p style="text-align: justify;">
          [/snippet]
        </p>
        
        <h4 style="text-align: justify;">
          Lambdas
        </h4>
        
        <p style="text-align: justify;">
          Una <strong>lambda expression</strong> è una shortcut sintattica per creare inline dei <strong>function objects</strong> (funtori o callable-objects) <strong>anonimi</strong> (senza nome e con tipo non specificato). Hanno due possibili declinazioni:
        </p>
        
        <strong style="line-height: 12px;">Funzioni anonime stateless</strong> <span style="line-height: 12px;">(castabili a function-pointers):</span> [snippet]
        
        <pre>auto it = find_if(begin(nums), end(nums), [](int i) { 
    return i%2 == 0; 
});</pre>
        
        [/snippet] <span style="color: #ffffff;"> </span>
        
        **Closures** (con accesso ad alcune/tutte le variabili nello scope): <span style="color: #ffffff;"> </span> <span style="color: #ffffff;"> </span> [snippet]
        
        <pre>auto sum = 0;
auto weight = 2;
for_each(begin(nums), end(nums), [&sum, weight](int i) { 
    sum += i * weight; 
});</pre>
        
        [/snippet]
        
        La **cattura** delle variabili nello scope può avvenire per copia o per riferimento.
        
        <p style="text-align: justify;">
          Per fare <strong>storage</strong> di una lambda (e per <strong>passarla</strong>) è possibile utilizzare <strong>auto</strong> (o un <strong>template</strong> se va messa in un class-member o va passata ad una funzione), che costituisce la scelta più performante. Spesso questo non è possibile (e.g. creare un vector di lambdas) e allora è possibile utilizzare un nuovo contenitore standard di funzioni e callable-objects: <strong>std::function</strong>. Questo è generalmente un po&#8217; meno performante perché &#8211; essendo un contenitore &#8220;polimorfo&#8221; &#8211; è spesso implementato utilizzando <strong>type-erasure</strong> (quindi allocazione dinamica) anche se i compilatori sono sempre nostri amici e bravi ottimizzatori.
        </p>
        
        <p style="text-align: justify;">
          Il talk si conclude con una sfumatura verso il <strong>C++14</strong>, con introduzione della initialized capture delle lambdas, chiamata in causa dal limite di non poter fare una cattura per move e quindi non poter trasferire l&#8217;ownership di una risorsa all&#8217;interno di una lambda.
        </p>
        
        <h4 style="text-align: justify;">
          Alcune domande
        </h4>
        
        <p style="text-align: justify;">
          Sono davvero contento della platea! Preparata ed interessata, ho fatto alcune domande live e sono sempre riuscito a ricevere risposte, regalando un gadget! Perdonatemi, mi ricordo solo due domande che mi avete fatto (se ne ricordate altre o volete farne altre scrivetele in un commento per favore):
        </p>
        
          1. Come inizializzo tramite auto un tipo numerico diverso da int?  
            **R**: con un literal (e.g. auto a = 10.0f &#8211; float; auto size = 100u; &#8211; unsigned).  
            <span style="color: #ffffff;"> </span>
          2. Gli shared_ptr sono thread-safe?  
            **R**: l&#8217;incremento del contatore è atomico, quindi sì. L&#8217;utilizzo della risorsa dev&#8217;essere però sincronizzato dal programmatore.  
            <span style="color: #ffffff;"> </span>
        
        <h3 style="text-align: justify;">
          Altre sessioni
        </h3>
        
        <p style="text-align: justify;">
          Dopo il mio talk è stata la volta di <strong>Guido Pederzini</strong> che ha parlato di <strong>Visual Studio 2013</strong> e alcuni tools indispensabili alla realizzazione di prodotti di alto livello. Debugger, profiler, analisi statica e warnings sono solo alcuni esempi.
        </p>
        
        <p style="text-align: justify;">
          Segue poi<strong> Raffaele Rialdi</strong> con una panoramica dettagliata sulle estensioni <strong>C++/CX</strong> per scrivere ed utilizzare efficacemente oggetti WinRT.
        </p>
        
        <p style="text-align: justify;">
          Dopo è salito sul palco <strong>Alessio Gogna</strong> che ha mostrato un po&#8217; di STL e boost con esempi live. Il suo compito, non banale, è riuscito comunque molto bene, trattando le tematiche con grande simpatia e competenza.
        </p>
        
        <p style="text-align: justify;">
          Finalmente è poi stato il turno di <strong>Ale Contenti</strong> e il suo divertentissimo talk su <strong>Cinder</strong> e <strong>OpenFrameworks</strong> ricco di esempi e demo che hanno fatto venir voglia di comprare un Surface e scrivere app!
        </p>
        
        <p style="text-align: justify;">
          Chiude la giornata la sessione di <strong>Raf</strong> e <strong>Ale</strong> sulla <strong>migrazione</strong> da legacy a moderno. Il talk riprende molti argomenti trattati in precedenza (dalla RAII agli smart pointers, dai warning all&#8217;SDL) e li porta in un contesto legacy, mostrandone i benefici in maniera evidente.
        </p>
        
        <p style="text-align: justify;">
          Hanno colorato l&#8217;intera giornata i nostri orginalissimi &#8220;Cheatsheet C++11&#8221;, ovvero dei pieghevoli in 6 facciate (un A4) con le novità più importanti del C++11 divise per categorie. Un grazie speciale a <strong>Franco Milicchio</strong> per la parte grafica. Oltre ai cheatsheet abbiamo regalato qualche gadget (magliette, mouse-pad e tazze)!
        </p>