---
id: 1357
title: Описание Desired State Configuration
date: 2014-07-10T23:43:47+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post1357
permalink: /post1357
categories:
  - random
tags:
  - DSC
  - PowerShell
---
**Описание DSC**
  
![DSC-basic-00](http://blogs.technet.com/cfs-file.ashx/__key/communityserver-blogs-components-weblogfiles/00-00-00-85-24-metablogapi/4454.image_5F00_thumb_5F00_20FA899E.png)
  
Жизненный цикл DSC можно условно разделить на три фазы: создание, стейджинг (я отказываюсь придумывать русский аналог) и внесение изменений.

Создание - процесс создание файлов конфигурации DSC. Вы можете использовать различные утилиты для этого (хоть notepad). ISE прекрасно подходит для этого упражнения.
  
Стейджинг - процесс подготовки DSC к работе. В случае Pull модели взаимодействия, целевая система связаывается с DSC сервером и передает ему уникальный идентификатор, а в ответ получает список провайдеров, в случае расхождения скачивает и устанавливает их. В Push случае сервер DSC сам устанавливает соединение с целевой системой и передает данные. В этом случае Вы должны установить провайдеры (“%SYSTEMROOT%System32WindowsPowerShellv1.0ModulesPSDesiredStateConfigurationPSProviders”).
  
Внесение изменений - Фаза внесения изменений. Целевая система так или иначе получает DSC конфигурацию, после чего эти данные передаются в WMI, который и вносит изменения в систему.

Применение конфигурации - Start-DscConfiguration –Path .ContosoWebsite –Wait –Verbose
  
Тест конфигурации - Test-DscConfiguration –CimSession $session

Для функционирования DSC необходим Windows Management Framework 4.0.
  
Из коробки DSC обладает следующими "resource providers": Registry, Script, Archive, File, WindowsFeature, Package, Environment, Group, User, Log, Service, WindowsProcess.

<table border="1" cellspacing="1" cellpadding="3">
  <tr>
    <td valign="top" width="105">
      Provider
    </td>
    
    <td valign="top" width="405">
      Properties
    </td>
  </tr>
  
  <tr>
    <td valign="top" width="105">
      Archive
    </td>
    
    <td valign="top" width="405">
      Destination, Path, Checksum, DependsOn, Ensure, Force, Validate
    </td>
  </tr>
  
  <tr>
    <td valign="top" width="105">
      Environment
    </td>
    
    <td valign="top" width="405">
      Name, DependsOn, Ensure, Path, Value
    </td>
  </tr>
  
  <tr>
    <td valign="top" width="105">
      File
    </td>
    
    <td valign="top" width="405">
      DestinationPath, Attributes, Checksum, Contents, Credential, DependsOn, Ensure, Force, MatchSource, Recurse, SourcePath, Type
    </td>
  </tr>
  
  <tr>
    <td valign="top" width="105">
      Group
    </td>
    
    <td valign="top" width="405">
      GroupName, Credential, DependsOn, Description, Ensure, Members, MembersToExclude, MembersToInclude
    </td>
  </tr>
  
  <tr>
    <td valign="top" width="105">
      Log
    </td>
    
    <td valign="top" width="405">
      Message, DependsOn
    </td>
  </tr>
  
  <tr>
    <td valign="top" width="105">
      Package
    </td>
    
    <td valign="top" width="405">
      Name, Path, ProductId, Arguments, Credential, DependsOn, Ensure, LogPath, ReturnCode
    </td>
  </tr>
  
  <tr>
    <td valign="top" width="105">
      Registry
    </td>
    
    <td valign="top" width="405">
      Key, ValueName, DependsOn, Ensure, Force, Hex, ValueData, ValueType
    </td>
  </tr>
  
  <tr>
    <td valign="top" width="105">
      Script
    </td>
    
    <td valign="top" width="405">
      GetScript, SetScript, TestScript, Credential, DependsOn
    </td>
  </tr>
  
  <tr>
    <td valign="top" width="105">
      Service
    </td>
    
    <td valign="top" width="405">
      Name, BuiltInAccount, Credential, DependsOn, StartupType, State
    </td>
  </tr>
  
  <tr>
    <td valign="top" width="105">
      User
    </td>
    
    <td valign="top" width="405">
      UserName, DependsOn, Description, Disabled, Ensure, FullName, Password, PasswordChangeNotAllowed, PasswordChangeRequired, PasswordNeverExpires
    </td>
  </tr>
  
  <tr>
    <td valign="top" width="105">
      WindowsFeature
    </td>
    
    <td valign="top" width="405">
      Name, Credential, DependsOn, Ensure, IncludeAllSubFeature, LogPath, Source
    </td>
  </tr>
  
  <tr>
    <td valign="top" width="105">
      WindowsProcess
    </td>
    
    <td valign="top" width="405">
      Arguments, Path, Credential, DependsOn, Ensure, StandardErrorPath, StandardInputPath, StandardOutputPath, WorkingDirectory
    </td>
  </tr>
</table>