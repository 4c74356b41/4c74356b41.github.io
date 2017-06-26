---
id: 3081
title: Как снести агента VMM с хоста Hyper-V даже если агент этого сильно не хочет
date: 2015-08-25T15:54:28+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post3081
permalink: /post3081
categories:
  - Virtualization and Cloud
tags:
  - Copypaste
  - Virtual Machine Manager
---
В интернетах много написано про то как снести агента VMM с core сервера:
  
Get-WMIObject -Class Win32_product или Regedit > HKLM > Software > Microsoft > Windows > CurrentVersion > Uninstall, там находим GUID MSI пакета и далее msiexec /x "{GUID}" или wmic get product name "Имя продукта" delete&#8230; И это все прекрасно. Когда эти записи в реестреWMI есть. А если их нет, а агент есть? 🙂

CopyPaste моего [поста](https://social.technet.microsoft.com/Forums/en-US/aa122e7f-ef6c-44ee-aa23-243f65b20eb4/unable-to-remove-vmm-agent-from-hyperv-host) на social.Technet

1. We imported registry folders from the host where agent was present and working normally  
```
HKEY\_LOCAL\_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Installer\Folders
  
HKEY\_LOCAL\_MACHINE\SOFTWARE\Classes\Installer\Products\GUID
  
HKEY\_LOCAL\_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Installer\UserData\S-1-5-18\Products\GUID
  
HKEY\_CLASSES\_ROOT\Installer\Products\GUID
  
HKEY\_LOCAL\_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{EE6A3726-D270-4AD1-9EFD-CFD982D2313C}
  
HKEY\_LOCAL\_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Perflib\_V2Providers\{ab8e1320-965a-4cf9-9c07-fe25378c2a23}
```
2. We changed build number to the one from UR6 (something.8002 or whatever, you can google it). In description and in hex (version string) and path to msi under C:\Windows\Installer. You can figure out the MSI you need by size, for example.

3. The program was still missing in Add\Remove but we were able to remove program with https://support.microsoft.com/mats/program\_install\_and_uninstall (don't forget to shutdown SCVMMAgent service before doing so).

4. We used the SC utility to delete VMM Agent service (sc delete SCVMMAgent)

5. Renamed\Deleted VMM Agent folder in program files

6. We manually installed agent.

7. Reassociated host from VMM console