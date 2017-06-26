---
id: 1345
title: Используем Desired State Configuration для поддержания конфигурации SMA Worker'ов
date: 2014-07-10T23:33:44+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post1345
permalink: /post1345
categories:
  - Azure Pack
  - Virtualization and Cloud
tags:
  - Copypaste
  - DSC
  - Guide
  - PowerShell
  - Service Management Automation
  - SMA
  - Windows Azure Pack
---
Если Вы используете SMA Вы должны знать что при запуске задания SMA его "подхватывает" случайный свободный worker. Таким образом, Вам необходимо поддерживать идентичную конфигурацию worker'ов, чтобы исключить ошибки при исполнении заданий. Можно, конечно, делать это "руками", но есть способ лучше - PowerShell Desired State Configuration (далее DSC).

**Что нам потребуется:**
  
1. SMA Runbook, который будет запускаться для проверки конфигурации;
  
2. Переменная для подключения к SMA (SMA Web Service Endpoint);
  
3. Учетная запись с правами на изменение конфигурации worker'ов;
  
4. Сетевая папка для хранения пакетов, файлов, модулей PowerShell.

**Описание сценария**
  
<img src="http://www.miru.ch/wp-content/uploads/2014/02/022814_1327_UsingDSCtok1.png" alt="DSC-sma-00" width="530" height="495" />
  
1. Сетевая папка со всеми необходимыми файлами (должна быть доступна для чтения и исполнения всем компьютерным аккаунтам worker'ов);
  
2. После того как Вы перенесли туда необходимые файлы нужно будет подогнать скрипт и структуру папок;
  
3. Сервисная учетная запись runbook web service должна быть администратором на всех worker'ах;
  
4. Создать runbook в WAP с названием "Update-SMARunbookWorkers" и скопировать в него скрипт (будет ниже);
  
5. Подогнать переменные "SMAWebServiceEndpoint" и "SMAAdmin" в скрипте;
  
6. Запустить runbook.

```
workflow Update-SMARunbookWorkers
{
    Runbook Name: Update-SMARunbookWorkers
    Runbook Type: Process 
    Runbook Tags: Type:Process, Proj:Update Runbook Workers, DSC 
    Runbook Description: Поддержание DSC на всех runbook worker'ах  

    param(
        [Parameter(Mandatory=$true)]
        [SWITCH]$RebootWorkers
    )

    #Прекращение исполнения при ошибке
    $ErrorActionPreference = "stop"

    #Получаем переменные
    $SMAWebServiceEndpoint = Get-AutomationVariable -Name SMAWebServiceEndpoint

    #Работаем с учетной записью
    $PSUserCred = Get-AutomationPSCredential -Name SMAAdmin

    #Указываем каталог для MOF файлов
    $DSCConfigPath = "C:DSCConfigsUpdateRBConfig"

    InlineScript
    {
        Configuration UpdateRBConfig 
        {
            param (
            [Parameter(Mandatory=$true)]
            [ValidateNotNullOrEmpty()]
            [String[]]$NodeName,

            [Parameter(Mandatory=$false)]
            [ValidateNotNullOrEmpty()]
            [String]$ModuleSourcePath = "ssma01DSCResourcesModules",

            [Parameter(Mandatory=$false)]
            [ValidateNotNullOrEmpty()]
            [String]$ModulePath="$env:ProgramFilesWindowsPowerShellModules"
            )

            Node $NodeName
            {
                #Powershell Modules
                File PSModules 
                {
                    SourcePath = $ModuleSourcePath
                    DestinationPath = $ModulePath
                    Recurse = $true
                    Type = "Directory"
                    CheckSum = "SHA-256"
                }

                #SQL 2012 CLR Types
                Package SQL2K12CLRTypes
                {
                    Name = "Microsoft System CLR Types for SQL Server 2012 (x64)"
                    Path = "ssma01DSCResourcesSWPackagesSQLCLR2012SQLSysClrTypes.msi"
                    ProductId = "F1949145-EB64-4DE7-9D81-E6D27937146C"
                    Ensure = "Present"
                    ReturnCode = 0
                }

                #Report Viewer 2010
                Package MSReportViewer
                {
                    Name = "Microsoft Report Viewer 2012 Runtime"
                    Path = "ssma01DSCResourcesSWPackagesReportViewerReportViewer.msi"
                    ProductId = "421B88F8-D7C9-44CB-8B73-166D65B18DCC"
                    Ensure = "Present"
                    DependsOn = "[Package]SQL2K12CLRTypes"
                    ReturnCode = 0
                }

                #Ops Manager Console
                Package OpsMgrConsole
                {
                    Name = "System Center Operations Manager 2012 Console"
                    Path = "ssma01DSCResourcesSWPackagesOpsMgrSetup.exe"
                    ProductId = "041C3416-87CE-4B02-918E-6FDC95F241D3"
                    Arguments = "/silent /install /components:OMConsole /EnableErrorReporting:Never /SendCEIPReports:0 /UseMicrosoftUpdate:1 /AcceptEndUserLicenseAgreement:1"
                    Ensure = "Present"
                    DependsOn = "[Package]MSReportViewer"
                    ReturnCode = 0
                }

                #SCVMM Console
                Package VMMConsole
                {
                    Name = "Microsoft System Center Virtual Machine Manager Administrator Console (x64)"
                    Path = "ssma01DSCResourcesSWPackagesSCVMMsetup.exe"
                    ProductId = "CDFB453F-5FA4-4884-B282-F46BDFC06051"
                    Arguments = "/client /i /IACCEPTSCEULA /f ssma01DSCResourcesSWPackagesSCVMMVMClient.ini"
                    Ensure = "Present"
                    ReturnCode = 0
                }
            }
        }

        #Получаем имена всех runbook worker'ов
        $SMARunbookNodes = (Get-SmaRunbookWorkerDeployment -WebServiceEndpoint $USING:SMAWebServiceEndpoint -Credential $USING:psusercred).ComputerName
        Write-OutPut "INFO: Создаем конфигурацию для SMA Runbook сервер: $SMARunbookNodes"

        #Создаем MOF файлы
        UpdateRBConfig -NodeName $SMARunbookNodes -OutputPath $USING:DSCConfigPath

        #Запускаем DSC
        Write-OutPut "INFO: Запускаем процесс DSC"
        Start-DscConfiguration -Path $USING:DSCConfigPath -Force -wait -verbose
        Write-OutPut "INFO: DSC успешно, Лог можно посмотреть в задании"

        #Перезагрузка, если необходима 
        If ($Using:RebootWorkers)
        {
            Write-OutPut "INFO: Перезагружаем SMA Runbook сервер: $SMARunbookNodes"
            $SMARunbookNodes | Restart-Computer -force
        }
    }
    Write-OutPut "INFO: Runbook выполнен успешно. Лог можно посмотреть в задании"
}
```
