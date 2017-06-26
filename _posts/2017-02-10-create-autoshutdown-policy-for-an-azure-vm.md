---
id: 5698
title: Create auto-shutdown policy for an Azure VM with Powershell
date: 2017-02-10T23:07:24+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post5698
permalink: /post5698
categories:
  - Azure
tags:
  - Azure
  - PowerShell
---
Recently Microsoft <a href="https://azure.microsoft.com/en-us/blog/announcing-auto-shutdown-for-vms-using-azure-resource-manager/" target="_blank">announced</a> the ability to create auto-shutdown policies for ARM VM's, but there's no capacity to automate this, or is there?

Lets create a following hashtable in Powershell:

```
$properties = @{}
$properties.Add('status', 'Enabled')
$properties.Add('taskType', 'ComputeVmShutdownTask')
$properties.Add('dailyRecurrence', @{'time'= 1600})
$properties.Add('timeZoneId', 'Belarus Standard Time') # _case_sensitive_, use this to list time zones ([System.TimeZoneInfo]::GetSystemTimeZones()).id
$properties.Add('notificationSettings', @{status='Disabled'; timeInMinutes=15})
$properties.Add('targetResourceId', '/subscriptions/{sub_guid}/resourceGroups/{rg_name}/providers/Microsoft.Compute/virtualMachines/{vm_name}')

New-AzureRmResource -Location {location} -ResourceId /subscriptions/{sub_guid}/resourceGroups/{rg_name}/providers/microsoft.devtestlab/schedules/shutdown-computevm-{vm_name} -Properties $properties
```