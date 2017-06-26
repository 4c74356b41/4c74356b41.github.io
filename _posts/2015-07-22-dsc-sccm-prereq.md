---
id: 2741
title: 'DSC ресурс - ПО для установки SCCM'
date: 2015-07-22T15:03:36+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post2741
permalink: /post2741
categories:
  - SCCM
tags:
  - Configuration Manager
  - DSC
  - System Center 2012 R2
---
Вот такой вот простенький DSC ресурс для установки ПО необходимого для SCCM (SQL намерено опущен, во время когда он писался не было нормального модуля для SQL, возможно до сих пор нет, не исследовал вопрос). 

После выполнения данного "скрипта" Powershell создаст .mof файл, который необходимо использовать для применения конфигурации на сервер. 

Start-DSCConfiguration -Path "Путь к папке где лежит файл (не к файлу, а к папке)" 

```
Configuration SCCM_Prereq
{
  param ($MachineName)

 
  Node $MachineName 
  {
WindowsFeature "Web Server IIS" 
    {
      Ensure = "Present" 
      Name = "Web-Server"
    }
WindowsFeature "IIS"
    {
      Ensure = "Present" 
      Name = "Web-WebServer"
    }
WindowsFeature "IIS Directory Browsing"
    {
      Ensure = "Present"
      Name = "Web-Dir-Browsing"
    }
WindowsFeature "IIS Default Document"
    {
      Ensure = "Present"
      Name = "Web-Default-Doc"
    }
WindowsFeature "IIS HTTP Errors"
    {
      Ensure = "Present"
      Name = "Web-Http-Errors"
    }
WindowsFeature "IIS Static Content"
    {
      Ensure = "Present"
      Name = "Web-Static-Content"
    }
WindowsFeature "IIS HTTP Redirection"
    {
      Ensure = "Present"
      Name = "Web-Http-Redirect"
    }
WindowsFeature "IIS HTTP Logging"
    {
      Ensure = "Present"
      Name = "Web-Http-Logging"
    }
WindowsFeature "IIS Logging Tools"
    {
      Ensure = "Present"
      Name = "Web-Log-Libraries"
    }
WindowsFeature "IIS Request Monitor"
    {
      Ensure = "Present"
      Name = "Web-Request-Monitor"
    }
WindowsFeature "IIS Tracing"
    {
      Ensure = "Present"
      Name = "Web-Http-Tracing"
    }
WindowsFeature "IIS Static Content Compression"
    {
      Ensure = "Present"
      Name = "Web-Stat-Compression"
    }
WindowsFeature "Basic Authentication"
    {
      Ensure = "Present"
      Name = "Web-Basic-Auth"
    }
WindowsFeature "Windows Authentication"
    {
      Ensure = "Present"
      Name = "Web-Windows-Auth"
    }
WindowsFeature "URL Authorization"
    {
      Ensure = "Present"
      Name = "Web-Url-Auth"
    }
WindowsFeature "Request Filtering"
    {
      Ensure = "Present"
      Name = "Web-Filtering"
    }
WindowsFeature "IP and Domain Restrictions"
    {
      Ensure = "Present"
      Name = "Web-IP-Security"
    }
WindowsFeature "ASP.NET 3.5"
    {
      Ensure = "Present"
      Name = "Web-ASP-Net"
    }
WindowsFeature "ASP.NET 4.5"
    {
      Ensure = "Present"
      Name = "Web-ASP-Net45"
    }
WindowsFeature ".NET Extensibility"
    {
      Ensure = "Present"
      Name = "Web-Net-Ext"
    }
WindowsFeature ".NET Extensibility 4.5"
    {
      Ensure = "Present"
      Name = "Web-Net-Ext45"
    }
WindowsFeature "IIS ISAPI Filters"
    {
      Ensure = "Present"
      Name = "Web-ISAPI-Filter"
    }
WindowsFeature "IIS ISAPI Extensions"
    {
      Ensure = "Present"
      Name = "Web-ISAPI-Ext"
    }
WindowsFeature "IIS Management Console"
    {
      Ensure = "Present"
      Name = "Web-Mgmt-Console"
    }
WindowsFeature "Management Tools" 
    {
      Ensure = "Present" 
      Name = "Web-Mgmt-Tools"
    }
WindowsFeature "IIS 6 Metabase Compatibility" 
    {
      Ensure = "Present" 
      Name = "Web-Metabase"
    }
WindowsFeature "IIS 6 Management Console" 
    {
      Ensure = "Present" 
      Name = "Web-Lgcy-Mgmt-Console"
    }
WindowsFeature "IIS 6 Scripting Tools" 
    {
      Ensure = "Present" 
      Name = "Web-Lgcy-Scripting"
    }
WindowsFeature "IIS 6 WMI Compatibility" 
    {
      Ensure = "Present" 
      Name = "Web-WMI"
    }
WindowsFeature "IIS Management Scripts and Tools" 
    {
      Ensure = "Present" 
      Name = "Web-Scripting-Tools"
    }
WindowsFeature "Management Service" 
    {
      Ensure = "Present" 
      Name = "Web-Mgmt-Service"
    }
WindowsFeature ".NET Framework 3.5 Features" 
    {
      Ensure = "Present" 
      Name = "NET-Framework-Features"
    }
WindowsFeature ".NET Framework 3.5 (includes .NET 2.0 and 3.0)" 
    {
      Ensure = "Present" 
      Name = "NET-Framework-Core"
    }
WindowsFeature "HTTP Activation" 
    {
      Ensure = "Present" 
      Name = "NET-HTTP-Activation"
    }
WindowsFeature ".NET Framework 4.5 Features" 
    {
      Ensure = "Present" 
      Name = "NET-Framework-45-Features"
    }
WindowsFeature ".NET Framework 4.5" 
    {
      Ensure = "Present" 
      Name = "NET-Framework-45-Core"
    }
WindowsFeature "FW ASP.NET 4.5" 
    {
      Ensure = "Present" 
      Name = "NET-Framework-45-ASPNET"
    }
WindowsFeature "WCF Services" 
    {
      Ensure = "Present" 
      Name = "NET-WCF-Services45"
    }
WindowsFeature "TCP Port Sharing" 
    {
      Ensure = "Present" 
      Name = "NET-WCF-TCP-PortSharing45"
    }
WindowsFeature "Background Intelligent Transfer Service (BITS)" 
    {
      Ensure = "Present" 
      Name = "BITS"
    }
WindowsFeature "BITS IIS Server Extension"
    {
      Ensure = "Present"
      Name = "BITS-IIS-Ext"
    }
WindowsFeature "Remote Differential Compression"
    {
      Ensure = "Present"
      Name = "RDC"
    }
Package "User State Migration Tools"
    {
      Name = "ADK Deployment Tools"
      Path = "c:adk81adksetup.exe"
      ProductId = "0C4384AC-02DB-B4E5-E537-EE6CF22392CF"
      Arguments = "/quiet /features OptionId.UserStateMigrationTool OptionId.WindowsPreinstallationEnvironment OptionId.DeploymentTools /norestart"
      Ensure = "Present"
      ReturnCode = 0
    }
  }
}

SCCM_Prereq –MachineName "localhost"
```