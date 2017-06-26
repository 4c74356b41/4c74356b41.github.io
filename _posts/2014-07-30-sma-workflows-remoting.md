---
id: 1428
title: SMA Workflows и Remoting, работа с переменными
date: 2014-07-30T19:27:47+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post1428
permalink: /post1428
categories:
  - Azure Pack
  - Virtualization and Cloud
tags:
  - Copypaste
  - Guide
  - Service Management Automation
  - SMA
  - Windows Azure Pack
---
[Репост](http://www.miru.ch/sma-workflows-and-remoting-how-to-deal-with-variable-scoping/)  

SMA использует PowerShell Workflows, это накладывает некоторые ограничения, например при обращении к переменным или невозможность использования Invoke-Command. Для вызова команд недоступных в PowerShell Workflows можно использовать InlineScript. При этом все что "внутри" InlineScript выполняется "отдельно", некое подобие sandbox'а.

```
Workflow Get-VMReplicaStatus
{
    param(
    [Paramater(mandatory=$true)]
    $VMHost,
    [Paramater(mandatory=$true)]
    $VMName
    )
    InlineScript
    {
       Invoke-Command -ComputerName $USING:VMHost -ScriptBlock {Get-VMReplication -VMName $USING:VMName}
    }
}
```

В данном случае переменная VMName не будет доступна в ScriptBlock'е, т.к. $USING:VMName используется для передачи переменной из PowerShell Workflow в InlineScript. Решением будет переобозначить переменную в InlineScript'е.

```
Workflow Get-VMReplicaStatus
{
    param(
    [Paramater(mandatory=$true)]
    $VMHost,
    [Paramater(mandatory=$true)]
    $VMName
    )
    InlineScript
    {
        $VMName = $USING:VMName
        Invoke-Command -ComputerName $USING:VMHost -ScriptBlock {param($VMName) Get-VMReplication -VMName $VMName} -ArgumentList $VMName
    }
}
```

Однако, Best Practice - передавать переменные как аргументы для InlineScript.

```
Workflow Get-VMReplicaStatus
{
    param(
    [Paramater(mandatory=$true)]
    $VMHost,
    [Paramater(mandatory=$true)]
    $VMName
    )
    InlineScript
    {
        Get-VMReplication $USING:VMName
    } -PSComputerName $VMHost
}
```