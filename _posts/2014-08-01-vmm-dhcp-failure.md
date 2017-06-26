---
id: 1444
title: Виртуальные машины долго не получают IP адрес после перезагрузки
date: 2014-08-01T11:19:23+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post1444
permalink: /post1444
categories:
  - Azure Pack
  - Virtualization and Cloud
tags:
  - Copypaste
  - Guide
  - Hyper-V
  - Virtual Machine Manager
  - Windows Azure Pack
---
При использовании виртуализации сети и использовании динамических адресов в VMM (2012 R2), виртуальные машины могут полчать адрес от VMM DHCP только через несколько минут.

Для проверки выполните на хосте где расположена виртуальная машина команду:
  
Get-WmiObject -Class win32_product -Filter &#8216;Name = "Microsoft System Center Virtual Machine Manager DHCP Server (x64)"&#8216;
  
Данное поведение наблюдается если версия ниже чем 3.2.7649.0.

**Решение:**
  
Обновите VMM до версии Update Rollup 3 (UR3) или выше (2965414 - [Update rollup 3 for System Center 2012 R2 Virtual Machine Manager](http://support.microsoft.com/kb/2965414)).
  
После этого возмите MSI пакет сервера VMM DHCP из папки VMM (путь\_до\_каталога\_установки\_VMM\SwExtn\DHCPExtn.msi) и запустите данный файл на хостах Hyper-V. После этого проблема исчезнет.

[Source](http://blogs.technet.com/b/scvmm/archive/2014/07/31/support-tip-vms-deployed-to-hyper-v-networks-experience-delays-acquiring-an-ip-address-after-reboot.aspx)