---
id: 5708
title: Running Jenkins on Azure WebApp (Linux)
date: 2017-02-11T21:08:30+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post5708
permalink: /post5708
categories:
  - Azure
tags:
  - Azure
  - jenkins
  - WebApp
---
So, turns out its super easy.

  1. Create a `WebApp on Linux (Preview)` and specify Jenkins container:[<img class="alignnone size-medium wp-image-5709" src="http://4c74356b41.com/wp-content/uploads/2017/02/unnamed-file-1-300x156.png" alt="webappjenkins" width="300" height="156" srcset="http://4c74356b41.com/wp-content/uploads/2017/02/unnamed-file-1-300x156.png 300w, http://4c74356b41.com/wp-content/uploads/2017/02/unnamed-file-1-768x400.png 768w, http://4c74356b41.com/wp-content/uploads/2017/02/unnamed-file-1.png 879w" sizes="(max-width: 300px) 100vw, 300px" />](http://4c74356b41.com/wp-content/uploads/2017/02/unnamed-file-1.png)
  2. Create a `Port` AppSetting and set it to 8080.
  3. Enjoy 😉