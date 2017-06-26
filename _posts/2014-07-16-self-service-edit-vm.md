---
id: 2541
title: Self Service виртуальных машин; Изменение виртуальной машины с портала
date: 2014-07-16T00:03:35+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post1381
permalink: /post2541
categories:
  - Virtualization and Cloud
tags:
  - Guide
  - Operations Manager
  - Private Cloud VM Self Service
  - Service Manager
  - System Center 2012 R2
  - Virtual Machine Manager
---
Продолжаю цикл статей про самообслуживание пользователей. Перед прочтением этой статьи рекомендую ознакомиться с "[подготовительными процедурами](http://4c74356b41.com/post1139)".

1. [Создание виртуальной машины](http://4c74356b41.com/post1176);
  
2. Изменение виртуальной машины;
  
3. [Удаление виртуальной машины](http://4c74356b41.com/post1326);
  
4. [Создание сервиса из шаблона сервиса](http://4c74356b41.com/post1062).

Итак, я предполагаю что у Вас есть SCSM, Orchestrator, SCOM и VMM, которые [настроены, интегрированы и работают](http://4c74356b41.com/post1139).
  
Если Вы еще не знакомы с Orchestrator, подробнее процесс создания runbook'а, аналогичного данному, описан в [другой статье.](http://4c74356b41.com/post1176)

Со стороны SCSM Вам нужен только Request Offering опубликованный на портале, создание его аналогично созданию [других Request Offering'ов для связки SCSM и Orchestrator](http://4c74356b41.com/post1284), поэтому его я описывать не буду. Перечислю только информацию, которую Вам нужно передать в Orchestrator. Виртуальную машину, подтверждение на возможность немедленной перезагрузки и, по желанию, количество процессоров, количество оперативной памяти, VLAN ID, Сколько ГБ места добавить на жесткий диск (или что угодно что придумает Ваша фантазия).

Со стороны Orchestrator Вам нужен Runbook (удивительно), который выглядит приблизительно вот так
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/pc-modifyvm-00.png" rel="attachment wp-att-5253"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/pc-modifyvm-00-300x145.png" alt="pc-modifyvm-00" width="300" height="145" /></a>

**Создаем Runbook**

**1. Initialize Data**
  
Создайте шаг и создайте переменные как на картинке. 😉
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/pc-modifyvm-01.png" rel="attachment wp-att-5258"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/pc-modifyvm-01-300x205.png" alt="pc-modifyvm-01" width="300" height="205" /></a>
  
Обращаю внимание, если Вы хотите чтобы виртуальная машина перезагружалась только после подтверждения (в моем случае, на портале создан запрос на который пользователь может ответить "Да" или "Нет") Вам необходимо настроить "Link" от шага "Initialize Data" до шага "Get SR", где переменная "Shall We Restart VM" ровняется "Да".
  
В моем runbook'е, при выборе "Нет" запрос передается в другой runbook, который ждет следующего окна обслуживания и только тогда перегружает виртуальную машину. Это костыль. Правильнее сделать запись с VM ID в базу данных и runbook, который будет запускаться по рассписанию и из базы данных брать данные о виртуальных машинах и изменениях, которые необходимо к ним применить.
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/pc-modifyvm-02.png" rel="attachment wp-att-5261"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/pc-modifyvm-02-300x206.png" alt="pc-modifyvm-02" width="300" height="206" /></a>

**2. Get SR**
  
Этот шаг и далее, до шагов VMM, из SCSM integration pack.
  
Action: Get Object
  
Connector: SCSM Connector
  
Class: Service Request
  
Filter: "SC Object GUID" equals {SR GUID from "Initialize Data"}

**3. Get Relationship SR to VM**
  
Action: Get Relationsship
  
Connector: SCSM Connector
  
Object Class: Service Request
  
Object GUID: {SC Object GUID from "Get SR"}
  
Related Class: Virtual Machine

**4. Get Object - VM**
  
Action: Get Object
  
Connector: SCSM Connector
  
Class: Virtual Machine
  
Filter: "SC Object GUID" equals {Related object GUID from "Get Relationship SR to VM"}

**5. Get Relationship - Affected User**
  
Action: Get Relationsship
  
Connector: SCSM Connector
  
Object Class: Service Request
  
Object GUID: {SC Object GUID from "Get SR"}
  
Related Class: Active Directory User

**6. Get Object - Affected User**
  
Action: Get Object
  
Connector: SCSM Connector
  
Class: Service Templates
  
Filter: "SC Object GUID" equals {Related object GUID from "Get Relationship - Affected User"}

**7. Get VM**
  
Далее идут шаги VMM
  
Action: Get VM
  
Connector: VMM Connector
  
Filter: VM Name equals {Display Name from "Get Object - VM"}
  
Filter: Owner equals domain{User Name from "Get Object - Affected User"}

**8. Stop VM**
  
Action: Stop VM
  
Connector: VMM Connector
  
Filter: VM ID equals {VM ID from "Get VM"}

**9. Update VM**
  
Action: Update VM
  
Connector: VMM Connector
  
Filter: VM ID equals {VM ID from "Get VM"}
  
CPU Count: {Processor from "Initialize Data"}
  
Memory(MB): {RAM from "Initialize Data"}
  
Внимание, если у виртуальной машины стоит динамическая память, а runbook изменит значение Memory на значение больше чем максимальная память VM перейдет в состояние Failed. Кажется это "By Design", шаг Update VM не умеет работать с динамической памятью. Workaround - PowerShell.

**10. Get Disk**
  
Action: Get Disk
  
Connector: VMM Connector
  
Filter: VM ID equals {VM ID from "Get VM"}

**11. Update Disk**
  
Action: Update Disk
  
Connector: VMM Connector
  
Filter: VM ID equals {Virtual Disk Drive ID from "Get Disk"}
  
Additional Size: {HDD from "Initialize Data"}

По аналогии Вы можете создать и шаги для изменения свойств адаптера.
  
Данные шаги не последовательны по причине того, что если шаг "Get Disk" или "Get Network Adapter" вернет 2 значения (или более), все следующие шаги будут повторятся несколько раз (по числу возвращенных объектов).

После этого можно передавать VM ID в Runbook "Launch VM". Шаг "Launch VM" соответствует уже настроенному шагу "Launch VM" ([тут](http://4c74356b41.com/post1227)).

**Модификация Runbook'а "Launch VM"**
  
Если Вы не читали мы уже [создали](http://4c74356b41.com/post1227) этот runbook. Пришло время добавить в него шаги для сценария изменения VM.
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/module-runbooks-00.png" rel="attachment wp-att-5129"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/module-runbooks-00-300x175.png" alt="module-runbooks-00" width="300" height="175" /></a>
  
Содайте линк к событию "Delay 120", а в линке задайте условие Reserved from Initialize Data does not equals "NewVM"
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/pc-modifyvm-03.png" rel="attachment wp-att-5264"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/pc-modifyvm-03-300x187.png" alt="pc-modifyvm-03" width="300" height="187" /></a>

**2. Delay 120**
  
Action: Run .Net Script
  
Type: PowerShell
  
Script: Sleep 120
  
Ждем пока VMM произведет изменения с дисками и сетевыми адаптерами виртуальной машины.

**3. Start VM**
  
Action: Start VM
  
Connector: VMM Connector
  
Filter: {VM ID from "Get VM"}