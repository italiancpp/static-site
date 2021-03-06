---
id: 7740
title: Singleton revisited
date: 2017-03-19T16:52:43+01:00
author: Giuseppe
layout: post
guid: http://www.italiancpp.org/?p=7740
permalink: /2017/03/19/singleton-revisited-eng/
wp_sponsor_link_behaviour:
  - "0"
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
It happens quite often to deal with those annoying objects, used everywhere in your applications. This may be because of a poorly designed application but, sometime, it is simply an inevitable condition. With this in mind and considering that either a design refactoring to remove the global dependence is, sometimes, not affordable because of business needs or not convenient because it leads to more complex code, I&#8217;ll try to propose a non-canonical solution to the problem.

The obvious solution is the global scope, but we all know that it is also something which is better to avoid if you don&#8217;t want to run into sneaky problems, easy to cause and way more complicated to solve. We learned to be wary of the use of the global scope, as it is indeed a bad programming practice often causing long debugging sessions. But the problem still remains as it is at least useful (sometime necessary) to have variables valid within our whole program.

To bring to light the most relevant cons concerning the use of the global scope, we need to consider that its use involves the impossibility to count on data consistency. Furthermore, those variables can be modified at any time without us, as programmers, being really aware of it.

The global sharing can be a necessity, that&#8217;s why a standard pattern like Singleton exists. Ok, this pattern does something more, enforcing the uniqueness of a given type instances, however, at least as far as my own experience is concerned, the use of Singleton is often justified by the will of being able to easily refer to a unique object from any point effortlessly.

I&#8217;ll try to describe an alternative which, from my perspective, can work better.

## A typical case

A typical example is the implementation of a **logger **to be used application wide. If you don&#8217;t want to pass that object around, as a parameter in each and every function and constructor, you&#8217;ll probably implement that object as a Singleton.

At a first glance, it is a good idea, it must be unique and shared. This snippet below is a quite standard implementation:

[snippet]

<pre>class Logger{

  Logger() = default;

  public:

  static Logger& get(){
    static Logger instance;
    return instance;
  }

  void log(std::string s){
    std::cout &lt;&lt; s &lt;&lt; std::endl;
  }
};
[/snippet]
</pre>

Ok, this is quite nice, it achieves the result and also avoid troubles with resource acquisition and release, which you may have defining the instance as a private class member.

But the Singleton is a weak choice because it enforces the uniqueness of the object for the whole application life and this is not what we really want.

Let&#8217;s suppose that we need to log the activity of a really long function, and that we want to log to a different file every time the function is executed. (In the following examples I&#8217;m omitting some details for simplicity).

[snippet]

<pre>void g(){ 
   singleton::Logger::get().log("do something");
}

void f(){
  singleton::Logger::get().start();

  singleton::Logger::get().log("call g()");
  g();
  singleton::Logger::get().end();
}
[/snippet]</pre>

**start** and **end** methods are there to open and close a new file to log to. It works decently but it&#8217;s probably not the most beautiful code you&#8217;ve ever seen. Too many things can go wrong once that snippet become part of a much more complex application.

Let&#8217;s suppose that the functions you need to log the activity are many, for each of them you need to insert that calls to open and close the file to ensure other function are logged the right way. What if you forgot to close the file at the end of one of those functions? The next call would open a new log file leaving the old one open. And what if in the next call you don&#8217;t even open the new file? It will continue to write to the old one causing an unexpected behaviour.

As programmers our task is to write error-less code and, as it is a hard one, the best way is to design things so that they are not error prone.

In the example above, the first reference to the Singleton creates it but still does not really initialize it. At that point, even if we have the object, we can&#8217;t use it but after some preliminary action. Moreover, we&#8217;d like not to be able to refer to a resource once it is released, as it happens after the file is closed in the example. Ultimatly, the problem, in that example, is that the Singleton is doing more than what we really want it to do. The logger must not be unique and accessible during the whole application life but only for a part.

This Singleton&#8217;s limit has become clear to me when I was asked to put such a resource under test. In that case it was not a logger but a global component that, once under test, was to become local to the test. In practice I had a global (an exotic one implemented as a Singleton but still a global) to handle. That led me to try some variation on a theme, till I realized that I was searching for something like dynamic scope.

