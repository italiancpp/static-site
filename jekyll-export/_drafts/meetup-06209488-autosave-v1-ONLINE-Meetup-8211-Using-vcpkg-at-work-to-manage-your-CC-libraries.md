---
id: 9495
title: 'ONLINE Meetup &#8211; Using vcpkg at work to manage your C/C++ libraries'
date: 2020-05-14T11:01:50+02:00
author: marco
layout: revision
guid: https://www.italiancpp.org/2020/05/14/9488-autosave-v1/
permalink: /2020/05/14/9488-autosave-v1/
---
<center>
  <img loading="lazy" class="wp-image-9489 size-full aligncenter" src="https://www.italiancpp.org/wp-content/uploads/2020/05/meetupmo0620.png" alt="" width="1280" height="720" srcset="http://192.168.64.2/wordpress/wp-content/uploads/2020/05/meetupmo0620.png 1280w, http://192.168.64.2/wordpress/wp-content/uploads/2020/05/meetupmo0620-300x169.png 300w, http://192.168.64.2/wordpress/wp-content/uploads/2020/05/meetupmo0620-768x432.png 768w, http://192.168.64.2/wordpress/wp-content/uploads/2020/05/meetupmo0620-1024x576.png 1024w, http://192.168.64.2/wordpress/wp-content/uploads/2020/05/meetupmo0620-600x338.png 600w" sizes="(max-width: 1280px) 100vw, 1280px" />
</center>

<h4 style="text-align: center;">
  A very special meetup with the participation of some members of the Microsoft Visual C++ Team!
</h4>

<h4 style="text-align: center;">
</h4>

<h4 style="text-align: center;">
  <a href="https://teams.microsoft.com/l/meetup-join/19%3ameeting_NjdjZDAyYTMtMzdiOS00YzNmLWE0ZWUtZWQzYTlkZmEyMDI2%40thread.v2/0?context=%7b%22Tid%22%3a%22d2d2794a-61cc-4823-9690-8e288fd554cc%22%2c%22Oid%22%3a%22a5583cec-cf3a-4656-8066-925bdd3c7ce3%22%7d">[icon name=&#8221;video-camera&#8221; class=&#8221;&#8221; unprefixed_class=&#8221;&#8221;] Join the meetup!</a>
</h4>

<h4 style="text-align: center;">
  <span style="color: #2945a4;">Using vcpkg at work to manage your C/C++ libraries</span>
</h4>

<h5 style="text-align: center;">
  <span style="color: #2945a4;"><em>Augustin Popa &#8211; Program Manager, Microsoft C++ Team<br /> </em></span>
</h5>

<p style="text-align: center;">
  <img loading="lazy" class="aligncenter wp-image-9493 size-thumbnail" src="https://www.italiancpp.org/wp-content/uploads/2020/05/Augustin-photo-150x150.jpg" alt="" width="150" height="150" srcset="http://192.168.64.2/wordpress/wp-content/uploads/2020/05/Augustin-photo-150x150.jpg 150w, http://192.168.64.2/wordpress/wp-content/uploads/2020/05/Augustin-photo-300x300.jpg 300w, http://192.168.64.2/wordpress/wp-content/uploads/2020/05/Augustin-photo-50x50.jpg 50w, http://192.168.64.2/wordpress/wp-content/uploads/2020/05/Augustin-photo.jpg 400w" sizes="(max-width: 150px) 100vw, 150px" />
</p>

<p style="text-align: center;">
  [icon name=&#8221;commenting-o&#8221; class=&#8221;&#8221; unprefixed_class=&#8221;&#8221;] This meetup is hosted on Microsoft Teams so we can use voice and video!
</p>

<p style="text-align: center;">
  <a href="https://raw.githubusercontent.com/italiancpp/misc/master/Using%20vcpkg%20at%20work%20to%20manage%20your%20CC%2B%2B%20libraries.ics">[icon name=&#8221;calendar-plus-o&#8221; class=&#8221;&#8221; unprefixed_class=&#8221;&#8221;] Add this meetup to your calendar</a>
</p>

<p style="text-align: center;">
  <a href="https://teams.microsoft.com/l/meetup-join/19%3ameeting_NjdjZDAyYTMtMzdiOS00YzNmLWE0ZWUtZWQzYTlkZmEyMDI2%40thread.v2/0?context=%7b%22Tid%22%3a%22d2d2794a-61cc-4823-9690-8e288fd554cc%22%2c%22Oid%22%3a%22a5583cec-cf3a-4656-8066-925bdd3c7ce3%22%7d">Entra a questo link un po&#8217; prima delle 19</a>
</p>

<p style="text-align: justify;">
  <span style="color: #ffffff;"> </span>
</p>

<p style="text-align: justify;">
  <strong>7 PM</strong>
</p>

<p style="text-align: justify; padding-left: 30px;">
  <em>Welcome</em> &#8211; Marco Arena
</p>

<p style="text-align: justify;">
  <strong>7:05 PM</strong>
</p>

<p style="text-align: justify; padding-left: 30px;">
  Using vcpkg at work to manage your C/C++ libraries &#8211; Augustin Popa
</p>

<p style="font-weight: 400; text-align: justify;">
  Vcpkg appeared in 2016 as an open source C/C++ library manager with an expansive catalog of open source libraries that are tested together for compatibility. More recently, the team has been developing new features based on user feedback, including features relevant to enterprises with complex package management needs. This talk will give an overview of the tool and how to use it in a real-world scenario at your job, using new features we are planning on our roadmap: <a href="https://aka.ms/vcpkg/roadmap" data-saferedirecturl="https://www.google.com/url?q=https://aka.ms/vcpkg/roadmap&source=gmail&ust=1589530952270000&usg=AFQjCNFzkI0loWG-zNQwZjB92Uwj8Gdgeg">https://aka.ms/vcpkg/roadmap</a>.
</p>

<p style="font-weight: 400; text-align: justify;">
   Here is a preview of what we will go over:<br /> 1) How to cache library binaries for re-use across your development and CI machines
</p>

<p style="font-weight: 400; text-align: justify;">
  2) Using the vcpkg.json manifest file to declare all your dependencies easily
</p>

<p style="font-weight: 400; text-align: justify;">
  3) Using the new versioning support to lock yourself to specific versions of certain dependencies, or to maintain multiple versions of the same library on the same machine
</p>

<p style="font-weight: 400; text-align: justify;">
  4) How to install your own private libraries with vcpkg, alongside popular open source ones like Boost
</p>

<p style="font-weight: 400; text-align: justify;">
  <strong>8:30 PM </strong>
</p>

<p style="font-weight: 400; text-align: justify; padding-left: 30px;">
  <em>Q&A and Feedback</em>
</p>

**Resources**

  * Slides
  * Video

<p style="text-align: justify;">