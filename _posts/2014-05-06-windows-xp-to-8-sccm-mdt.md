---
id: 379
title: Миграция с Windows XP на 8.1 с использованием SCCM 2012 R2 и MDT 2013
date: 2014-05-06T15:51:19+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post379
permalink: /post379
categories:
  - SCCM
tags:
  - Configuration Manager
  - Guide
---
Верхнеуровневое разбиение работ:

1. Подготовка SCCM к процедуре OSD
  
2. Создание необходимых пакетов
  
3. Создание необходимых Task Sequence'ов (далее TS)
  
4. Связывание компьютеров в SCCM
  
5. Миграция данных с Windows XP на точку миграции данных.
  
6. Установка Windows 8.1 на компьютер с восстановлением заранее мигрированных данных.

**Ограничения:**

1. На всех машинах с Windows XP должен быть установлен SCCM Client
  
2. Мигрировать можно папки и файлы, настройки не переедут.

**Подготовка SCCM к процедуре OSD**
  
1. Подготовка PXE
  
Открываем консоль, далее топаем в Administration > Servers and Site System Roles > Distribution Point, открываем свойства, ставим галочку «Enable PXE support for clients», «Enable unknown computer support» и «Allow this distribution point to respond to incoming PXE requests». Кроме того, Вам необходимо сконфигурировать DHCP для корректной работы PXE (настройки WDS трогать не нужно).
  
опция 66 — NetBIOS имя PXE сервера
  
опция 67 — smsbootx64wdsnbp.com

2. Установка роли State Migration Point
  
Открываем консоль, далее топаем в Administration > Sites, правой кнопкой мыши на необходимый сайт "Add Site System Roles". В случае если у Вас Standalone Primary Site (а это верно для 99.99% читающих это) нажимайте на кнопку "далее" N-нное количество раз, не забудьте выбрать роль State Migration Point, указать папку для хранения данных и срок удержания данных после успешной миграции.

**Создание необходимых пакетов**
  
1. Добавление образа Windows 8.1
  
Я лично добавил просто install.wim с установочного диска (в рамках теста), если у Вас есть корпоративный образ добавьте его.

2. Добавление пакета USMT.
  
