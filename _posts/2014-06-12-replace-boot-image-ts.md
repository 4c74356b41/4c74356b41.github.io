---
id: 455
title: Как обновить boot image во всех Task Sequnce'ах
date: 2014-06-12T22:03:47+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post455
permalink: /post455
categories:
  - SCCM
tags:
  - Configuration Manager
  - Copypaste
  - Guide
---
В случае если у Вас много TS'ов и лень обновлять руками.

```
Get-WmiObject -ComputerName localhost -Namespace rootsmssite_cas 
   -Class SMS_TaskSequencePackage 
   -Filter "BootImageID = 'ID_старого_образа'"
   | ForEach-Object { $_.BootImageID = 'ID_нового_образа'; $_.Put()}
```
