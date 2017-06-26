---
id: 1399
title: Ошибка Live Migration виртуальной машины с виртуальным HBA
date: 2014-07-16T11:23:54+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post1399
permalink: /post1399
categories:
  - Virtualization and Cloud
tags:
  - Copypaste
  - Guide
  - Virtual Machine Manager
---
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/npiverror.jpg" rel="attachment wp-att-5157"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/npiverror-300x209.jpg" alt="npiverror" width="300" height="209" /></a>

Суть ошибки в том что соответствующий WMI класс (MSFC_FibrePortNPIVAttributes в rootwmi) на хосте отсутствует. Скорее всего в результате пересоздания WMI.

mofcomp -N: “C:\Program Files\Microsoft System Center 2012 R2\Virtual Machine Managersetup\NPIV.mof
  
Данной командой его можно создать, при выполнении команды будет выдано предупреждение что mof файл не содержит всей необходимой информации и при пересоздании WMI будет утерян.