USMT 6.3 создается при установке SCCM, нам нужен USMT 5.0 (build 6.2.9200.16384), качаем [ADK](http://www.microsoft.com/en-us/download/details.aspx?id=30652) и ставим на какую-то машину только USMT (лучше не на машину с уже установленным USMT 6.3) и "выдираем" из неё файлы USMT (папка по умолчанию C:Program Files (x86)Windows Kits8.0Assessment and Deployment KitUser State Migration Tool)
  
После чего копируем их на сервер и создаем пакет в который входят скопированные файлы, программу создавать не нужно.

3. Создание MDT Boot Image
  
Открываем консоль, далее топаем в Software Library > Operating Systems > Boot Images. "Create Boot Image using MDT", вводим имя, описание, путь до места хранения пакета, после чего выбираем битность и размер "Scratch Space", рекомендуется выбрать размер не менее 128мб. Необходимо создать и x86 и x64 образы. После создания необходимо зайти в свойства созданных образов и поставить галочку "Deploy this boot image from the PXE-enabled distribution point"

**Создание необходимых Task Sequence'ов**
  
1. Создание TS для миграции данных с Windows XP.
  
Открываем консоль, далее топаем в Software Library > Operating Systems > Task Sequence. Создаем обычный «Custom Task Sequence» с тремя шагами: Request State Store, Capture User State, Release State Store. В шаге Capture User State необходимо выбрать пункт «Customize how user profiles are captured» и добавить файлы MigDocs.xml и MigUser.xml.
  
В данном TS будет использоваться пакет USMT 5.0

2. Созданье TS для установки Windows 8.1
  
Открываем консоль, далее топаем в Software Library > Operating Systems > Task Sequence. Создаем MDT Task Sequence. Задаем имя и комментарии, вводим информацию об организации, вводе в домен и тд, на следующем экране оставляем галочку «This task sequence will never be used to capture an image». Выбираем загрузочный образ и пакет Windows 8.1 созданные ранее. Создаем новый MDT Toolkit Package, заполняем информацию. Выбираем пункт «Zero Touch Installation». Выбираем пакет клиента SCCM. Выбираем пакет USMT (6.3!) Создаем новый MDT Settings Package, заполняем информацию. Жмем «далее» до конца.

3. Модификация TS
  
Необходимо модифицировать наш TS чтобы он [работал](http://www.deploymentresearch.com/Research/tabid/62/EntryId/80/Fixing-the-Computer-Replace-uberbug-in-MDT-2012-Update-1-With-ConfigMgr.aspx). Открываем консоль, далее топаем в Software Library > Operating Systems > Task Sequence. Выбираем наш TS и нажимаем "Edit". Находим шаг "Set Status 5" и добавляем после него шаг "Request State Store" и выбираем "Restore State from another computer"
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/e837859f6cfe7778b7de2532e9c1b4d9.jpg" rel="attachment wp-att-4777"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/e837859f6cfe7778b7de2532e9c1b4d9-300x270.jpg" alt="e837859f6cfe7778b7de2532e9c1b4d9" width="300" height="270" /></a>

В закладке "Options" добавьте условие "Task Sequence Variable" "USMTLOCAL" "Not equals" "True"<a href="http://4c74356b41.com/wp-content/uploads/2016/02/bbd7fcc592dc5391bd77dc0604f54c6e.jpg" rel="attachment wp-att-4766"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/bbd7fcc592dc5391bd77dc0604f54c6e-287x300.jpg" alt="bbd7fcc592dc5391bd77dc0604f54c6e" width="287" height="300" /></a>

Добавьте под пунктом "Restore User State" пункт "Release State Store" и добавьте для него такое же условие.
  
Далее в пункте "Restore User State" выберите пункт "Customize how user profiles are restored" и добавить файлы MigDocs.xml и MigUser.xml
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/304807fc5d1fe123ccc3e03360a30ae1.jpg" rel="attachment wp-att-4762"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/304807fc5d1fe123ccc3e03360a30ae1-300x271.jpg" alt="304807fc5d1fe123ccc3e03360a30ae1" width="300" height="271" /></a>

В пункте "Set Variable for Drive Letter" в группе "Install" измените значение на "True"

4. Модификация CustomSettings.ini
  
При создании MDT Setting Package был создан файл CustomSettings.ini необходимо его модифицировать. Добавьте в него следующие строчки:

```
DeploymentType=NEWCOMPUTER
SLShare=имя_сервераxxxlog - UNC путь к папке куда TS будет копировать логи, очень удобно для траблшутинга.
ScanStateArgs=/v:5 /o /c /ue:%computername%* - внимание, данная команда исключит всех локальных пользователей из процесса миграции.
LoadStateArgs=/v:5 /c
```

5. Распространяем пакеты
  
Необходимо распространить все пакеты и оба образа загрузочных на точку распространения контента. (Я, лично, всегда забываю это сделать)

**Связывание компьютеров в SCCM**
  
Данный шаг необходим для успешности миграции, необходимо связать компьютеры для успешной миграции между разными компьютерами.

Открываем консоль, далее топаем в Assets And Compliance > User State Migration. Выбираем пункт "Create Computer Association" и выбираем исходный компьютер (Windows XP) и целевой (Windows 8.1). Если целевого компьютера еще нет его необходимо создать в SCCM.

В случае если Вам необходимо реализовать сценарий «Refresh», а не «Replace» Вам не нужно связывать компьютеры. Вы просто запускаете сбор данных, после чего перегружаете машину в PXE и запускаете установку Windows 8.1.

Далее следуют пункты 5 и 6.
  
Естественно, для грамотной миграции Вам необходимо правильно создать коллекции на которые Вы "натравите" данные TS'ы.
  
Коллекция со всеми Windows XP компьютерами:

```
select *  from  SMS_R_System inner join SMS_G_System_OPERATING_SYSTEM on SMS_G_System_OPERATING_SYSTEM.ResourceId = SMS_R_System.ResourceId where SMS_G_System_OPERATING_SYSTEM.Caption like "%Windows XP%"
```

Коллекцию для Windows 8.1 компьютеров так же будет необходимо создать.

Таким образом можно мигрировать как настройки со старого компьютера на новый так и в "пределах" одной машины.
  
Из плюсов - копия файлов пользователя на сервере лежит столько сколько нужно, единый сценарий для "Refresh" (этот сценарий лучше реализовывать целиком через WinPE, но для этого необходим отдельный TS) и "Replace" сценариев.
  
Из минусов - 2 TS, один делается не в WinPE потому пользователь может как-то на него повлиять, необходимо много места на State Migration Point для хранения информации пользователей.