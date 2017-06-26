---
id: 857
title: 'Ошибка при первом логине "The universal unique identifier (UUID) type is not supported"'
date: 2014-06-26T23:28:17+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post857
permalink: /post857
categories:
  - SCCM
tags:
  - Configuration Manager
  - Copypaste
---
При разворачивании Windows 8 или Windows 8.1 с использованием SCCM 2012 R2 пользователи могут получить сообщение следующего вида
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/SCCM_GPC_Error.png" rel="attachment wp-att-4826"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/SCCM_GPC_Error-300x127.png" alt="SCCM_GPC_Error" width="300" height="127" /></a>

**Workaround 1**
  
Добавьте рестарт в последний таск вашего Task Sequence'а. SMSTSPostAction shutdown /r /t 0

**Workaround 2**
  
Выполните следующую команду из Task Sequence'а. cmd /c reg add "HKLMSYSTEMCurrentControlSetServicesgpsvc" /v Type /t REG_DWORD /d 0x10 /f

Подробнее [KB2976660](http://support.microsoft.com/kb/2976660/en-us)