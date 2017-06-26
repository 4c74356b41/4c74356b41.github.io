---
id: 678
title: Регистрация SMA в Windows Azure Pack
date: 2014-06-23T17:13:27+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post678
permalink: /post678
categories:
  - Azure Pack
  - Virtualization and Cloud
tags:
  - Guide
  - Service Management Automation
  - SMA
  - WAPack Express
  - Windows Azure Pack
---
В продолжении поста об [установке SMA](http://4c74356b41.com/post532) мы подключим SMA к WAP и попробуем разобраться с базовым функционалом.

Регистрация endpoint'а SMA в WAP аналогична регистрации [SPF в WAP](http://4c74356b41.com/post466). С той лишь разницей что регистрацию можно проводить в закладках VM Clouds или Automation.
  
Для регистрации Вам потребуется указать endpoint вида "https://имя\_web\_services\_хоста\_SMA:9090/" и пользователя, который обладает правами на управление SMA.
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/sma_register_011.png" rel="attachment wp-att-4875"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/sma_register_011-300x141.png" alt="sma_register_011" width="300" height="141" /></a>

<a href="http://4c74356b41.com/wp-content/uploads/2016/02/sma_register1.png" rel="attachment wp-att-4880"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/sma_register1-300x204.png" alt="sma_register1" width="300" height="204" /></a>

После того как Вы зарегистрируете SMA, Вы сможете полноценно работать с вкладкой Automation.

<a href="http://4c74356b41.com/wp-content/uploads/2016/02/sma_basic.jpg" rel="attachment wp-att-4857"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/sma_basic-300x225.jpg" alt="sma_basic" width="300" height="225" /></a>.

На данном dashboard'е Вы можете просмотреть всю основную информацию о runbook'ах и заданиях. Используя пиктограммы над графиком Вы можете фильтровать отображаемую на графике информацию. По клику на runbook Вам откроется более детальный dashboard по конкретному runbook'у.
  
В закладке Assets находятся все ваши "активы". Модули, которые вы импортировали в SMA, переменные, учетные данные и настройки соединений. Все это можно интерактивно использовать в своих runbook'ах.

Создание и редактирование runbook'а
  
Создать новый runbook можно из меню создания нового объекта в левом нижнем углу и указания названия, описания и тега runbook'а.
  
После это необходимо открыть dashboard созданного runbook'а и выбрать вкладку "Author". Для редактирования существующего runbook'а необходимо снова будет пройти во вкладку "Author" runbook'а, который необходимо редактировать.
  
Для связывания runbook'а с определенным событием в WAP необходимо открыть VM Clouds далее во пройти во вкладку Automation и связать runbook с событием. Для привязки runbook'ов к событиям необходимо назначить runbook'у тэг "SPF". Например, для привязки runbook'а к созданию роли виртуальной машины необходимо указать следующую информацию при добавлении объекта автоматизации.

<a href="http://4c74356b41.com/wp-content/uploads/2016/02/sma-bind.jpg" rel="attachment wp-att-4886"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/sma-bind-300x199.jpg" alt="sma-bind" width="300" height="199" /></a>

Для теста можно создать ранбук приблизительно следующего содержания:

workflow Test-Runbook
  
{
  
$a = Get-Date
  
Write-Output "Ранбук запущен при создании виртуальной машины из галереи в $a"
  
}

При срабатывании этого ранбука он должен будет "вернуть" в SMA сообщение и его можно будет просмотреть в подробностях задания.

<a href="http://4c74356b41.com/wp-content/uploads/2016/02/sma-details.jpg" rel="attachment wp-att-4889"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/sma-details-300x246.jpg" alt="sma-details" width="300" height="246" /></a>

И в открывшемся экране в самом низу посмотреть результат.

<a href="http://4c74356b41.com/wp-content/uploads/2016/02/sma-output.jpg" rel="attachment wp-att-4893"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/sma-output-300x30.jpg" alt="sma-output" width="300" height="30" /></a>

Более детальное рассмотрение различных вариантов использования SMA в ближайщее время.

Troubleshooting
  
Вы можете столкнуться с "забавной" проблемой, когда у Вас успешно регистрируется endpoint в WAP, но в SPF нет. Об этом Вы можете "узнать" зайдя в закладку Automation, раздела VM Clouds и увидеть что у Вас не зарегистрирован SMA, хотя закладка Automation убеждает Вас что на самом деле SMA зарегистрирован.
  
Вы можете удалить регистрацию SMA из WAP для того, чтобы повторить регистрацию.

```
$Credential = Get-Credential
$Token = Get-MgmtSvcToken -Type Windows -AuthenticationSite https://yourauthenticationsite:30072 -ClientRealm http://azureservices/AdminSite -User $Credential -DisableCertificateValidation
Get-MgmtSvcResourceProvider -AdminUri "https://localhost:30004" -Token $Token -DisableCertificateValidation -name "Automation"
Remove-MgmtSvcResourceProvider -AdminUri "https://localhost:30004" -Token $Token -DisableCertificateValidation -Name "Automation" -InstanceId "Инстанс_ID_из_Get-MgmtSvcResourceProvider"
```

После этого Вы сможете снова зарегистрировать SMA в WAP. Проблема в том что ошибка не исчезнет. 😉

```
Import-Module SPFAdmin
Get-SCSpfStamp | fl
$Stamp = Get-SCSpfStamp -Name "имя_Stamp_vmm"
New-SCSpfServer -Name "IaasAutomation" "ServerType None -Stamps $Stamp
$srv = Get-SCSpfServer -Name "IaasAutomation"
New-SCSpfSetting -Name EndpointURL -SettingType EndpointconnectionString -Value "https://SMAhostname:9090/" -Server $srv
```

С помощью этих команд Вы создадите запись SMA в базе SPF.

Кроме того, Вам необходимо добавить учетную запись spf-app-pool в локальную группу smaAdminGroup на сервере SMA<a href="http://4c74356b41.com/wp-content/uploads/2016/02/smaadmingroup.png" rel="attachment wp-att-4883"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/smaadmingroup-300x69.png" alt="smaadmingroup" width="300" height="69" /></a>