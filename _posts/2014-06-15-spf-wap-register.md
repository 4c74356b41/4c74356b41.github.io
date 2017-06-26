---
id: 466
title: Регистрация SPF в Windows Azure Pack
date: 2014-06-15T17:58:13+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post466
permalink: /post466
categories:
  - Azure Pack
  - Virtualization and Cloud
tags:
  - Guide
  - Service Provider Foundation
  - SPF
  - System Center 2012 R2
  - Virtual Machine Manager
  - WAPack Express
  - Windows Azure Pack
---
В [прошлом посте посвященном SPF](http://4c74356b41.com/post459) мы создали локальную учетную запись spf-local. Для чего это необходимо?

Дело в том, что Windows Azure Pack не может зарегистрировать SPF endpoint корректно при использовании доменной учетной записи. Данный аккаунт необходимо добавить в локальные группы spf-admin, spf-vmm, spf-provider, spf-usage. Учетную запись spf-app-pool тоже необходимо добавить в данные группы, кроме того, этой учетной записи необходимы права SA (sysdamin) для SQL базы данных где хранится база SPF и права администратора VMM.

Следующим шагом будет регистрация SPF Endpoint в Windows Azure Pack. Для этого необходимо зайти на Admin Portal (https://hostname:30091/) в раздел VM Clouds и выбрать пункт Register System Center Service Provider Foundation.

<a href="http://4c74356b41.com/wp-content/uploads/2016/02/spf.jpg" rel="attachment wp-att-4909"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/spf-300x191.jpg" alt="spf" width="300" height="191" /></a>

<a href="http://4c74356b41.com/wp-content/uploads/2016/02/spf_reg_2.jpg" rel="attachment wp-att-4910"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/spf_reg_2-300x201.jpg" alt="spf_reg_2" width="300" height="201" /></a>

В окне регистрации SPF Endpoint укажите URL вида https://hostname:8090/ и данные локальной учетной записи spf-local. После успешной регистрации SPF необходимо добавить провайдер VMM. Для добавления провайдера VMM необходимо нажать на плюсик (NEW) в левом нижнем углу и выбрать VM Clouds. После чего необходимо заполнить FQDN сервера VMM и порт (в случае если Вы его меняли). В случае если VMM не регистрируется Вы скорее всего забыли дать права администратора учетной записи spf-app-pool в VMM.

[Продолжение приключений с WAP.](http://4c74356b41.com/post655)

Как удалить SPF Endpoint из Windows Azure Pack
  
Необходимо отредактировать базу данных Microsoft.MgmtSvc.Store (база данных не SPF, а Windows Azure Pack) и сделать IIS Reset Admin сайта:
  
Table: mp.ResourceProviders, Record : systemcenter.
  
Можно удалить руками (найти эту запись и щелкнув на неё правой кнопкой мыши и выбрать удалить) или запросом:
  
DELETE FROM mp.ResourceProviders
  
Where Name = ‘systemcenter’