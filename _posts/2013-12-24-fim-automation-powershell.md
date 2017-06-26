---
id: 281
title: Установка FIMAutomation Powershell на сервер без оной
date: 2013-12-24T14:02:41+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post281
permalink: /post281
categories:
  - MIM
tags:
  - Copypaste
  - FIM
  - Guide
---
Главный вопрос: "Зачем?".
  
Ответов может быть много, в моем случае я хотел использовать Powershell для запуска заданий агентов синхронизации на сервере без данного модуля.

**Итак. Нам необходимы:**
  
Microsoft.ResourceManagement.Automation.dll
  
Microsoft.IdentityManagement.Logging.dll (для FIM 2010 R2)
  
Microsoft.ResourceManagement.Logging.dll (для FIM 2010)
  
Microsoft.ResourceManagement.dll
  
Берем их из "C:Program FilesMicrosoft Forefront Identity Manager2010Service". После чего, необходимо зарегистрировать модуль и dll файлы в Global Assembly Cache.

Командная строка Visual Studio с права администратора:
  
InstallUtil.exe -i .Microsoft.ResourceManagement.Automation.dll
  
gacutil -i Microsoft.ResourceManagement.dll
  
gacutil -i Microsoft.IdentityManagement.Logging.dll (для FIM 2010 R2)
  
gacutil -i Microsoft.ResourceManagement.Logging.dll (для FIM 2010)

В случае установки на 64х битную систему необходимо использовать 64х битную версию InstallUtil, а не 32х битную.

Честно говоря, не всегда под рукой есть Visual Studio, потому:

```
@echo off
cls
set _FIMAutoDLL=Microsoft.ResourceManagement.Automation.dll
set _FIMAutoHlp=Microsoft.ResourceManagement.Automation.dll-Help.xml
set _FIMRscMgmt=Microsoft.ResourceManagement.dll
set _FIMLogging=Microsoft.ResourceManagement.Logging.dll
set _FIMR2Logging=Microsoft.IdentityManagement.Logging.dll


if exist %_FIMAutoHlp% goto FoundHelp
echo FIM Automation Help not found!
goto BadMojo

:FoundHelp
if exist %_FIMAutoDLL% goto FIMAutoInstall
echo FIM Automation Assembly not found!
goto BadMojo

:FIMAutoInstall
echo Install FIMAutomation
"C:WindowsMicrosoft.NETFramework64v2.0.50727InstallUtil.exe" -i .%_FIMAutoDLL%


if exist %_FIMRscMgmt% goto FIMRscMgmtInstall
echo FIm Resource Management Assembly not found!
goto BadMojo

:FIMRscMgmtInstall
echo Install ResourceManagement Assembly in the GAC
"C:Program Files (x86)Microsoft SDKsWindowsv7.0ABinx64gacutil.exe" -i %_FIMRscMgmt%

if exist %_FIMLogging% goto FIMLogInstall
if exist %_FIMR2Logging% goto FIMR2LogInstall
echo FIM Logging Assembly not found!
goto BadMojo

:FIMR2LogInstall
echo Install FIM 2010 R2 Logging Assembly into the GAC
"C:Program Files (x86)Microsoft SDKsWindowsv7.0ABinx64gacutil.exe" -i %_FIMR2Logging%
goto BatchEnd

:FIMLogInstall
echo Install FIM 2010 Logging Assembly into the GAC
"C:Program Files (x86)Microsoft SDKsWindowsv7.0ABinx64gacutil.exe" -i %_FIMLogging%
goto BatchEnd

:BadMojo
echo.
echo.
echo Copy ALL these files
echo.
echo %_FIMAutoHlp%
echo %_FIMAutoDLL%
echo %_FIMRscMgmt%
echo %_FIMLogging%
echo.
echo to this directory before running this command again!
echo.
goto BatchEnd

:BatchEnd
set _FIMAutoDLL=
set _FIMAutoHlp=
set _FIMRscMgmt=
set _FIMLogging=
set _FIMR2Logging=

echo Install Done.
```