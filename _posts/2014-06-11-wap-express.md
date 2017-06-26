---
id: 422
title: Экспресс установка Windows Azure Pack
date: 2014-06-11T11:35:00+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post422
permalink: /post422
categories:
  - Azure Pack
tags:
  - Guide
  - WAPack Express
  - Windows Azure Pack
---
В данной статье я расскажу Вам как производится экспресс установка Windows Azure Pack (далее WAP или WAPack).  
При экспресс установке на один сервер будут установлены следующие компоненты WAPack:
  
Admin API  
Tenant API  
Tenant public API  
Admin authentication site (портал авторизации для администраторов)  
Tenant authentication site (портал авторизации для пользователей)  
Admin site (портал управления для администраторов)  
Tenant site (портал управления для пользователей)

После экспресс установки Вам необходимо будет установить как минимум Service Provider Foundation (об этом следующий пост).

Итак, приступим, необходимое ПО:  
Windows Server® 2012 or Windows Server 2012 R2;  
Microsoft Web Platform Installer 4.6 или выше;  
Microsoft .NET Framework 3.5 Service Pack (SP) 1;  
Internet Information Services (IIS) 8 (встроенный функционал Windows Server 2012) или IIS 8.5 (встроенный функционал Windows Server 2012 R2);  
.NET Framework 4.5 Extended, с ASP.NET для Windows 8.  

необходимое "железо":
  
40гб места на жестком диске  
8гб оперативной памяти (не используйте динамическую память)  
2 ЦПУ минимум на серверной машине

1. Скачайте и запустите [Web Platform Installer](http://www.microsoft.com/web/downloads/platform.aspx);
  
2. Запустите его и выберите "Windows Azure Pack: Portal and API Express" компонент, согласитесь с условиями лицензии, согласитесь скачивать обновления с Windows Update (во время установки нужен доступ к интернету так как Web Platform Installer качает все файлы установщика с сайта Microsoft);
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/wap_express_00.png" rel="attachment wp-att-4983"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/wap_express_00-300x204.png" alt="wap_express_00" width="300" height="204" /></a>
  
3. После того как установка закончена, выключите Internet Explorer Enhanced Security и запустите Internet Explorer от имени администратора;
  
4. Пройдите по ссылке <https://localhost:30101/> для конфигурации Windows Azure Pack;
  
5. На страничке указания базы данных укажите SQL сервер для Windows Azure Pack (Mixed mode Authentication должен быть включен на SQL сервере);
  
6. Далее-далее-далее, Готово.

Для доступа к админ порталу: <https://localhost:30091/#Workspaces/WebSystemAdminExtension/quickStart>
  
Для доступа к тенант портал: <https://localhost:30081/#Workspaces/All/dashboard>
  
Так же WAP при первом заходе на портал проведет для вас чудесный мини-тур по интерфейсу.
  
Но до установки дополнительных компонентов наш портал практически бесполезен, [об этом скоро](http://4c74356b41.com/post459).