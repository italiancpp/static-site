---
id: 6855
title: 'Boost : Errore in fase di compilazione'
date: 2016-10-14T00:02:56+02:00
author: Giovanni
layout: revision
guid: http://www.italiancpp.org/2016/10/14/6854-revision-v1/
permalink: /2016/10/14/6854-revision-v1/
---
Ciao a tutti ragazzi,  
è un pezzo che non mi faccio piu&#8217; vivo per cause di forze maggiori.. 🙁  
Stavo vendendo la libreria boost in questi giorni.. Mi sono scaricato l&#8217; ultima versione della libreria e l&#8217;ho decompressa in usr/lib/boost\_1\_62_0 .  
Io sto lavorando sotto linux, ed utilizzo netbeans come ide..  
Ho provato a compilare il seguente programmino che vorrei utilizzare come base di spunto :  
[Telnet Boost](http://lists.boost.org/boost-users/att-40895/telnet.cpp)

Il problema è che mi da un errore che non riesco a capire :  
[cce_cpp]cd &#8216;/home/ciclonite/NetBeansProjects/telnet&#8217;  
/usr/bin/make -f Makefile CONF=Debug  
&#8220;/usr/bin/make&#8221; -f nbproject/Makefile-Debug.mk QMAKE= SUBPROJECTS= .build-conf  
make[1]: Entering directory &#8216;/home/ciclonite/NetBeansProjects/telnet&#8217;  
&#8220;/usr/bin/make&#8221; -f nbproject/Makefile-Debug.mk dist/Debug/GNU-Linux/telnet  
make[2]: Entering directory &#8216;/home/ciclonite/NetBeansProjects/telnet&#8217;  
mkdir -p build/Debug/GNU-Linux  
rm -f &#8220;build/Debug/GNU-Linux/main.o.d&#8221;  
g++ -c -g -I/usr/local/boost\_1\_62_0 -std=c++11 -MMD -MP -MF &#8220;build/Debug/GNU-Linux/main.o.d&#8221; -o build/Debug/GNU-Linux/main.o main.cpp  
mkdir -p dist/Debug/GNU-Linux  
g++ -o dist/Debug/GNU-Linux/telnet build/Debug/GNU-Linux/main.o -L../../boost  
build/Debug/GNU-Linux/main.o: In function \`_\_static\_initialization\_and\_destruction_0(int, int)&#8217;:  
/usr/local/boost\_1\_62\_0/boost/system/error\_code.hpp:221: undefined reference to \`boost::system::generic_category()&#8217;  
/usr/local/boost\_1\_62\_0/boost/system/error\_code.hpp:222: undefined reference to \`boost::system::generic_category()&#8217;  
/usr/local/boost\_1\_62\_0/boost/system/error\_code.hpp:223: undefined reference to \`boost::system::system_category()&#8217;  
build/Debug/GNU-Linux/main.o: In function \`boost::system::error\_code::error\_code()&#8217;:  
/usr/local/boost\_1\_62\_0/boost/system/error\_code.hpp:322: undefined reference to \`boost::system::system_category()&#8217;  
build/Debug/GNU-Linux/main.o: In function \`boost::asio::error::get\_system\_category()&#8217;:  
/usr/local/boost\_1\_62\_0/boost/asio/error.hpp:230: undefined reference to \`boost::system::system\_category()&#8217;  
build/Debug/GNU-Linux/main.o: In function \`boost::asio::detail::posix\_thread::~posix\_thread()&#8217;:  
/usr/local/boost\_1\_62\_0/boost/asio/detail/impl/posix\_thread.ipp:35: undefined reference to \`pthread_detach&#8217;  
build/Debug/GNU-Linux/main.o: In function \`boost::asio::detail::posix_thread::join()&#8217;:  
/usr/local/boost\_1\_62\_0/boost/asio/detail/impl/posix\_thread.ipp:42: undefined reference to \`pthread_join&#8217;  
build/Debug/GNU-Linux/main.o: In function \`boost::asio::detail::posix\_thread::start\_thread(boost::asio::detail::posix\_thread::func\_base*)&#8217;:  
/usr/local/boost\_1\_62\_0/boost/asio/detail/impl/posix\_thread.ipp:50: undefined reference to \`pthread_create&#8217;  
build/Debug/GNU-Linux/main.o: In function \`boost::thread\_exception::thread\_exception(int, char const*)&#8217;:  
/usr/local/boost\_1\_62\_0/boost/thread/exceptions.hpp:51: undefined reference to \`boost::system::system\_category()&#8217;  
build/Debug/GNU-Linux/main.o: In function \`boost::detail::thread\_data\_base::thread\_data\_base()&#8217;:  
/usr/local/boost\_1\_62\_0/boost/thread/pthread/thread\_data.hpp:152: undefined reference to \`vtable for boost::detail::thread\_data\_base&#8217;  
build/Debug/GNU-Linux/main.o: In function \`boost::thread::start_thread()&#8217;:  
/usr/local/boost\_1\_62\_0/boost/thread/detail/thread.hpp:178: undefined reference to \`boost::thread::start\_thread_noexcept()&#8217;  
build/Debug/GNU-Linux/main.o: In function \`boost::thread::~thread()&#8217;:  
/usr/local/boost\_1\_62_0/boost/thread/detail/thread.hpp:253: undefined reference to \`boost::thread::detach()&#8217;  
build/Debug/GNU-Linux/main.o: In function \`boost::thread::get_id() const&#8217;:  
/usr/local/boost\_1\_62\_0/boost/thread/detail/thread.hpp:742: undefined reference to \`boost::thread::native\_handle()&#8217;  
build/Debug/GNU-Linux/main.o: In function \`boost::thread::join()&#8217;:  
/usr/local/boost\_1\_62\_0/boost/thread/detail/thread.hpp:768: undefined reference to \`boost::thread::join\_noexcept()&#8217;  
build/Debug/GNU-Linux/main.o: In function \`boost::detail::thread\_data<boost::\_bi::bind\_t<unsigned long, boost::\_mfi::mf0<unsigned long, boost::asio::io\_service>, boost::\_bi::list1<boost::\_bi::value<boost::asio::io\_service*> > > >::~thread_data()&#8217;:  
/usr/local/boost\_1\_62\_0/boost/thread/detail/thread.hpp:90: undefined reference to \`boost::detail::thread\_data\_base::~thread\_data_base()&#8217;  
build/Debug/GNU-Linux/main.o:(.rodata.\_ZTIN5boost6detail11thread\_dataINS\_3\_bi6bind\_tImNS\_4\_mfi3mf0ImNS\_4asio10io\_serviceEEENS2\_5list1INS2\_5valueIPS7\_EEEEEEEE[\_ZTIN5boost6detail11thread\_dataINS\_3\_bi6bind\_tImNS\_4\_mfi3mf0ImNS\_4asio10io\_serviceEEENS2\_5list1INS2\_5valueIPS7\_EEEEEEEE]+0x10): undefined reference to \`typeinfo for boost::detail::thread\_data\_base&#8217;  
collect2: error: ld returned 1 exit status  
nbproject/Makefile-Debug.mk:62: recipe for target &#8216;dist/Debug/GNU-Linux/telnet&#8217; failed  
make[2]: \*** [dist/Debug/GNU-Linux/telnet] Error 1  
make[2]: Leaving directory &#8216;/home/ciclonite/NetBeansProjects/telnet&#8217;  
nbproject/Makefile-Debug.mk:59: recipe for target &#8216;.build-conf&#8217; failed  
make[1]: \*** [.build-conf] Error 2  
make[1]: Leaving directory &#8216;/home/ciclonite/NetBeansProjects/telnet&#8217;  
nbproject/Makefile-impl.mk:39: recipe for target &#8216;.build-impl&#8217; failed  
make: \*** [.build-impl] Error 2  
[/cce_cpp]

Ho incluso la libreria boost in fase di compilazione ma niente da fare.. Qualcuno sa darmi qualche dritta?  
Grazie.