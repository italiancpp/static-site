---
id: 2088
title: compiler-beta
date: 2013-11-17T14:47:52+01:00
author: marco
layout: page
guid: http://www.italiancpp.org/?page_id=2088
---
[raw]  
<!-- JQuery, the web Boost! -->

  
  


<!-- Our style for this page after the jquery one (to override the search box z-index). -->

<link rel="stylesheet" href="http://www.italiancpp.org/wp-includes/css/jquery-ui.css" />

<link rel="stylesheet" type="text/css" href="http://www.italiancpp.org/wp-includes/css/onlineCompiler.css" media="screen" />

<!-- Overlay to open the search box. Here for JQuery to take over.-->

  


<div id="searchBox" class="searchGizmos" style="visibility: hidden; overflow: auto; z-index: 1000;" title="Ricerca">
</div>

<!--Editor box - here for ACE to take over.-->

<div id="editor" onmouseup="editorResize();comboClick();" onmouseover="editorResize()">
</div>

<!-- onmouseover ensure that the editor gets resized if the user drags the mouse outside it after  grabbing the resize handle. If something goes wrong he moves the mouse back in and the editor repairs itself. -->

  
  
<!-- Command bar of this IDE. -->

  
  
<input class="toolbarButton" type="button" value="Compila ed esegui" id="compileButton"      
       onclick="compilationCommandSequence();" />  
<input class="toolbarButton" type="button" value="Opzioni" id="optionsButton"        
        onclick="optionButtonScipt();" />  
<input class="toolbarButton" type="button" value="Help" id="helpButton"         
        onclick="jQuery('#instructions').toggle('blind' );jQuery('#instructions').goTo();" /> 

<p class="pageOneLiners">
  <!-- Copyright string -->
  
  <br /> Powered by <a href="http://coliru.stacked-crooked.com">Coliru</a> online compiler
</p>

</BR>  


<DIV  id="compilerToolbar">
  <br /> 
  
  <DIV>
    <br /> <!-- Every option must have a option- prefix in the ID. -->
    
    <br /> <LABEL for="compileCommand">Opzioni compilazione:</LABEL><br /> <span id="compileCommand"><br /> <select id="option-compiler"><option value="g++-4.8" selected>g++ (4.8)</option><option value="clang++">clang (3.4)</option><!-- TODO other compilers? -->
    
    <br /> </span><br /> <span><input input type="text" id="option-compilerOptions" value="-std=c++1y -pthread" /></input></span><br /> </DIV><br /> 
    
    <DIV>
      <br /> <LABEL for="option-fontSize">Dimensione carattere:</LABEL><br /> <INPUT id = "option-fontSize" onchange="setFontSize()"></INPUT><br /> <SCRIPT type="text/javascript"><br />
jQuery( &#8220;#option-fontSize&#8221; ).spinner({ max: 25, min: 8,<br />
                                      change: BETA_setFontSize(), spin: BETA_setFontSize()}).val(14);<br />
