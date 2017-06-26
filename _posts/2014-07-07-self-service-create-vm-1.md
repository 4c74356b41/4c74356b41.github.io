---
id: 1176
title: Self Service виртуальных машин; Создание виртуальной машины с портала SCSM (часть 1)
date: 2014-07-07T17:24:21+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post1176
permalink: /post1176
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

1. Создание виртуальной машины;
  
2. [Изменение виртуальной машины](http://4c74356b41.com/post1381);
  
3. [Удаление виртуальной машины](http://4c74356b41.com/post1326);
  
4. [Создание сервиса из шаблона сервиса](http://4c74356b41.com/post1062).

**Что будет сделано**
  
1. Создание Runbook'а; (часть 1)
  
2. [Создание дочерних Runbook'ов](http://4c74356b41.com/post1227); (часть 2)
  
3. [Импорт Runbook'ов в SCSM](http://4c74356b41.com/post1261); (часть 3)
  
4. [Создание шаблонов для публикации на портале](http://4c74356b41.com/post1261); (часть 3)
  
5. [Подготовка Request Offering к публикации](http://4c74356b41.com/post1284); (часть 4)
  
6. [Публикация и проверка](http://4c74356b41.com/post1284). (часть 4)

**Создание Runbook'а**
  
Runbook, который будет создавать виртуальные машины, выглядит приблизительно так
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/pc_newvm_00.png" rel="attachment wp-att-5171"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/pc_newvm_00-300x146.png" alt="pc_newvm_00" width="300" height="146" /></a>
  
Я останавлюсь на его создании крайне подробно. Для начала откройте Runbook Designer
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/pc_newvm_021.png" rel="attachment wp-att-5220"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/pc_newvm_021-300x225.png" alt="pc_newvm_021" width="300" height="225" /></a>
  
Создайте папку с осмысленным названием и в ней новый Runbook
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/pc_newvm_04.png" rel="attachment wp-att-5181"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/pc_newvm_04-300x249.png" alt="pc_newvm_04" width="300" height="249" /></a>
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/pc_newvm_05.png" rel="attachment wp-att-5184"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/pc_newvm_05-300x267.png" alt="pc_newvm_05" width="300" height="267" /></a>
  
После этого необходимо заполнить runbook шагами. Первым шагом будет "Initialize Data". Для создания шага в панели справа выберите пункт "Runbook Control" и действие "Initialize Data" и перетащите его в рабочую область.
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/pc_newvm_01.png" rel="attachment wp-att-5175"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/pc_newvm_01-151x300.png" alt="pc_newvm_01" width="151" height="300" /></a>
  
После этого двойным шелчком откройте свойства данного шага и при необходимости добавьте или переименуйте шаги
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/pc_newvm_03.png" rel="attachment wp-att-5178"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/pc_newvm_03-300x205.png" alt="pc_newvm_03" width="300" height="205" /></a>
  
Вы так же можете создать дополнительные переменные сейчас, на случай дальнейших кастомизаций. Я всегда рекомендую создавать запасные переменные, дело в том, что если Вы добавляете переменную после того как Вы создали шаблон runbook'а, он будет помечен как "failed" (или что-то в таком духе), и Вам придется пересоздавать шаблон и request offering.
  
Для того, чтобы шаги были связаны, Вам необходимо создать link между шагами. При наведении мышки на шаг Вы заметите маленькие стрелочки по бокам. Та что слева - "вход", а что справа "выход". Таким образом, для связывания двух шагов Вам нужно провести link между выходом однога шага ко входу другого.
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/pc_newvm_20.png" rel="attachment wp-att-5218"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/pc_newvm_20.png" alt="pc_newvm_20" width="251" height="90" /></a>

**2. Get SR**
  
Этот шаг и далее, до шагов VMM, из SCSM integration pack.
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/pc_newvm_061.png" rel="attachment wp-att-5223"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/pc_newvm_061-85x300.png" alt="pc_newvm_061" width="85" height="300" /></a>
  
Action: Get Object
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/pc_newvm_07.png" rel="attachment wp-att-5187"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/pc_newvm_07-85x300.png" alt="pc_newvm_07" width="85" height="300" /></a>
  
После этого откройте свойства данного шага, выбирайте коннектор, класс и создаете фильтр
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/pc_newvm_08.png" rel="attachment wp-att-5191"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/pc_newvm_08-300x206.png" alt="pc_newvm_08" width="300" height="206" /></a>
  
Connector: SCSM Connector
  
Class: Service Request
  
Filter: "SC Object GUID" equals {SR GUID" from "Initialize Data"}
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/pc_st_03.png" rel="attachment wp-att-5237"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/pc_st_03-300x182.png" alt="pc_st_03" width="300" height="182" /></a>
  
Для того, чтобы в поле Value передать значение из какого-либо шага runbook'а, Вам необходимо нажать правой кнопкой мыши и выбрать Subscribe >> Published Data
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/pc_newvm_09.png" rel="attachment wp-att-5194"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/pc_newvm_09-300x259.png" alt="pc_newvm_09" width="300" height="259" /></a>

**3. Get Relationship SR to Template**
  
Action: Get Relationsship
  
Connector: SCSM Connector
  
Object Class: Service Request
  
Object GUID: {SC Object GUID from "Get SR"}
  
Related Class: Virtual Machine Template
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/pc_newvm_101.png" rel="attachment wp-att-5227"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/pc_newvm_101-300x206.png" alt="pc_newvm_101" width="300" height="206" /></a>
  
Остальные шаги создаются по подобию данных шагов.

**4. Get Object – Template**
  
Action: Get Object
  
Connector: SCSM Connector
  
Class: Virtual Machine Template
  
Filter: "SC Object GUID" equals {Related object GUID from "Get Relationship - SR to Template"}
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/pc_newvm_11.png" rel="attachment wp-att-5197"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/pc_newvm_11-300x282.png" alt="pc_newvm_11" width="300" height="282" /></a>

**5. Get Relationship – Affected User**
  
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
  
Object Class: {SC Object GUID from "Get SR"}
  
Related Class: Private Cloud

**8. Get Object – Cloud**
  
Action: Get Object
  
Connector: SCSM Connector
  
Class: Private Cloud
  
Filter: "SC Object GUID" equals {Related object GUID" from "Get Relationship SR to Cloud"}

Теперь я поясню, что тут происходит. Второй шаг берет SR GUID, который SCSM передает в Runbook, и запрашивает Service Request из SCSM. После этого шаги 3, 5 и 7 запрашивают связанные с Service Request объекты, а шаги 4, 6 и 8 "получают" эти объекты.

**9. Run .Net Script** (опциональный параметр, я использую его для генирации пароля администратора)
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/pc_newvm_12.png" rel="attachment wp-att-5201"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/pc_newvm_12-300x173.png" alt="pc_newvm_12" width="300" height="173" /></a>
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/pc_newvm_13.png" rel="attachment wp-att-5204"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/pc_newvm_13-300x138.png" alt="pc_newvm_13" width="300" height="138" /></a>

Обратите внимание, что в разделе "Published Data", переменная указывается без знака "$". Вы можете просто создать еще одну переменную и запрашивать пароль на портале.

**10. Create VM from Template**
  
Этот шаг и шаги далее используют VMM Integration Pack
  
Action: Create VM from Template
  
Connector: VMM Connector
  
Properties:
  
Destination Type - Cloud
  
Destination - {"Display Name from "Get Object - Cloud"}
  
Path - не меняем
  
VM Name - {VM Name from "Initialize Data"}
  
Source Template Name - {Name from "Get Object - Template"}
  
Cloud Capability Profile - выберите подходящий Вам
  
Computer Name - {VM Name from "Initialize Data"}
  
Description - опционально
  
Admin User Name - administrator
  
Admin Password - {Password from "Run .Net Script"}<a href="http://4c74356b41.com/wp-content/uploads/2016/02/pc_newvm_14.png" rel="attachment wp-att-5207"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/pc_newvm_14-300x205.png" alt="pc_newvm_14" width="300" height="205" /></a>

**11. Get VM**
  
Action: Get VM
  
Connector: VMM Connector
  
Filter: VM Name equals {VM Name from "Initialize Data"}

**12. Update VM**
  
Action: Get VM
  
Connector: VMM Connector
  
VM ID: {VM ID from "Get VM"}
  
Owner: domain{User Name from "Get Object - Affected User}
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/pc_newvm_15.png" rel="attachment wp-att-5210"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/pc_newvm_15-300x251.png" alt="pc_newvm_15" width="300" height="251" /></a>
  
Последние 2 действия нужны для смены владельца виртуальной машины, чтобы создатель виртуальной машины получил права на управления её через портал SCSM в дальнейшем. Когда я указывал владельца при создании машины через шаг "Create VM from Template", разворачивание заканчивалось ошибкой, это workaround.

**13. Launch VM**
  
Этот шаг запускает другой Runbook, который в свою очередь запускает виртуальную машину. Для теста можно заменить этот шаг на просто шаг запуск виртуальной машины (Start VM).

**14. Update Object**
  
Опциональный шаг, в моем случае возвращает в Service Request dns имя машины, IP адрес и учетные данные для подключения.
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/pc_newvm_16.png" rel="attachment wp-att-5214"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/pc_newvm_16-300x217.png" alt="pc_newvm_16" width="300" height="217" /></a>
  
Вы могли обратить внимание на {IP from "Launch VM"}. Эта переменная содержит IP виртуальной машины из дочернего ранбука, подробнее в [следующем посте](http://4c74356b41.com/post1227).