C, C++, Java, C# and many other languages, bind names to addresses using the static scope mechanism. That is, statically looking at the code, it is possible to decide which is the definition a variable name is referring.

[snippet]

<pre>int i;

void f(){
  int i=9;
  b();
  // here i refers to the local variable
}

void b(){
  // here i refers to the variable in global scope
   
}

void a(){
  // here i refers to the variable in global scope
  i= 3;
  b();
  f();
}</pre>

[/snippet]

Using dynamic binding, instead, the variable a symbol refers to depends on the current call stack. In the example above, the name _i _refers to the global or the local defined in _f()_ depending on the call stack that lead to the execution of _b()_.

If we had something like the dynamic scope, we could define a new object each and every time the need for a new resource arises, share it thereafter as it was a global untill the function which acquired the resource terminates and the resource itself is released

In the example below things are a little complicated to make it possible to define into dynamic scope any type even if it requires some parameter to be constructed:

[snippet]

<pre>template &lt;typename T&gt;
struct dynamic_scope {
  
  static std::stack&lt;T&gt;& instances(){
    static typename std::stack&lt;T&gt; m_instances;
    return m_instances;
  }

  static T& instance() {
    return instances().top();
  }
                     
  template &lt;typename... Args&gt;
  dynamic_scope(Args... args){
    instances().push(T(args...));
  }

  ~dynamic_scope(){
    instances().pop();
  }
};

void f2(){
  dynamic_scope&lt;Console&gt; the_console (Console(40L, 3L));
  dynamic_scope&lt;Console&gt;::instance() &lt;&lt; "log from f2"; 
}; 

void f1(){  
  dynamic_scope&lt;Console&gt;::instance() &lt;&lt; "log from f1"; 
  f2(); 
}; 

int _tmain(int argc, _TCHAR* argv[]) { 
  dynamic_scope&lt;Console&gt; the_console (40L, 3L);
  dynamic_scope&lt;Console&gt;::instance() &lt;&lt; "log something"; 
  f1(); 
  
  return 0; 
}
[/snippet]</pre>

What I did here is to enforce the uniqueness of a stack of instances. Every instance override previous one once it is defined and untill it is released.

In the example, main function and f1 log their data in a different Console then the more specific one that f2 uses. Moreover every call to f2 causes the acquisition of a new Console object. Every each time a new dynamic\_scope object is created, it is pushed on the static stack. The instance in use is always the one on top of the stack, it will be popped  and destroyed once the corresponding dynamic\_scope object comes out of its scope.  At that point, the last overridden instance become the current in use again. The name given to the variable that manages the dynamic scope is not important.

A little programming puzzle can help clarify even more. What&#8217;s the output of the following program?

[compiler]

<pre>#include &lt;iostream&gt;
#include &lt;stack&gt;

template &lt;typename T&gt;
struct dynamic_scope {
  
  static std::stack&lt;T&gt;& instances(){
    static typename std::stack&lt;T&gt; m_instances;
    return m_instances;
  }

  static T& instance() {
    return instances().top();
  }
                     
  template &lt;typename... Args&gt;
  dynamic_scope(Args... args){
    instances().push(T(args...));
  }

  ~dynamic_scope(){
    instances().pop();
  }
};

void f2(){
  std::cout &lt;&lt; ++dynamic_scope&lt;long&gt;::instance() &lt;&lt; std::endl;
};

void f1(){
  dynamic_scope&lt;long&gt; the_long(10);
  std::cout &lt;&lt; ++dynamic_scope&lt;long&gt;::instance() &lt;&lt; std::endl;

  f2();
};

int main(int argc, char* argv[]){
  dynamic_scope&lt;long&gt; the_long(80);

  std::cout &lt;&lt; dynamic_scope&lt;long&gt;::instance()  &lt;&lt; std::endl;
  f1();
  std::cout &lt;&lt; dynamic_scope&lt;long&gt;::instance() &lt;&lt; std::endl;
  
  return 0;
}
</pre>

[/compiler]

Here I defined a unique instance of and integer on the dynamic scope. When the program enter main function, one instance of the integer is created on the dynamic scope. Its value is 80 and that is the value sent to stdout.

When the program enter f1(), the integer instance defined in its scope override the previous one becoming the current in use. Its initial value is 10 which is increased by one, so 11, and is sent to the stdout before f2() get called.

