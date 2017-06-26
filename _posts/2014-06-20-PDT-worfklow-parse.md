---
id: 580
title: 'PDT Парсим Workflow.xml 2.64.2611'
date: 2014-06-20T03:07:53+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post580
permalink: /post580
categories:
  - Azure Pack
  - Virtualization and Cloud
tags:
  - Copypaste
  - Guide
  - PDT
  - Powershell Deployment Toolkit
  - System Center 2012 R2
  - Windows Azure Pack
---
Один добрый человек в интернете распарсил Workflow.xml (версия 2.64.2611) вот этим скриптом:

```
$xml = New-Object -TypeName XML
$xml.Load("путьWorkflow.xml")
#Глобальные переменные
$xml.Installer.Variable
#Компоненты
$xml.Installer.Components.Component | select Name | sort Name
#Переменные компонентов
$xml.Installer.Components.Component | select Name,Variable | sort Name | foreach{Write-Host $_.Name -ForegroundColor Cyan;If($_.PSObject.Properties.Match('Variable').Count){foreach($Var in $_.Variable){Write-Host " – $($Var.Name)=$($Var.Value)"}}}
#Роли, без интеграции
$xml.Installer.Roles.Role | where {$_.Type -ne 'Integration'} | select Name | sort Name | ft -AutoSize
#SQL и переменные для него
$xml.Installer.SQL.SQL | select Version,Variable | sort Version | foreach{Write-Host $_.Version -ForegroundColor Cyan;If($_.PSObject.Properties.Match('Variable').Count){foreach($Var in $_.Variable){Write-Host " – $($Var.Name)=$($Var.Value)"}}}
#Роли которые можно совмещать с VMM:
$xml.Installer.Roles.Role | where {$_.Name -eq 'System Center 2012 R2 Virtual Machine Manager Management Server'} | foreach {$_.Validation.Combinations.Combination}
#Все URL для скачивания, если нет URL – отметить красным
$xml.Installer.Installables.Installable | foreach {If ($_.Download.URL) {Write-Host $_.Name -ForegroundColor Cyan} Else {Write-Host $_.Name -ForegroundColor Red}; foreach ($Link in $_.Download.URL){Write-Host " " $Link}}
#Только компоненты без URL
$xml.Installer.Installables.Installable | foreach {If (! $_.Download.URL) {Write-Host $_.Name -ForegroundColor Red}}
```

Можете повторить его подвиг :)