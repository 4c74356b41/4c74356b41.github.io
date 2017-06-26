---
id: 1408
title: '"An error occurred while retrieving the list of Virtual Machine Roles" ошибка в Windows Azure Pack'
date: 2014-07-24T22:41:52+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post1408
permalink: /post1408
categories:
  - Azure Pack
tags:
  - Copypaste
  - Service Provider Foundation
  - SPF
  - Virtual Machine Manager
  - Windows Azure Pack
---
Лог Microsoft-WindowsAzurePack-MgmtSvc-TenantSite содержит подобную ошибку:  
```
Log Name: Microsoft-WindowsAzurePack-MgmtSvc-TenantSite
EventID: 220
Level: Warning
Description: “subscriptionId”>{00000000-0000-0000-0000-000000000000}
System.AggregateException: One or more errors occurred. —>
System.NullReferenceException: Object reference not set to an instance of an object. at
Microsoft.WindowsAzure.Server.VM.TenantExtension.Controllers.VMController.
«ListVMRoles>b__2a8>d__2ae.MoveNext() —
End of stack trace from previous location where exception was thrown — at
System.Runtime.CompilerServices.TaskAwaiter.ThrowForNonSuccess(Task task) at
System.Runtime.CompilerServices.TaskAwaiter.HandleNonSuccessAndDebuggerNotification(Task task) at
Microsoft.WindowsAzure.Server.VM.TenantExtension.Controllers.VMController.d__2b3.MoveNext()
— End of stack trace from previous location where exception was thrown —
at System.Runtime.CompilerServices.TaskAwaiter.ThrowForNonSuccess(Task task)
at System.Runtime.CompilerServices.TaskAwaiter.HandleNonSuccessAndDebuggerNotification(Task task)
at System.Runtime.CompilerServices.TaskAwaiter1.GetResult()
at Microsoft.WindowsAzure.Server.VM.TenantExtension.Controllers.VMController.d__fa.MoveNext()
— End of inner exception stack trace —
—> (Inner Exception #0)
System.NullReferenceException: Object reference not set to an instance of an object.
at Microsoft.WindowsAzure.Server.VM.TenantExtension.Controllers.VMController.«ListVMRoles>b__2a8>d__2ae.MoveNext()
— End of stack trace from previous location where exception was thrown —
at System.Runtime.CompilerServices.TaskAwaiter.ThrowForNonSuccess(Task task)
at System.Runtime.CompilerServices.TaskAwaiter.HandleNonSuccessAndDebuggerNotification(Task task)
at Microsoft.WindowsAzure.Server.VM.TenantExtension.Controllers.VMController.d__2b3.MoveNext()
— End of stack trace from previous location where exception was thrown —
at System.Runtime.CompilerServices.TaskAwaiter.ThrowForNonSuccess(Task task)
at System.Runtime.CompilerServices.TaskAwaiter.HandleNonSuccessAndDebuggerNotification(Task task)
at System.Runtime.CompilerServices.TaskAwaiter`1.GetResult()
at Microsoft.WindowsAzure.Server.VM.TenantExtension.Controllers.VMController.d__fa.MoveNext()
<—</Data>
```

Означает что у Вас не синхронизированы аккаунты для ресурс провайдеров в базе данных WAP.

**Синхронизируем**  

```
$rp = Get-MgmtSvcResourceProviderConfiguration -Name 'systemcenter' -DecryptPassword
$rp.AdminEndpoint.AuthenticationPassword = 
$rp.AdminEndpoint.AuthenticationUsername = 
Add-MgmtSvcResourceProviderConfiguration -ResourceProvider $rp -Force
```