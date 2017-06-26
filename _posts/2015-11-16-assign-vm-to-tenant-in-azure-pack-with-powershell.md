---
id: 3893
title: Assign VM to Tenant in Azure Pack with PowerShell
date: 2015-11-16T16:14:25+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post3893
permalink: /post3893
categories:
  - Azure Pack
  - Virtualization and Cloud
tags:
  - Guide
  - PowerShell
  - Windows Azure Pack
---
```
#Initialize Variables
$pattern = Read-Host -Prompt "Input Username or part of it"
$VMName = Read-Host -Prompt "Input VM Name"

#Establish Connection to VMM
$vmm = Get-VMMServer msk-vmm-cls.sibintek.ru
$vmmSPF = Get-VMMServer msk-vmm-cls.sibintek.ru -ForOnBehalfOf

#Construct Variables
$tmpRole = Get-SCUserRole -VMMServer $vmm | ? name -like "*$pattern*"
$Owner = ($tmpRole.Name).Split("_") | Select -First 1
$UserRole = $tmpRole.Name
$Role = Get-SCUserRole -Name $UserRole 

#Assign VM to Tenant
$vm | Set-SCVirtualMachine -UserRole $Role
$vm | Set-SCVirtualMachine -OnBehalfOfUser $Role -OnBehalfOfUserRole $role -Owner $Owner
```

I got really bored with assigning random VM's by hand