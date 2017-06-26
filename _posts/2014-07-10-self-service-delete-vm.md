---
id: 1326
title: Self Service виртуальных машин; Удаление виртуальной машины с портала
date: 2014-07-10T11:18:30+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post1326
permalink: /post1326
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
Продолжаю цикл статей про самообслуживание пользователей. Перед прочтением этой статьи рекомендую ознакомиться с "[подготовительными процедурами](http://4c74356b41.com/post1139)".

1. [Создание виртуальной машины](http://4c74356b41.com/post1176);
  
2. [Изменение виртуальной машины](http://4c74356b41.com/post1381);
  
3. Удаление виртуальной машины;
  
4. [Создание сервиса из шаблона сервиса](http://4c74356b41.com/post1062).

Итак, я предполагаю что у Вас есть SCSM, Orchestrator, SCOM и VMM, которые [настроены, интегрированы и работают](http://4c74356b41.com/post1139).
  
Если Вы еще не знакомы с Orchestrator, подробнее процесс создания runbook'а, аналогичного данному, описан в [другой статье.](http://4c74356b41.com/post1176)

Со стороны SCSM Вам нужен только Request Offering опубликованный на портале, создание его аналогично созданию [других Request Offering'ов для связки SCSM и Orchestrator](http://4c74356b41.com/post1284), поэтому его я описывать не буду. Перечислю только информацию, которую Вам нужно передать в Orchestrator. Виртуальную машину и подтверждение на удаление.

Со стороны Orchestrator Вам нужен Runbook (удивительно), который выглядит приблизительно вот так
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/pc-del-00.png" rel="attachment wp-att-5243"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/pc-del-00-300x205.png" alt="pc-del-00" width="300" height="205" /></a>

**Создаем Runbook**

**1. Initialize Data**
  
Создайте шаг и создайте переменные как на картинке. 😉
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/pc-del-01.png" rel="attachment wp-att-5247"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/pc-del-01-300x206.png" alt="pc-del-01" width="300" height="206" /></a>
  
Обращаю внимание, если Вы хотите чтобы runbook исполнялся только после подтверждения (в моем случае, на портале создан запрос на который пользователб должен ответить "Подтверждаю") Вам необходимо настроить "Link" от шага "Initialize Data" до шага "Get SR", где переменная "Confirm" равняется "Подтверждаю"
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/pc-del-02.png" rel="attachment wp-att-5250"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/pc-del-02-300x205.png" alt="pc-del-02" width="300" height="205" /></a>

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

**9. Remove VM**
  
Action: Remove VM
  
Connector: VMM Connector
  
Filter: VM ID equals {VM ID from "Get VM"}

Остальные шаги опциональны.