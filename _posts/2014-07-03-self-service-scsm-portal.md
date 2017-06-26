---
id: 1062
title: Self Service виртуальных машин; Создание сервиса с портала SCSM
date: 2014-07-03T16:43:52+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post1062
permalink: /post1062
categories:
  - MIM
  - Virtualization and Cloud
tags:
  - Guide
  - Orchestrator
  - Private Cloud VM Self Service
  - Service Manager
  - System Center 2012 R2
  - Virtual Machine Manager
---
С этой статьи я начну цикл статей про SCSM, Orchestrator, SCOM и VMM.
  
Получается, что я начинаю с конца, но поскольку я постоянно забываю написать хоть что-то на эту тему&#8230; это будет хорошим пинком. 😉

1. [Создание виртуальной машины](http://4c74356b41.com/post1176);
  
2. [Изменение виртуальной машины](http://4c74356b41.com/post1381);
  
3. [Удаление виртуальной машины](http://4c74356b41.com/post1326);
  
4. Создание сервиса из шаблона сервиса.

Итак, я предполагаю что у Вас есть SCSM, Orchestrator, SCOM и VMM, которые [настроены, интегрированы и работают](http://4c74356b41.com/post1139).
  
Если Вы еще не знакомы с Orchestrator, подробнее процесс создания runbook'а, аналогичного данному, описан в [другой статье.](http://4c74356b41.com/post1176)

Со стороны SCSM Вам нужен только Request Offering опубликованный на портале, создание его аналогично созданию [других Request Offering'ов для связки SCSM и Orchestrator](http://4c74356b41.com/post1284), поэтому его я описывать не буду. Перечислю только информацию, которую Вам нужно передать в Orchestrator. Имя сервиса в VMM, шаблон сервиса, облако и переменные для разворачивания.

Со стороны VMM Вам нужен готовый шаблон сервиса, я воспользуюсь уже описанным мною [шаблоном](http://4c74356b41.com/post428).

Со стороны Orchestrator Вам нужен Runbook (удивительно), который выглядит приблизительно вот так
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/pc_st_00.png" rel="attachment wp-att-5230"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/pc_st_00-300x126.png" alt="pc_st_00" width="300" height="126" /></a>

**Создаем Runbook**
  
Шаги
  
**1. Initialize Data**
  
Создайте шаг и создайте переменные как на картинке. 😉
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/pc_st_01.png" rel="attachment wp-att-5234"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/pc_st_01-300x205.png" alt="pc_st_01" width="300" height="205" /></a>
  
Переменные Custom1, Custom2 и Custom3 запасные. Я всегда рекомендую создавать запасные переменные, дело в том что если Вы добавляете переменную после того как Вы создали шаблон runbook'а он будет помечен как "failed" или что-то в таком духе, и Вам придется пересоздавать шаблон и request offering.

**2. Get SR**
  
Этот шаг и далее, до шагов VMM, из SCSM integration pack.
  
Action: Get Object
  
Connector: SCSM Connector
  
Class: Service Request
  
Filter: "SC Object GUID" equals {SR GUID from "Initialize Data"}
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/pc_st_03.png" rel="attachment wp-att-5237"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/pc_st_03-300x182.png" alt="pc_st_03" width="300" height="182" /></a>
  
Для того, чтобы в поле Value передать значение из какого-либо шага runbook'а Вам необходимо нажать правой кнопкoй мыши и выбрать Subscribe >> Published Data.

**3. Get Relationship SR to Service**
  
Action: Get Relationsship
  
Connector: SCSM Connector
  
Object Class: Service Request
  
Object GUID: {SC Object GUID from "Get SR"}
  
Related Class: Service Template

**4. Get Object - Service**
  
Action: Get Object
  
Connector: SCSM Connector
  
Class: Service Templates
  
Filter: "SC Object GUID" equals {Related object GUID from "Get Relationship SR to Service"}

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

**7. Get Relationship SR to Cloud**
  
Action: Get Relationsship
  
Connector: SCSM Connector
  
Object Class: Service Request
  
Object GUID: {SC Object GUID from "Get SR"}
  
Related Class: Private Cloud

**8. Get Object - Cloud**
  
Action: Get Object
  
Connector: SCSM Connector
  
Class: Private Cloud
  
Filter: "SC Object GUID" equals {Related object GUID from "Get Relationship SR to Cloud"}

Теперь я поясню что тут происходит. Второй шаг берет SR GUID, который SCSM передает в Runbook, и запрашивает Service Request из SCSM. После этого шаги 3, 5 и 7 запрашивают связанные с Service Request объекты, а шаги 4, 6 и 8 "получают" эти объекты.

**9. Get Service Template**
  
Этот шаг и шаги далее используют VMM Integration Pack
  
Action: Get Service Template
  
Connector: VMM Connector
  
Filter: "Service Template ID" equals {ID Virtual Machine Manager from "Get Object - Service Template"}

**10. Get Object - Cloud**
  
Action: Get Cloud
  
Connector: VMM Connector
  
Filter: "Cloud ID" equals {ID Virtual Machine Manager from "Get Object - Cloud"}

**11. Configure Service Deployment**
  
Action: Configure Service Deployment
  
Connector: VMM Connector
  
Service Configuration Name: {Service Name from "Initialize Data'}
  
Service Template Name: {Service Template Name from "Get Service Template"}
  
Deployment Target: Cloud
  
Cloud Name: {Cloud Name from "Get Object - Cloud"}
  
Service Template Release: {Service Template Release from "Get Service Template}

**12. Get-ServiceConfiguration**
  
Action: Run VMM PowerShell Script
  
Connector: VMM Connector
  
PowerShell:
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/pc_st_041.png" rel="attachment wp-att-5240"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/pc_st_041-300x205.png" alt="pc_st_041" width="300" height="205" /></a>

```
$servicedeployment = Get-SCServiceConfiguration -Name {Service Name from "Initialize Data"};
Update-SCServiceConfiguration -VMMServer "FQDN_сервера_VMM" -ServiceConfiguration $servicedeployment
Get-SCServiceSetting -ServiceConfiguration $servicedeployment -Name "FirstTier" | Set-SCServiceSetting -value {First Tier from "Initialize Data"}
Get-SCServiceSetting -ServiceConfiguration $servicedeployment -Name "SecondTier" | Set-SCServiceSetting -value {Second Tier from "Initialize Data"}
```

Первая строчка просто запрашивает данные, а вторая обновляет Placement, без этого разворачивание невозможно. Далее строчки 3 и 4 присваивают значение переменным.

Output Variable 01: $servicedeployment
  
Если не вернуть хоть какую-то информацию из скрипта шаг заканчивается с ошибкой.
  
Шаги 9-12 создают временное разворачивание, обновляют placement виртуальных машин и заполняют переменыые. Следующий шаг просто запустит разворачивание.

**13. Deploy Service**
  
Action: Deploy Service
  
Connector: VMM Connector
  
Service Configuration Name: {Service Name from "Initialize Data"}

На этом все закончено, можно сохранять ранбук, импортировать его в SCSM, создавать шаблоны и заполнять заявку.