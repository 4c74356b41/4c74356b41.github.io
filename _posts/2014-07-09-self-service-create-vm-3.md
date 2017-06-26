---
id: 1261
title: Self Service виртуальных машин; Создание виртуальной машины с портала SCSM (часть 3)
date: 2014-07-09T14:18:54+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post1261
permalink: /post1261
categories:
  - Virtualization and Cloud
tags:
  - Guide
  - Operations Manager
  - Orchestrator
  - Private Cloud VM Self Service
  - Service Manager
  - System Center 2012 R2
  - Virtual Machine Manager
---
Продолжим настройку платформы самообслуживания пользователей.
  
1. [Создание Runbook'а](http://4c74356b41.com/post1176); (часть 1)
  
2. [Создание дочерних Runbook'ов](http://4c74356b41.com/post1227); (часть 2)
  
3. Импорт Runbook'ов в SCSM; (часть 3)
  
4. Создание шаблонов для публикации на портале; (часть 3)
  
5. [Подготовка Request Offering к публикации](http://4c74356b41.com/post1284); (часть 4)
  
6. [Публикация и проверка](http://4c74356b41.com/post1284). (часть 4)

**Импортирование runbook'ов в SCSM**
  
Откройте консоль SCSM и в закладке Administration синхронизируйте коннектор с Orchestrator'ом
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/import-runbook-00.png" rel="attachment wp-att-5098"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/import-runbook-00-300x146.png" alt="import-runbook-00" width="300" height="146" /></a>
  
Сложновато, да? 😉

**Создание шаблонов для публикации Service Offering**
  
В консоли SCSM в закладке Library откройте пункт Runbook, выберите Ваш новый Runbook (создание виртуальной машины) и создайте шаблон автоматизации
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/import-runbook-01.png" rel="attachment wp-att-5101"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/import-runbook-01-300x77.png" alt="import-runbook-01" width="300" height="77" /></a>
  
Дайте шаблону название, выберите management pack или создайте новый (рекомендуется). Нажмите "OK" и закройте открывшееся после этого окно.

Теперь нужно подготовить шаблон собственно Service Offering. В закладке Library откройте пункт Templates и создайте новый шаблон
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/import-runbook-02.png" rel="attachment wp-att-5105"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/import-runbook-02-300x93.png" alt="import-runbook-02" width="300" height="93" /></a>
  
Дайте ему название, выберите класс "Service Request"
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/import-runbook-03.png" rel="attachment wp-att-5108"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/import-runbook-03-300x278.png" alt="import-runbook-03" width="300" height="278" /></a>
  
После этого, в новом окне заполните поля: название, приоритет , срочность - обязательно, а остальные - желательно. Перейдите в закладку "Activities" и нажмите плюсик справа сверху
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/import-runbook-04.png" rel="attachment wp-att-5111"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/import-runbook-04-300x244.png" alt="import-runbook-04" width="300" height="244" /></a>
  
И выберите только что созданный шаблон Runbook Automation Activity
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/import-runbook-05.png" rel="attachment wp-att-5115"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/import-runbook-05-287x300.png" alt="import-runbook-05" width="287" height="300" /></a>
  
Теперь Вам предстоит очень ответственный момент, необходимо замапить (сопоставить с) переменные из runbook'а. Переменную SR GUID необходимо сопоставить с переменной ID Service Request, а остальные переменные с соответствующими переменными runbook'а. В данном случае, VM Name со второй переменной
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/import-runbook-06.png" rel="attachment wp-att-5118"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/import-runbook-06-300x249.png" alt="import-runbook-06" width="300" height="249" /></a>
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/import-runbook-07.png" rel="attachment wp-att-5122"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/import-runbook-07-300x263.png" alt="import-runbook-07" width="300" height="263" /></a>
  
Как определить с какой переменной сопоставлять? Ну очень просто, но не удобно. Открываете шаг Initialize Data и просто пересчитываете переменные по порядку
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/import-runbook-08.png" rel="attachment wp-att-5126"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/import-runbook-08-300x205.png" alt="import-runbook-08" width="300" height="205" /></a>
  
Осталось только сохранить шаблон Service Request'а и читать следующую статью, в которой я поясню для чего мы сопоставляли переменные.