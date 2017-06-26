---
id: 396
title: FIM Powershell Workflow на Windows Server 2012 R2
date: 2014-05-23T10:24:08+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post396
permalink: /post396
categories:
  - MIM
tags:
  - Copypaste
  - FIM
---
Основная проблема - невозможно использовать модули повершела версии 3 или 4. $PSVersionTable.PSVersion запущенный из FIM WF возвращает значение 2, а не 3 или 4. Как с этим бороться?

**2 варианта:**
  
- powershell version 3.0 -command путь\_до\_скрипта.ps1 -TargetGuid $fimwf.TargetId.Guid (чтобы передать параметры в скрипт), а в скрипт нужно добавить param([guid]$TargetGuid)
  
- добавить в файл "C:\Program Files\Microsoft Forefront Identity Manager\2010\Service\Microsoft.ResourceManagement.Service.exe.config"

<startup>
  
<supportedRuntime version="v4.0&#8243;/>
  
<supportedRuntime version="v2.0.50727&#8243;/>
  
</startup>

Как-то так 😉