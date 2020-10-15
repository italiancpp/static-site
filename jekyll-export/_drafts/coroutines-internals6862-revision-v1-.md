---
id: 6868
date: 2016-10-16T21:00:03+02:00
author: Marco Alesiani
layout: revision
guid: http://www.italiancpp.org/2016/10/16/6862-revision-v1/
permalink: /2016/10/16/6862-revision-v1/
---
## What are coroutines and why should I care?

Coroutines are control flow structures that generalize subroutines by providing multiple exit/entry points. A normal subroutine usually has a starting point and one or more exit (return) points. A coroutine provides the ability to seamlessly enter/exit a subroutine&#8217;s control flow at different spots therefore allowing for greater code expressiveness and [nonpreemptive multitasking](https://en.wikipedia.org/wiki/Cooperative_multitasking).

Thoughtful use of coroutines can lead to cleaner and more maintainable code in a variety of situations. As a motivating example let&#8217;s take for instance the following pseudocode

<pre>function start_accepting() {

  socket.async_accept_connection(accept_handler);

}

function accept_handler() {

  socket.async_read(read_handler);
  start_accepting();

}

function read_handler(data) {

  request = parse_data(data);

  switch(request) {

    case SEND_DATA: {

      data_to_send = prepare_data_for(request);

      socket.async_write(data_to_send, write_handler);

    } break;

  };

}

function write_handler() {

  ... // continue execution

}</pre>

Asynchronous programming is often the preferred way of accomplishing potentially blocking operations without stalling the thread on blocking calls. In the pseudocode above we&#8217;re assuming (and omitting for clarity&#8217;s sake) that all operations are queued and handled by an event loop manager (a common and powerful idiom in asynchronous applications programming, cfr. [boost::asio](http://www.boost.org/doc/libs/)).

Coroutines allow modeling the same behavior with more readable code

<pre>function start_accepting() {

  while(true) {

    socket.async_accept_connection(serve_request);

    start_coroutine(serve_request);

  }

}

coroutine serve_request() {

  socket.async_read(data, yield);

  request = parse_data(data);

  switch(request) {

    case SEND_DATA: {

      data_to_send = prepare_data_for(request);

      socket.async_write(data_to_send, yield);

      ... // Continue execution

    } break;

  };

}</pre>

&nbsp;

The code in _serve_request()_ uses a sequential-looking paradigm

> Coroutines let you create a structure that mirrors the actual program logic. Asynchronous operations don’t split functions, because there are no handlers to define what should happen when an asynchronous operation completes. Instead of having handlers call each other, the program can use a sequential structure.
> 
> ([boost.asio-coroutines](http://theboostcpplibraries.com/boost.asio-coroutines))
> 
> &nbsp;

## Coroutines internals

It is important to understand the role of coroutines in providing a collaborative non-preemptive multitasking: spawning a coroutine **does not spawn a new thread** of execution but coroutines _waive_ execution by <a href="https://en.wikipedia.org/wiki/Yield_(multithreading)" target="_blank">yielding</a> to callers (_asymmetric coroutines_) or to other coroutines (_symmetric coroutines_) explicitly.

Implementing basic support for asymmetric stack-based coroutines can be a rewarding experience in terms of understanding the relationship between coroutines and the way these program flow constructs interact with callers and the underlying memory. Most of the code that will be presented is a pruned-down version of the coroutine implementation by Oliver Kowalke (cfr. <a href="http://www.boost.org/doc/libs/" target="_blank">boost::coroutine2</a>) available with the boost libraries.