---
id: 823
title: 'SMA Studio 2014 - утилита для работы с Service Management Automation'
date: 2014-06-26T11:42:36+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post823
permalink: /post823
categories:
  - Azure Pack
  - Virtualization and Cloud
tags:
  - Copypaste
  - Service Management Automation
  - SMA
  - Windows Azure Pack
---
Хочу поведать Вам об этом <a href="http://www.sekurbit.se/" target="_blank">чудесном продукте</a>.

Данная утилита является аналогом Runbook Designer'а для Service Management Automation. На данный момент SMA поставляется как часть Orchestrator и состоит из трех частей.
  
Web Service - Endpoint для соедиения SMA с WAP и SMA Studio;
  
Runbook Worker - сервис выполняющий ранбуки;
  
Powershell Module - модуль повершел для работы с SMA.

SMA использует исключительно Powershell Workflow (в отличие от Orchestrator) и является прекрасной платформой для автоматизации, но что если у Вас нет Windows Azure Pack или нет желания его внедрять только для тестирования SMA?

SMA Studio позволяет Вам управлять Вашими runbook'ами используя визуальный редактор

1. Просматривать, редактировать, runbool'и переменные и учетные данные;
  
2. Редактировать runbook'и с "подсветкой" синтаксиса;
  
3. Сверять версии runbook'ов и откатываться к предыдущим версиям;
  
4. Тестировать runbook'и и просматривать результат как в Orchestrator Runbook Tester.

**Требования**
  
1. Windows 7 или выше;
  
2. .NET Framework 4.5;
  
3. Развернутое SMA;
  
4. Пользователь с правами администратора SMA.

"Подсветка" ошибок
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/sma-studio-01.png" rel="attachment wp-att-4897"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/sma-studio-01-289x300.png" alt="sma-studio-01" width="289" height="300" /></a>

Сравнение версий runbook'ов (этой функции пока еще нет в WAP'е)
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/sma-studio-02.png" rel="attachment wp-att-4901"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/sma-studio-02-300x87.png" alt="sma-studio-02" width="300" height="87" /></a>

Тестирование runbook'а
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/sma-studio-03.png" rel="attachment wp-att-4904"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/sma-studio-03-300x134.png" alt="sma-studio-03" width="300" height="134" /></a>
  
**В последнем обновлении добавились новые функции**
  
1. Шаблоны runbook'ов;
  
2. Группировка runbook'ов по тегам;
  
3. Баг фиксы.

&nbsp;