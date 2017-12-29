---
id: 5777
title: Find all VMs that require maintenance and perform maintenance on them
date: 2017-12-29T11:40:00+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post5777
permalink: /post5777
categories:
  - Azure
  - Powershell
---

Howdy,

I needed to perform maintenance on a bunch of VMs across many subs (mostly dev resource groups).
So I could just perform maintenance and not worry about breaking things.

Here's the core of the script:
```
$rg = '%rg_name%'
$vms = get-azurermvm -ResourceGroupName $rg -Status
$vms.Where({$PSItem.MaintenanceRedeployStatus.IsCustomerInitiatedMaintenanceAllowed -eq 'true'}) |  ForEach-Object {
    Restart-AzureRmVM -PerformMaintenance -Name $PSItem.Name -ResourceGroupName $rg -AsJob
}
```

I think the script itself is pretty self explanatory. Additional reading [here](https://docs.microsoft.com/en-us/azure/virtual-machines/windows/maintenance-notifications).  
So this whole blog post is mostly about pointing out the `-AsJob` switch. As without it each vm takes like 15-20 minutes to complete
and if you have hundreds of them there is chance you dont want to wait days.

You could obviously wrap a couple of other loops around it, like go through resource groups or go through subs:
```
Get-AzureRMSubscription | ForEach-Object { 
  Select-AzureRmSubscription -SubscriptionName %sub_name%
  Get-AzureRmResourceGroup | ForEach-Object {
    $rg = $_.Name
    $vms = get-azurermvm -ResourceGroupName $rg -Status
    $vms.Where({$PSItem.MaintenanceRedeployStatus.IsCustomerInitiatedMaintenanceAllowed -eq 'true'}) |  ForEach-Object {
      Restart-AzureRmVM -PerformMaintenance -Name $PSItem.Name -ResourceGroupName $rg -AsJob
    }
  }
}
```
