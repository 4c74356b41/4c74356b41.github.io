---
id: 916
title: WDS перестает работать после добавления boot-image на pxe в SCCM 2012 R2
date: 2014-06-28T23:54:41+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post916
permalink: /post916
categories:
  - SCCM
tags:
  - Configuration Manager
  - Copypaste
---
И Вы находите ошибку приблизительно следующего содержания в Event log'е
  
Faulting application name: svchost.exe_WDSServer, version: 6.3.9600.16384, time stamp: 0x5215dfe3
  
Faulting module name: MSVCR100.dll, version: 10.0.40219.1, time stamp: 0x4d5f034a
  
Exception code: 0xc0000005
  
Fault offset: 0x000000000005f61a
  
Faulting process id: 0xae4
  
Faulting application start time: 0x01cec5d767184634
  
Faulting application path: C:Windowssystem32svchost.exe
  
Faulting module path: C:Program FilesMicrosoft Configuration Managerbinx64MSVCR100.dll

Бежим ставить http://support.microsoft.com/kb/2905002 или [Rollup 2](http://support.microsoft.com/kb/2970177).

&nbsp;