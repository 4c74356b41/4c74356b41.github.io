---
id: 1037
title: 'SMA - переименовываем Standalone VM'
date: 2014-07-02T14:30:09+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post1037
permalink: /post1037
categories:
  - Azure Pack
  - Virtualization and Cloud
tags:
  - Copypaste
  - Guide
  - Service Management Automation
  - Service Provider Foundation
  - SMA
  - SPF
  - Windows Azure Pack
---
Вы, наверно, замечали, что при разворачивании Standalone VM ей присваиваться случайное имя, чтож используем runbook, чтобы это исправить.

**Что потребуется:**

1. Работающий [SPF](http://4c74356b41.com/post466), [SMA](http://4c74356b41.com/post678) и [WAP](http://4c74356b41.com/post422);
  
2. SPF и SMA доверяющие друг-другу (сертификаты endpoint’ов);
  
3. Пользователь spf-app-pool в группе smaAdmingroup (на веб сервис ролях SMA);
  
4. Готовый ассет для подключения к SPF

(https://spf_endpoint:8090/SC2012R2/VMM/Microsoft.Management.Odata.svc/), пользователь с правами на переименование компьютера в AD и пользователь с правами на доступ к SPF.

```
workflow RenameVM
{    
    param
    (
        
        [Parameter(Mandatory=$true)]
        [string] $vmmJobId,
        
        [Parameter(Mandatory=$true)]
        [object] $params,
        
        [Parameter(Mandatory=$true)]
        [object] $resourceObject
    )
    
    #Объявляем переменные для подключения
    $spfUrl = Get-AutomationVariable -Name "spfUrl"
    $spfCredentials = Get-AutomationPSCredential -Name "spfCredentials"
    $ADCred = Get-AutomationPSCredential -Name "ADCred"
    $stampId = $params.StampId
    $fullUrl = $spfUrl + "Jobs?`$filter=ID eq guid'" + $vmmJobId + "' and StampId eq guid'" + $stampId + "'"
    
    #Получаем имя компьютера и обрабатываем его
    $VMName = $resourceObject.Name
    $initComputerName = $resourceObject.ComputerName
    $compNameSplit = $initComputerName.split('.')
    $ComputerName = $compNameSplit[0]
   
    #Логирование
    Write-Output " "
    Write-Output "SPF URL: $fullUrl"
    Write-Output " "
    Write-Output "Computer Name Initially Set To: $ComputerName"
    Write-Output "Computer Name Will Be Reset To: $VMName"
    Write-Output " "
  
   do {
        Start-Sleep -s 30
        $Output = InlineScript {

            # Создаем ответ для SPF
            [System.Net.ServicePointManager]::ServerCertificateValidationCallback = {$true}
            $request = [System.Net.HttpWebRequest]::Create($Using:fullUrl)
            $request.Credentials = $Using:spfCredentials
            $request.Accept = "application/json"
            $request.Headers.Add("Accept-Charset", "UTF-8")
            $request.ContentType = "application/json"
            $request.Method = "GET"
            $response = $request.GetResponse()
            $requestStream = $response.GetResponseStream()
            $readStream = new-object System.IO.StreamReader $requestStream
            $outputJson = $readStream.ReadToEnd()
            $output = ConvertFrom-Json $outputJson
            $readStream.Close()
            $response.Close()
            $output
        }

        Write-Output "Current Progress: $($output.value.Progress)"
   } 

   while (!$output.value.IsCompleted)
        

   Write-Output "Final Status: $($output.value.Status)"
    
   #Переименовываем
   If (!$ComputerName -or !$VMName ) {

        Write-Output "Computer Name Not Defined, No Change Will Occur."

   }
   else {

        Inlinescript {

            $i = 1
            $newComputerName = $Using:VMName 
        
            Do {
                $checkComp = Get-ADComputer -LDAPFilter "(Name=$newComputerName)"
                if (!$checkComp) {              
                    Rename-Computer -ComputerName $Using:ComputerName -NewName $newComputerName -DomainCredential $Using:ADCred -Restart
                }
                else {  
                    $newComputerName  = $newComputerName  + $i
                    $i ++
                }
            }
            until ((!$checkComp))

        }
    }
}
```

Строки:
  
6-13 = инициализация данных;
  
19 = полечение пользовательских данных для подключения к AD;
  
24-27 = переделываем значение ComputerName.Domain в ComputerName
  
30-35 = логирование
  
37-64 = этот кусок взят из Sample-Using-VMCloud-Automation, этот код используется для запрашивания статуса задания в VMM и позволяет определить когда оно закончилось и приступить к следующему заданию;
  
67-68 = проверка;
  
72-89 = переименовываем VM, перед переименовыванием проверяем есть ли такая машина в AD. Если есть то добавляем единичку и проверяем снова, и снова и снова.
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/sma-rename-vm.png" rel="attachment wp-att-5349"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/sma-rename-vm-300x203.png" alt="sma-rename-vm" width="300" height="203" /></a>
  
Так как мы используем триггер VMM Virtual Machine, роли виртуальных машин не будут затронуты этим runbook'ом.