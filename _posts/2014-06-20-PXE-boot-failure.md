---
id: 618
title: 'PXE Boot зависает после получения IP адреса от DHCP'
date: 2014-06-20T14:59:43+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post618
permalink: /post618
categories:
  - SCCM
tags:
  - Configuration Manager
  - Copypaste
  - Guide
---
Если у вас не включен мультикаст в настройках PXE:
  
Administration >> Site >> Site Settings >> Site Systems >> Distribution Point - проверяем выключен ли мультикаст.
  
Software Library >> >> Operating System >> Operating System Images >> образ который используется для PXE >> убрана ли галочка "allow this package to be transferred via multicast".

Если это так, проверяем DHCP scope и убираем опцию 43. Voila!