---
id: 4682
title: 'Cat: a C++14 functional library'
date: 2015-04-29T16:20:36+02:00
author: Nicola Bonelli
layout: post
guid: http://www.italiancpp.org/?p=4682
permalink: /2015/04/29/cat-a-c14-functional-library/
categories:
  - Tecnologie
tags:
  - C++14
  - Functional Programming
  - Library
---
<img loading="lazy" class="aligncenter wp-image-4688" src="http://www.italiancpp.org/wp-content/uploads/2015/04/haskell-logo.png" alt="haskell-logo" width="163" height="115" />

<p style="text-align: justify;">
  The rise of functional programming has affected many programming languages, and C++ could not escape from it. The need of paradigms like partial <em>application</em> (via <em>currying</em>) and functional <em>composition</em> are now a reality also in C++, and the spread of libraries like <a title="FIT Library" href="https://github.com/pfultz2/Fit" target="_blank">FIT </a>and <a title="FLT Library" href="https://github.com/beark/ftl" target="_blank">FTL i</a>s an evidence.
</p>

<p style="text-align: justify;">
  <a href="http://cat.github.io/" target="_blank"><strong>Cat</strong> </a>is a <strong>C++14</strong> library, inspired by <em>Haskell. Cat </em>aims at pushing the functional programming approach in C++ to another level.
</p>

<p style="text-align: justify;">
  <strong>The added value of Cat is twofold.</strong> On one hand it works for filling the gap in the language with respect to functional programming. For this purpose, some <strong>utility functions</strong> and <strong>classes</strong> are provided (callable wrappers with partial application, sections, utilities for tuples, extended type traits, alternative forwarding functions, etc).
</p>

<p style="text-align: justify;">
  On the other hand <strong>Cat</strong> promotes the use of<strong> generic programming</strong> <strong>with type classes, </strong>inspired by <em>Category Theory</em>. A framework for building type-classes along with a dozen of them (<em>Functor</em>, <em>Applicative</em>, <em>Monoids</em>, <em>Monads</em>, <em>Read</em>, <em>Show</em>, to mention just a few) and the related instances dropped in the context of C++ are included in the library.
</p>

<h6 style="text-align: justify;">
  <strong>Cat</strong> is distributed under the <strong>MIT license</strong> and it’s available for download at the address <a href="http://cat.github.io/" target="_blank">https://cat.github.io</a>.
</h6>