In the scope of f2() function, the integer is accessible and it refers to the last instance defined in f1() therefore a new increment makes its value be 12 which is the value printed in f2().

When calls are popped from the call stack and the execution return within main function, the integer instance defined in main() itself is restored as the current in use so that the last instruction still print 80.

## Limits

I don&#8217;t think this is really a dynamic scope implemented in C++ because we override variables based on their type not their names. We always refer to the unique active instance of type so we will never refer to two different objects of the same type at the same time if they are managed by the &#8220;dynamic scope&#8221;.

Hope this notes of mine will be useful for anyone.

## Write down your idea is a great thing

And it is even better if someone review you.

After I wrote this and asked for a review, the reviewer has pointed out that someone had similar proposal. Bob Smidth, the author of this article published on [ACCU-2085](https://accu.org/index.php/journals/2085), had similar motivations to arrange a design and write his proposal.

Aside the use of the stack that adds features and try to highlight how the little forgotten  dynamic scope concept can be a good solution for a common problem, the approach I proposed here is very close to the one published by Bob. To me, the difference, is in a different compromise between invasiveness and use friendliness.

The tool I wrote here is not the most terse (I mean it is too verbose) but, on the plus side, it makes clear that we are accessing variables that do not follow common scope rules.

I mentioned the invasiveness because I think that the pattern proposed by Bob has the requirement to wrap every interface you want to be a Singleton (or with some modification in the dynamic scope) into a mono_nvi wrapper. This simplify the usage for sure but at the cost of boilerplate.

Anyway the two solutions are really similar, to switch to something really similar to the one in  [ACCU-2085](https://accu.org/index.php/journals/2085), you need just to write that small piece of boilerplate that define a temporary used to access the instance on top of the global stack. This code try to synthesize both approaches:

[compiler]

<pre>#include &lt;iostream&gt;
#include &lt;stack&gt;

struct ilogger {
  virtual void info(const char* msg) const = 0;
};

struct logger : public ilogger {
  std::string m_name;
  
  logger(std::string logger_name) : m_name(logger_name){}
  
  virtual void info(const char* msg) const {
    std::cout &lt;&lt; m_name.c_str() &lt;&lt; ":  " &lt;&lt;  msg &lt;&lt; std::endl;
  }
};

template &lt;typename T&gt;
struct dynamic_scope {

  static std::stack&lt;T&gt;& instances() {
    static typename std::stack&lt;T&gt; m_instances;
    return m_instances;
  }

  static T& instance() {
    return instances().top();
  }

  template &lt;typename... Args&gt;
  dynamic_scope(Args... args) {
    instances().push(T(args...));
  }

  ~dynamic_scope() {
    instances().pop();
  }


  struct entry {
    T& m_obj;
    
    entry() : m_obj(dynamic_scope::instance()) { }

    void info(const char* msg) const {
      m_obj.info(msg);
    }
  };

};



void f2() {
  dynamic_scope&lt;logger&gt;::entry the_logger;

  dynamic_scope&lt;logger&gt;::instance().info("from f2");
  the_logger.info("from f2 (simpler?");
}

void f1() {
  dynamic_scope&lt;logger&gt; dynamic_logger("f1");
  dynamic_scope&lt;logger&gt;::entry the_logger;
  
  dynamic_scope&lt;logger&gt;::instance().info("call f2");
  the_logger.info("call f2 (simpler?)");

  f2();
};

int main(int argc, char* argv[]) {
  dynamic_scope&lt;logger&gt; dynamic_logger("main");
  dynamic_scope&lt;logger&gt;::entry the_logger;

  dynamic_scope&lt;logger&gt;::instance().info("call f1");
  the_logger.info("call f1 (simpler?)");

  f1();
  dynamic_scope&lt;logger&gt;::instance().info("returned from f1");
  the_logger.info("returned from f1 (simpler?)");

  return 0;
}
</pre>

[/compiler]

## What if you are in a multithread world?

I don&#8217;t want to try a solution for Singleton in the multithread realm, but want just to warn about the dangers of such a solution applied in a multithreaded application.

For sure, even if the underlying object is thread safe, you need to synchronize the access to the shared global stack. You can do it using the inner structure **entry: **integrate a **std::lock_guard**  into it and be careful to not keep the temporary alive too long. But is a shared dynamic scope really meaningful? To me it is a stretch.