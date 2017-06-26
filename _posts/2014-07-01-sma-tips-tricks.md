---
id: 930
title: 'SMA - более пристальный взгляд'
date: 2014-07-01T17:23:02+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post930
permalink: /post930
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
Для примера я возьму Runbook изменения IP адреса виртуального адаптера на статический:

```
workflow New-NetworkAdapter
{
# Импортируем параметры  
param([object]$params) 
  
# Соединяемся с VMM, для этого необходимо создать "Connection Asset" с названием "VMM_Connection"
$con = Get-AutomationConnection -Name "Vmm_Connection"
 
$secpasswd = ConvertTo-SecureString $con.Password -AsPlainText -Force
$SMA-crd = New-Object System.Management.Automation.PSCredential ($con.username, $secpasswd)
 
# Работаем с VMM 
InlineScript {
 
    $con=$USING:Con
    $SMA-crd=$USING:SMA-crd
    $params=$USING:params
    
Invoke-Command -ComputerName $con.computername -Credential $SMA-crd -ArgumentList ($params.VMId),$con -ScriptBlock {
 
 param(
    $VMID,
    $con
    )
 
# Проверка работает ли VM, если да - выключаем
$restart = $false
if ((Get-SCVirtualMachine -VMMServer $con.computername -ID $VMID).VirtualMachineState -ne "PowerOff") {
    $restart = $true
    Get-SCVirtualMachine -VMMServer $con.computername -ID $VMID | Stop-SCVirtualMachine -Shutdown 
    }
if ((Get-SCVirtualMachine -VMMServer $con.computername -ID $VMID).VirtualMachineState -ne "PowerOff") {
    $restart = $true
    Get-SCVirtualMachine -VMMServer $con.computername -ID $VMID | Stop-SCVirtualMachine -force
    }
 
# Изменяем MAC на статический на всех адаптерах
Get-SCVirtualMachine -VMMServer $con.computername -ID $VMID | Get-SCVirtualNetworkAdapter | where {$_.MACAddressType -EQ "Dynamic"} | Set-SCVirtualNetworkAdapter -MACAddressType "Static"
 
# Включаем VM
if ($restart -eq "$true") {Get-SCVirtualMachine -VMMServer $con.computername -ID $VMID | Start-SCVirtualMachine } 
 
  }
 }
}
```

Кроме переменной $Params, Вы можете использовать переменные $ResourceOnject и $PSPrivateMetaData.

Для того чтобы при создании адаптера Runbook запустился необходимо создать Runbook с названием "New-NetworkAdapter" и тегом <em>"SPF"</em>. После этого опубликовать его и привязать к событию создания сетевого адаптера.<a href="http://4c74356b41.com/wp-content/uploads/2016/02/sma_new_network_adapter_00.png" rel="attachment wp-att-5335"><img class="alignnone size-medium wp-image-5335" src="http://4c74356b41.com/wp-content/uploads/2016/02/sma_new_network_adapter_00-300x204.png" alt="sma_new_network_adapter_00" width="300" height="204" srcset="http://4c74356b41.com/wp-content/uploads/2016/02/sma_new_network_adapter_00-300x204.png 300w, http://4c74356b41.com/wp-content/uploads/2016/02/sma_new_network_adapter_00.png 684w" sizes="(max-width: 300px) 100vw, 300px" /></a>.

Пример VMM_Connection Asset<br /> <a href="http://4c74356b41.com/wp-content/uploads/2016/02/sma_new_network_adapter_01.png" rel="attachment wp-att-5338"><img class="alignnone size-medium wp-image-5338" src="http://4c74356b41.com/wp-content/uploads/2016/02/sma_new_network_adapter_01-255x300.png" alt="sma_new_network_adapter_01" width="255" height="300" srcset="http://4c74356b41.com/wp-content/uploads/2016/02/sma_new_network_adapter_01-255x300.png 255w, http://4c74356b41.com/wp-content/uploads/2016/02/sma_new_network_adapter_01.png 688w" sizes="(max-width: 255px) 100vw, 255px" /></a>