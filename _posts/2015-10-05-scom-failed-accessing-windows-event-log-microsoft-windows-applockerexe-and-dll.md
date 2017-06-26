---
id: 3221
title: SCOM Failed Accessing Windows Event Log Microsoft-Windows-AppLocker/EXE and DLL
date: 2015-10-05T17:19:11+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post3221
permalink: /post3221
categories:
  - Virtualization and Cloud
tags:
  - Copypaste
  - Operations Management Suite
  - Operations Manager
---
Привет друзья! 

Вот с такой забавной проблемой столкнулся после интеграции SCOM'а и OMS. На всех гипер-в хостах агент в состоянии Warning, в HealthViewer'е видно такую ошибку "Failed Accessing Windows Event Log Microsoft-Windows-AppLocker/EXE and DLL". 

Чтож, сделаем оверрайд: Authoring >> Rules >> фильтруем по &uml;Collect Applocker Events". И применяем оверрайд на необходимую группу или часть группы. 

[Вдохновение](https://jurelab.wordpress.com/2015/07/23/scom-monitor-failed-accessing-windows-event-log-microsoft-windows-applockerexe-and-dll/).