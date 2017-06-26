---
id: 1139
title: Настройка SCSM, SCOM, VMM и Orchestrator; Self Service виртуальных машин
date: 2014-07-06T22:22:55+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post1139
permalink: /post1139
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
После того как мы установили [Service Manager](http://4c74356b41.com/post1127), [Orchestrator](http://4c74356b41.com/post1108), [Operations Manager](http://4c74356b41.com/post1085) и [Virtual Machine Manager](http://4c74356b41.com/post413) (если у Вас стоят версии 2012 или 2012 SP1 Вам необходимо будет проделать дополнительные операции, которые не описаны в этой статье) необходимо связать эти компоненты и произвести первоначальную настройку.

**Что произойдет:**
  
1. Связывание Virtual Machine Manager и Operations Manager;
  
2. Связывание Service Manager и Virtual Machine Manager;
  
3. Связывание Service Manager и Operations Manager;
  
4. Связывание Service Manager и Orchestrator;
  
5. Создание VMM и SCSM коннекторов в Orcjestrator;
  
6. Настройка ChargeBack (опционально).

**Что Вам потребуется:**
  
1. Интернет на сервере Operations Manager;
  
2. Дистрибутив Operations Manager;
  
3. Зарегистрированный Data Warehouse в Service Manager (опционально).

Связывание Virtual Machine Manager и Operations Manager
  
Для того чтобы связать VMM и SCOM Вам необходимо проделать несколько операции, установить агенты на все хосты виртуализации и сервера VMM, установить консоль SCOM на сервера VMM и создать коннектор из консоли VMM.
  
Установка агентов тривиальна и я не буду её описывать подробно, вкратце Вам необходимо установить агенты вручную с дистрибутива SCOM и связать их с сервером Operations Manager или из консоли администрирования SCOM запустить мастер обнаружения систем для мониторинга.
  
Для установки консоли SCOM на сервере(-ах) VMM необходимо с дистрибутива SCOM запустить setup.exe и выбрать установку консоли Operations Manager (Далее-далее-далее, Готово).
  
После того как Вы осуществили данные операции необходимо убедиться в наличии необходимых management pack'ов на сервере SCOM:
  
1. Windows Server Internet Information Services 2003
  
2. Windows Server 2008 Operating System (Discovery)
  
3. Windows Server Operating System Library
  
4. Windows Server 2008 Internet Information Services 7
  
5. Windows Server Internet Information Services Library
  
6. SQL Server Core Library
  
Частично эти management pack'и можно скачать через консоль SCOM, а частично они есть на дистрибутиве SCOM (.Management Packs) или из папки (c:Program FilesMicrosoft System Center 2012 R2Service ManagerChargebackDependencies) с сервера где установлен SCSM.
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/post-install-00.png" rel="attachment wp-att-5267"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/post-install-00-281x300.png" alt="post-install-00" width="281" height="300" /></a>
  
Вам необходимо скачать эти Management Pack'и, а не установить их, так как они потребуются далее для SCSM. Импортируйте все 6 management pack'ов в SCOM.
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/post-install-01.png" rel="attachment wp-att-5270"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/post-install-01-281x300.png" alt="post-install-01" width="281" height="300" /></a>
  
Теперь осталось только создать коннектор VMM - SCOM. Для этого из консоли VMM необходимо зайти в пункт Settings, выбрать Operations Manager и нажав правую кнопку мыши выбрать пункт "Properties".
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/post-install-02.png" rel="attachment wp-att-5274"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/post-install-02-300x257.png" alt="post-install-02" width="300" height="257" /></a>
  
Далее Вам останется указать FQDN сервера SCOM, указать учетные данные для подключения к SCOM и настроить параметры.

**Связывание Service Manager и Virtual Machine Manager**
  
Запустите консоль SCSM и в разделе Administration > Connectors Вы можете создать коннекторы для всех компонентов System Center.
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/post-install-03.png" rel="attachment wp-att-5278"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/post-install-03-300x211.png" alt="post-install-03" width="300" height="211" /></a>
  
Выберите "Virtual Machine Manager connector" укажите FQDN и учетные данные для подключения к VMM.

**Связывание Service Manager и Operations Manager**
  
Связывание происходит так же как и в предыдущем пункте, с той лишь разницей, что перед созданием коннектора SCSM - SCOM Вам необходимо импортировать management pack'и в SCSM.
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/post-install-04.png" rel="attachment wp-att-5281"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/post-install-04-276x300.png" alt="post-install-04" width="276" height="300" /></a>
  
Вам необходимо импортировать все management pack'и, которые установил VMM в SCOM и зависимости. Зависимости Вы должны были скачать перед установкой коннектора VMM - SCOM, а management pack'и, которые VMM установил в SCOM находятся в папке VMM (c:Program FilesMicrosoft System Center 2012 R2Virtual Machine ManagerManagementPacks). И только после этого создавать коннектор (Operations Manager Configuration Items).
  
Укажите FQDN и учетные данные для подключения к SCOM, в разделе "Management Packs" укажите все Management Pack'и. Если у Вас не совпадают версии management pack'ов, Вам необходимо будет обновить их в SCSM или в SCOM, чтобы версии соответствовали.

**Связывание Service Manager и Orchestrator**
  
Создайте коннектор (Orchestrator connector)
  
Укажите Web Service URL (вида http://fqdn:81/orchestrator2012/orchestrator.svc) корневую папку и URL web console (http://fqdn:82/) и аккаунт для подключения к Orchestrator.

**Создание коннекторов VMM и SCSM в Orchestrator**
  
Откройте "Runbook Designer" на сервере Orchestrator
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/post-install-10.png" rel="attachment wp-att-5302"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/post-install-10-300x193.png" alt="post-install-10" width="300" height="193" /></a>
  
Далее в появившемся окне создайте новый коннектор, дайте ему имя, введите учетные данные и FQDN для подключения. Для VMM операция аналогична, но есть нюанс, в поле адрес консоли укажите FQDN сервера VMM, а в поле сервер VMM значение "localhost".

**Настройка Chargeback**
  
Для того чтобы в SCSM появилась функция "Chargeback" Вам необходимо импортировать соответствующиq Management Pack Bundle, которыq расположен в папке c:Program FilesMicrosoft System Center 2012 R2Service ManagerChargeback и называется Chargeback.mpb.
  
После того как импорт закончен Вам необходимо будет дождаться синхронизации с Data Warehouse.
  
После этого создать прайс лист для облака, опубликовать его и связать его с облаком.
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/post-install-05.png" rel="attachment wp-att-5284"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/post-install-05-225x300.png" alt="post-install-05" width="225" height="300" /></a>
  
После этих операций у Вас появится новый куб в Data Warehouse и его можно анализировать в Excel.
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/post-install-06.png" rel="attachment wp-att-5287"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/post-install-06-300x142.png" alt="post-install-06" width="300" height="142" /></a>

**Проверка**
  
Бегикниги.
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/post-install-07.png" rel="attachment wp-att-5290"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/post-install-07-297x300.png" alt="post-install-07" width="297" height="300" /></a>
  
Классы виртуальных машин, дисков, адаптеров и так далее. Для этого просто создайте необходимый "Вид" и просмотрите его.
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/post-install-08.png" rel="attachment wp-att-5294"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/post-install-08-161x300.png" alt="post-install-08" width="161" height="300" /></a>
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/post-install-09.png" rel="attachment wp-att-5298"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/post-install-09-254x300.png" alt="post-install-09" width="254" height="300" /></a>

Если везде появились данные, значит все настроено правильно и можно продолжать чтение. 😉 В следующей статье мы будем настраивать непосредственно runbook'и и действия на портале.