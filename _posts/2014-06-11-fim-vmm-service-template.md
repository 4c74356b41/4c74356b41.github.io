---
id: 428
title: FIM 2010 R2 SP1 с использованием VMM Service Templates
date: 2014-06-11T14:06:54+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post428
permalink: /post428
categories:
  - MIM
  - Virtualization and Cloud
tags:
  - FIM
  - Guide
  - System Center 2012 R2
  - Virtual Machine Manager
---
Долгое время мне было лень готовить скрипты для автоматического разворачивания FIM, но тут я занялся VMM'ом и оправдания кончились. Посему, приступим.

**Нам потребуется:**
  
1. VMM с минимальными настройками;
  
2. 2 sysprep образа Windows Server 2012 R2 (на виртуальных машинах первого поколения), один с sysprep SQL сервером, один голый (но с .NET FX 3.5);
  
3. Распакованные дистрибутивы Sharepoint Foundation 2010 SP2, и FIM 2010 R2 SP1 на сетевой шаре.

Как делать SQL разворачивание я расскажу в [следующем посте](http://4c74356b41.com/post478), на данный момент сфокусируемся на FIM'е и VMM'е. Перед тем как приступить создайте на Library сервере VMM 2 папки FIM 2010 R2 и Sharepont Foindation 2010 SP2, в них создайте подпапки Synchronization\_Service.cr, Service\_Portal.cr для FIM и Install.cr, Configure.cr для Sharepoint.
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/folders.jpg" rel="attachment wp-att-4781"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/folders.jpg" alt="folders" width="195" height="208" /></a>
  
Потом мы положим в них скрипты.

1. Создаем 2х тировый шаблон сервиса, даем ему имя и версию;
  
2. Выбираем в качестве машины первого тира шаблон машины с Sysprep SQL, для машины второго типа выбираем шаблон машины без SQL;
  
3. Настраиваем железо под свои нужды;
  
4. Настраиваем ОС под свои нужды, в качестве имени машины первого тира указываем @FirstTier@, и @SecondTier@ для второго тира (желательно указать все роли-зависимости для Sharepoint Foundation в настройках ОС машины второго тира);
  
5. Для машины первого тира указываем развертывание SQL из sysprep'а;
  
6. Для машины первого тира создаем пункт установки приложения, даем ему имя и заполняем остальные поля следующим образом;
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/FSS.jpg" rel="attachment wp-att-4783"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/FSS-300x259.jpg" alt="Fim Synch Service" width="300" height="259" /></a>

7. На этом настройка машины первого тира закончена. И мы приступаем к настройке машины второго тира. Для неё не нужно настраивать раздел SQL Server Configuration, но раздел Application Configuration настроить сложнее;
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/pre-install.jpg" rel="attachment wp-att-4813"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/pre-install-300x260.jpg" alt="pre-install" width="300" height="260" /></a>

<a href="http://4c74356b41.com/wp-content/uploads/2016/02/Configure.jpg" rel="attachment wp-att-4769"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/Configure-300x262.jpg" alt="Configure Sharepoint" width="300" height="262" /></a>

<a href="http://4c74356b41.com/wp-content/uploads/2016/02/post-install.jpg" rel="attachment wp-att-4809"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/post-install-300x261.jpg" alt="post-install" width="300" height="261" /></a>
  
9. Создаем скрипты для разворачивания;
  
Synchronization_Service.cr Install.cmd:

```net start sqlserveragent
sc config sqlserveragent start= auto (Установка параметра запуск на "Автоматический" и запуск сервиса "SQL Agent")
msiexec /q /i "путь\Synchronization Service.msi" ACCEPT_EULA=1 /l*v c:NameOfLogFile1.txt STORESERVER=%1 SQLDB="FIMSynchronization" SERVICEACCOUNT="сервис_аккаунт" SERVICEPASSWORD="!Q2w3e4r" FIREWALL_CONF=1
```

Service_Portal.cr Install.cmd: (аккаунты сервиса и агента не должны совпадать)

```msiexec /q /i "путь\Service and Portal.msi" ACCEPT_EULA=1 ADDLOCAL=CommonServices,WebPortals SQMOPTINSETTING=0 SQLSERVER_SERVER=%1 SQLSERVER_DATABASE=FIMService EXISTINGDATABASE=0 MAIL_SERVER=ex.demo.local MAIL_SERVER_IS_EXCHANGE=1 POLL_EXCHANGE_ENABLED=1 SERVICE_ACCOUNT_NAME="сервис_аккаунт" SERVICE_ACCOUNT_PASSWORD="!Q2w3e4r" SERVICE_ACCOUNT_DOMAIN=demo.local SERVICE_ACCOUNT_EMAIL=fim@demo.local SYNCHRONIZATION_SERVER=%1 SYNCHRONIZATION_SERVER_ACCOUNT="demo\аккаунт_менеджмент_агента" SERVICEADDRESS=%2 SHAREPOINT_URL=http://%2 REGISTRATION_PORTAL_URL=https://pwd.demo.local FIREWALL_CONF=1 SHAREPOINTUSERS_CONF=1 REQUIRE_REGISTRATION_INFO=1 /L*v C:fimservicelog.txt
```

SPF\_Install.cr spf\_install.cmd: (частично раскрыто в другом посте http://4c74356b41.com/post189)

```путь\PrerequisiteInstaller.exe -unattended
путь\setup.exe /config
путь\Files\Setup\FarmSilentconfig.xml
```

Пример Config.xml файла:

```&lt;Configuration&gt;
    &lt;Package Id="sts"&gt;
        &lt;Setting Id="SETUPTYPE" Value="CLEAN_INSTALL"/&gt;
    &lt;/Package&gt;
 
    &lt;Logging Type="verbose" Path="%temp%" Template="Microsoft SharePoint Foundation 2010 Setup *.log"/&gt;
    &lt;Setting Id="SERVERROLE" Value="APPLICATION"/&gt;
    &lt;Setting Id="UsingUIInstallMode" Value="0"/&gt;
    &lt;Display Level="none" CompletionNotice="no" AcceptEula="Yes" NoCancel="No" SuppressModal="Yes"/&gt;
    &lt;Setting Id="SETUP_REBOOT" Value="Never" /&gt;
&lt;/Configuration&gt;```

SPF\_Configure.cr spf\_configure.cmd:

```@echo off
@powershell -Version 2 -NonInteractive -NoProfile -ExecutionPolicy Unrestricted -Command "& {.spf_configure.ps1 %1 %2; exit $LastExitCode }"
exit /B %errorlevel%
```

SPF\_Configure.cr spf\_configure.ps1:

```#   Pass Variables   #
$1=$args[0]
$2=$args[1]

#    Import SP powershell module    #
Add-PsSnapin Microsoft.SharePoint.PowerShell

#    Credentials    #
$username = "demo\пользователь" (данный параметр, как и любой другой в скрипте, тоже можно передавать динамически, для этого необходимо будет сделать еще одну переменную, и инициализировать её в скрипте)
$password = "!Q2w3e4r"
$credential = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $username,(ConvertTo-SecureString -String $password -AsPlainText -Force)

#    Configure SP database, services and central site    #
$passphrase = convertto-securestring "!Q2w3e4r" -asplaintext -force
New-SPConfigurationDatabase -DatabaseName SP_CFG -DatabaseServer $1 -AdministrationContentDatabaseName SP_AC -Passphrase $passphrase -FarmCredentials $credential
Install-SPHelpCollection -All
Initialize-SPResourceSecurity
Install-SPService
Install-SPFeature -AllExistingFeatures
New-SPCentralAdministration -Port 1026 -WindowsAuthProvider "NTLM"
Install-SPApplicationContent

#    Create Web App and Site Collection    #
New-SPWebApplication -ApplicationPool FimPortal -Name FimPortal -ApplicationPoolAccount demoпользователь
New-SPSite -URL http://$2/ -OwnerAlias demoпользователь -Name FimPortal -Template STS#1
```

10. Сохраняем. Все готово.

Если использовать немного фантазии можно и NLB настроить для порталов сброса пароля и ферму Sharepoint 😉