</SCRIPT><br />
    </DIV>
    
    <br /> 
    
    <TABLE>
      <br /> 
      
      <TR>
        <br /> 
        
        <TD>
          <br /> <input class="toolbarButton" type="button" value="Stampa il comando di compilazione" onclick="showCommandLine();" /><br />
        </TD>
        
        <br />
      </TR>
      
      <br /> 
      
      <TR>
        <br /> 
        
        <TD>
          <br /> Ricerca su</p> 
          
          <p>
            </TD><br /> </TR><br /> 
            
            <TR>
              <br /> 
              
              <TD>
                <br /> <input class="toolbarButton" type="button" value="Salva" onclick="itc_saveOptions();" /><br /> <input class="toolbarButton" type="button" value="Carica" onclick="itc_loadOptions();" /><br /> <input class="toolbarButton" type="button" value="Default" onclick="itc_restoreDefaultOptions();" /><br />
              </TD>
              
              <br /> 
              
              <TD>
                <br /> <input class="toolbarButton" type="button" value="Chiudi e torna all'editor"        onclick="jQuery('#compilerToolbar').toggle('blind');jQuery('#editor').goTo();" /><br />
              </TD>
              
              <br />
            </TR>
            
            <br /> </TABLE><br /> </DIV><br />
          </p>
          
          <p>
            <!-- Box to print the output (compiler messages or execution results). -->
            
            <br /> </BR><br /> 
            
            <DIV id="outbox">
            </DIV>
          </p>
          
          <p>
            <input class="toolbarButton" type="button" value="Torna all'editor" onclick="jQuery('#editor').goTo();" /><br /> <input class="toolbarButton" type="button" value="Altri strumenti" 
       onclick="jQuery('#advancedTools').toggle('blind');" />
          </p>
          
          <p>
            <DIV id="advancedTools">
              <br /> <input class="toolbarButton" type="button" value="Archivia il codice su coliru" 
       onclick="itc_archiveCodeOnColiru()" /><br /> </BR><span id = "archiveCodeLinks"></span><br />
            </DIV>
          </p>
          
          <p>
          </p>
          
          <p>
            <DIV id="instructions">
              <br /> 
              
              <H4>
                Compilatore online
              </H4>
              
              <br /> 
              
              <UL>
                <br /> 
                
                <LI>
                  Modifica il codice nell&#8217;editor;
                </LI>
                <br /> 
                
                <LI>
                  Se desideri, modifica le opzioni del compilatore;
                </LI>
                <br /> 
                
                <LI>
                  Clicca <strong>Compila ed esegui</strong> o usa la shortcut <strong>CTRL+F7</strong> per compilare ed eseguire il codice!
                </LI>
                <br /> 
                
                <LI>
                  Infine guarda i risultati nel box in basso.
                </LI>
                <br /> 
                
                <LI>
                  Documentazione rapida? Non c&#8217;è problema! Con <strong>CTRL+click</strong> cerchi la parola cliccata direttamente su <a href="http://cppreference.com">cppreference.com</a>!
                </LI>
                <br /> 
                
                <LI>
                  Puoi salvare le opzioni (in un cookie &#8211; attento alle impostazioni del browser) con il pulsante &#8220;Salva&#8221; e recuperare il tuo set-up con il pulsante &#8220;Carica&#8221;. Se hai fatto pasticci, torna alle impostazioni-base con &#8220;Default&#8221;.
                </LI>
                <br />
              </UL></p> 
              
              <p>
                <H5>
                  Maggiori informazioni:
                </H5>
                
                <br /> 
                
                <UL>
                  <br /> 
                  
                  <LI>
                    realizzato con <a href="http://ace.c9.io/">Ace</a> Editor e <a href="http://www.coliru.stacked-crooked.com">Coliru</a> Online Compiler!
                  </LI>
                  <br /> 
                  
                  <LI>
                    <EM>Il tuo codice non viene salvato in modo permanente</EM>, ma solo in un cookie se esci dalla pagina.
                  </LI>
                  <br /> 
                  
                  <LI>
                    Attento, Coliru limita execution time e lunghezza dell&#8217;output!
                  </LI>
                  <br />
                </UL>
              </p>
              
              <p>
                <H5>
                  Vogliamo sentire il tuo parere!
                </H5>
                
                <br /> <A href="mailto:info@italiancpp.org?SUBJECT=[Compiler]"><br /> Scrivici segnalando problemi, idee e tutto quello che ti viene in mente!<br /> </A><br /> <BR /><br /> <input class="toolbarButton" type="button" value="Chiudi e torna all'editor"          
            onclick="jQuery('#instructions').toggle('blind');jQuery('#editor').goTo();" /><br /> </DIV>
              </p>
              
              <p>
                <br /> <!-- End of page.-->
              </p>
              
              <p>
                <!-- Initialization of the GUI machinery.-->
                
                <br /> <br />
              </p>
              
              <p>
                <br /> [/raw]
              </p>