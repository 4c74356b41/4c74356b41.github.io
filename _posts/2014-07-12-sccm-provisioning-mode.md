---
id: 1367
title: 'Выводим клиент из "Provisioning Mode" во время OSD'
date: 2014-07-12T13:46:36+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post1367
permalink: /post1367
categories:
  - SCCM
tags:
  - Configuration Manager
  - Copypaste
  - Guide
---
Если после OSD в реестре свежего Windows Вы находите ключ
  
HKEY\_LOCAL\_MACHINE\SOFTWARE\Microsoft\CCM\CcmExec\ProvisioingMode
  
со значением "True", Ваш агент SCCM не выходит из "Provisioning Mode" после завершения OSD. Это значит что он не будет получать политики. у него не будет сертификата клиента, SCEP не сможет быть установлен по время OSD и в консоли клиента SCCM будет меньше возможных действий.

В случае если по какой-то причине это происходит Вам необходимо добавить 2 шага в OSD после шага Setup Windows and ConfigMgr Client.
  
Тип: Run Command Line
  
Команда: REG ADD HKEY\_LOCAL\_MACHINE\SOFTWARE\Microsoft\CCM\CcmExec /v ProvisioningMode /t REG_SZ /d false /f

Тип: Run Command Line
  
Команда: REG ADD HKEY\_LOCAL\_MACHINE\SOFTWARE\Microsoft\CCM\CcmExec /v SystemTaskExcludes /t REG_SZ /d “” /f