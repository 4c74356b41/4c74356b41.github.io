---
id: 1369
title: 'Дупликация MAC адреса на хосте VMM; Event 16945 источник - MsLbfoSys'
date: 2014-07-14T13:47:35+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post1369
permalink: /post1369
categories:
  - Azure Pack
  - Virtualization and Cloud
tags:
  - Copypaste
  - Guide
  - Virtual Machine Manager
---
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/vmm-00.png" rel="attachment wp-att-5360"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/vmm-00-300x97.png" alt="vmm-00" width="300" height="97" /></a>
  
Недавно заметил подобные ивенты на хостах виртуализации.

Спасибо добрым людям, рассказали что к чему. При создании Hyper-V свича через VMM процесс можно изобразить следующим образом
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/vmm-01.png" rel="attachment wp-att-5363"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/vmm-01-300x87.png" alt="vmm-01" width="300" height="87" /></a>
  
На хосте имеется некоторое количество сетевых карт, Вы создаете свитч через VMM и ставите галочку наследовать настройки от родительской системы
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/vmm-04.png" rel="attachment wp-att-5372"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/vmm-04-300x132.png" alt="vmm-04" width="300" height="132" /></a>
  
Происходит создание свича
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/vmm-02.png" rel="attachment wp-att-5366"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/vmm-02-300x143.png" alt="vmm-02" width="300" height="143" /></a>
  
И собственно то самое "сохранение настроек родительской системы"
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/vmm-03.png" rel="attachment wp-att-5369"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/vmm-03-300x211.png" alt="vmm-03" width="300" height="211" /></a>
  
В результате которого vNIC менеджмент сети получает MAC адрес хоста.

**Workaround:**
  
Помните, что в результате изменений настроек vNIC соединение по сети будет разорвано на непродолжительный период (до нескольких минут)

```
#Получаем MAC пул из VMM
$MACPool = Get-SCMACAddressPool "имя MAC пула" 
#Получаем vNIC хоста
$VMHostNIC = Get-SCVirtualNetworkAdapter -VMHost "FQDN хоста" | ? {$_.PortClassification -match "Hоst Management"}
#Смена MAC адреса для vNIC хоста в VMM
$NewMACAddress = (Grant-SCMACAddress -MACAddressPool $macpool -VirtualNetworkAdapter $VMHostNIC).Address
#Присваиваем MAC адрес адаптеру
$AdapterName = $VMHostNIC.Name
Invoke-Command -ComputerName "FQDN хоста" -ScriptBlock {
       $MgmtNIC = Get-NetAdapter | where-object  {$_.Name -match $USING:AdapterName -and $_.InterfaceDescription -match 'Hyper-V Virtual Ethernet Adapter'}
       $MgmtNIC | Set-NetAdapter -MacAddress $USING:NewMACAddress -confirm:$false
}
```

Runbook для SMA

```
Workflow Set-MgmtvNICMACAddress
{
    param(
    [Parameter(Mandatory=$true)]
    [STRING]$VMMServer,

    [Parameter(Mandatory=$true)]
    [STRING]$VMHostName,

    [Parameter(Mandatory=$false)]
    [STRING]$PortClassification="Host management",

    [Parameter(Mandatory=$false)]
    [STRING]$MACAddressPool="Default MAC address pool"
    )

    $HostMgmtCred = Get-AutomationPSCredential -Name "Host Access Account"
    $VMMMgmtCred = Get-AutomationPSCredential -Name "SCVMM Access Account"

    $NewNICInfo = InlineScript
    {
        $macpool = Get-SCMACAddressPool $USING:MACAddressPool
        $VMHostNIC = Get-SCVirtualNetworkAdapter -VMHost $USING:VMHostName | ? {$_.PortClassification -match "$USING:PortClassification"}
        $NewMACAddress = (Grant-SCMACAddress -MACAddressPool $macpool -VirtualNetworkAdapter $VMHostNIC).Address
        $NICInfo = New-Object -TypeName PSObject -Property @{
            "VMHostNICName" = $VMHostNIC.Name
            "NewMACAddress" = $NewMACAddress
        }
        $NICInfo
    } -PSComputerName $SCVMMServer -PSCredential $VMMMgmtCred

    InlineScript
    {
        $AdapterName = ($USING:NewNICInfo).VMHostNICName
        $NewMACAddress = ($USING:NewNICInfo).NewMACAddress
        $MgmtNIC = Get-NetAdapter | ? {$_.Name -match "$AdapterName" -and $_.InterfaceDescription -match 'Hyper-V Virtual Ethernet Adapter'}
        $MgmtNIC | Set-NetAdapter -MacAddress $NewMACAddress -confirm:$false
    } -PSComputerName $VMHostName -PSCredential $HostMgmtCred
}
```