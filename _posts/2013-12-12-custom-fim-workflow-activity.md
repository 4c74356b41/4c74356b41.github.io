---
id: 193
title: Установка Custom FIM WorkFlow Activity
date: 2013-12-12T15:44:14+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post193
permalink: /post193
categories:
  - MIM
tags:
  - FIM
  - Guide
---
Для начала нам понадобяться:

[FIM Powershell Workflow Activity (v2.1)](http://fimpowershellwf.codeplex.com/)
  
Activity Library (FimExtensions.FimActivityLibrary.dll)
  
Installation Script (InstallFimPowerShellWF.ps1 - данный скрипт сохраняет dll файл скачанный нами в GAC Assembly, добавляет ActivityInformationConfiguration в Fim Service, создает источник EventLog "PowerShellActivity")
  
Example Scripts (Create-FimServiceAccountAsFimPerson.ps1 - данный скрипт находит Fim Service, находит пользователя, от имени которого запускается сервис, получает ObjectSID данного пользователя из Active Directory, создает данного пользователя на портале FIM и добавляет его в Set "Administrators" Update-FimServiceConfigFile.ps1 - исправляет конфигурацию resourceManagementServiceBaseAddress и добавляет записи System.Diagnostics для Fim PowerShell WorkFlow)

[FIM Powershell Module (v2.1)](http://fimpowershellmodule.codeplex.com/)
  
FIM Service module (FimPowerShellModule.psm1)
  
FIM Synchronization module (FimSyncPowerShellModule.psm1)
  
FIM Synchronization Configuration Viewer module (Get-FimSyncConfiguration.psm1)

После скачивания файлов их необходимо разблокировать для использования (правая кнопка мыши на файле - unblock)

Запускаем PowerShell от имени администратора, переходим в каталог где лежат все эти файлы и вводим:

Set-ExecutionPolicy –ExecutionPolicy Unrestricted
  
Import-Module .FimPowerShellModule.psm1
  
.Install-FimPowerShellWF.ps1
  
.Create-FimServiceAccountAsFimPerson.ps1 (необходимо только в случае если Вашего сервисного аккаунта FIM нет на портале FIM)
  
.Update-FimServiceConfigFile.ps1

После этого делаем IISReset + рестарт сервиса Fim Service или Reset 😉 Проверяем является-ли сервисный аккаунт FIM администратором на портале, если нет - добавляем его.

Как проверить: создаем Set, Action WorkFlow и MPR для проверки; в Action Workflow создаем Powershell WorkFlow Activity приблизительно следующего содержания:

$test = "It works!"
  
$test | Out-File С:путь\_к\_файлу

Добавляем пользователя в Set и наблюдаем "It works!" в только что созданном файле.