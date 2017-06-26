---
id: 1051
title: Администрирование Service Management Automation
date: 2014-07-03T12:11:41+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post1051
permalink: /post1051
categories:
  - Azure Pack
  - Virtualization and Cloud
tags:
  - Service Management Automation
  - SMA
  - Windows Azure Pack
---
<strong>Purging (очищение) базы данных</strong><br /> Довольно важный аспект жизненного цикла любой программы. SMA использует SQL Server Agent, который запускает внутренную процедуру. Эта процедура запускается раз в 15 минут и удаляет устаревшие задания и удаленные runbook'и.<br /> <a href="http://4c74356b41.com/wp-content/uploads/2016/02/sma_admin_00.png" rel="attachment wp-att-5321"><img class="alignnone size-medium wp-image-5321" src="http://4c74356b41.com/wp-content/uploads/2016/02/sma_admin_00-300x220.png" alt="sma_admin_00" width="300" height="220" srcset="http://4c74356b41.com/wp-content/uploads/2016/02/sma_admin_00-300x220.png 300w, http://4c74356b41.com/wp-content/uploads/2016/02/sma_admin_00-768x563.png 768w, http://4c74356b41.com/wp-content/uploads/2016/02/sma_admin_00.png 970w" sizes="(max-width: 300px) 100vw, 300px" /></a><br /> 

В процедуре присутствует шаг SMA Database Purge Next Batch, который вызывает процедуру SMA.Purge.PurgeNextBatch. Все процедуры Вы можете посмотреть в базе.

 <a href="http://4c74356b41.com/wp-content/uploads/2016/02/sma_admin_03-150x73-1.png" rel="attachment wp-att-5334"><img class="alignnone size-full wp-image-5334" src="http://4c74356b41.com/wp-content/uploads/2016/02/sma_admin_03-150x73-1.png" alt="sma_admin_03-150x73" width="150" height="73" /></a><br /> 

Контролировать параметры количества записей для сохранения и количество дней удержания можно через PowerShell. Get-SmaAdminConfiguration -WebServiceEndpoint "https://fqdn"<br /> <a href="http://4c74356b41.com/wp-content/uploads/2016/02/sma_admin_01.png" rel="attachment wp-att-5325"><img class="alignnone size-medium wp-image-5325" src="http://4c74356b41.com/wp-content/uploads/2016/02/sma_admin_01-300x60.png" alt="sma_admin_01" width="300" height="60" srcset="http://4c74356b41.com/wp-content/uploads/2016/02/sma_admin_01-300x60.png 300w, http://4c74356b41.com/wp-content/uploads/2016/02/sma_admin_01.png 713w" sizes="(max-width: 300px) 100vw, 300px" /></a><br /> 

И менять Set-SMAAdminConfiguration -WebServiceEndpoint "https://fqdn" -PurgeJobsOlderThanCountDays количество_дней -MaxJobRecords количество_записей.

<strong>Системные Runbook'и</strong><br /> C SMA, по умолчанию, идут 2 системных runbook'а<br /> <a href="http://4c74356b41.com/wp-content/uploads/2016/02/sma_admin_02.png" rel="attachment wp-att-5328"><img class="alignnone size-medium wp-image-5328" src="http://4c74356b41.com/wp-content/uploads/2016/02/sma_admin_02-300x32.png" alt="sma_admin_02" width="300" height="32" srcset="http://4c74356b41.com/wp-content/uploads/2016/02/sma_admin_02-300x32.png 300w, http://4c74356b41.com/wp-content/uploads/2016/02/sma_admin_02-768x82.png 768w, http://4c74356b41.com/wp-content/uploads/2016/02/sma_admin_02-1024x109.png 1024w, http://4c74356b41.com/wp-content/uploads/2016/02/sma_admin_02.png 1140w" sizes="(max-width: 300px) 100vw, 300px" /></a><br /> 

DiscoverAllLocalModules - сканирует систему и добавляет все нативные Windows PowerShell модули (только при добавлении SMA в WAP). После чего они доступны при создании runbook'ов (поле insert при редактировании runbook'а в WAP).<br /> SetAutomationModuleActivityMetadata - запускается при импорте нового модуля в SMA. Он собирает данные о модуле. По сути делает то же самое что и первый системный ранбук, но при импорте модуля.

<strong>Административные задачи</strong><br /> Get-SmaLicense и Set-SmaLicense - позволят Вам узнать время до конца пробного периода и конвертировать SMA из пробной в полную версию.<br /> Командлеты Get-SmaRunbookWorkerDeployment и Set-SmaRunbookWorkerDeployment позволяют получать информацию о SMA воркерах и добавить новых воркеров (только первый воркер добавляется в SMA автоматически).<br /> Для поддержания конфигурации SMA воркеров рекомендуется использовать PowerShell DSC, об этом в ближайщее время.