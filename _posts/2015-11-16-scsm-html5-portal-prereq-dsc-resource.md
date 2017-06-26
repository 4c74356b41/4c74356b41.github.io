---
id: 3801
title: SCSM HTML5 Portal prereq DSC Resource
date: 2015-11-16T11:43:15+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post3801
permalink: /post3801
categories:
  - random
tags:
  - DSC
  - PowerShell
  - Service Manager
---

<div>
  You need to attach 2012r2 dvd with source files and point "source" (in framework 3.5 parts) to dvdsourcessxs for this to work.
</div>

```
Configuration SCSM_Portal_Prereq
 {
   param ($MachineName)
   Node $MachineName
   {
 WindowsFeature 'Web Server IIS'
     {
       Ensure = "Present"
       Name = "Web-Server"
     }
 WindowsFeature 'IIS'
     {
       Ensure = "Present"
       Name = "Web-WebServer"
     }
 WindowsFeature 'IIS Directory Browsing'
     {
       Ensure = "Present"
       Name = "Web-Dir-Browsing"
     }
 WindowsFeature 'IIS Default Document'
     {
       Ensure = "Present"
       Name = "Web-Default-Doc"
     }
 WindowsFeature 'IIS HTTP Errors'
     {
       Ensure = "Present"
       Name = "Web-Http-Errors"
     }
 WindowsFeature 'IIS Static Content'
     {
       Ensure = "Present"
       Name = "Web-Static-Content"
     }
 WindowsFeature 'IIS HTTP Logging'
     {
       Ensure = "Present"
       Name = "Web-Http-Logging"
     }
 WindowsFeature 'IIS Static Content Compression'
     {
       Ensure = "Present"
       Name = "Web-Stat-Compression"
     }
 WindowsFeature 'Basic Authentication'
     {
       Ensure = "Present"
       Name = "Web-Basic-Auth"
     }
 WindowsFeature 'Windows Authentication'
     {
       Ensure = "Present"
       Name = "Web-Windows-Auth"
     }
 WindowsFeature 'Request Filtering'
     {
       Ensure = "Present"
       Name = "Web-Filtering"
     }
 WindowsFeature '.NET Extensibility 4.5'
     {
       Ensure = "Present"
       Name = "Web-Net-Ext45"
     }
 WindowsFeature 'ASP'
     {
       Ensure = "Present"
       Name = "Web-ASP"
     }
 WindowsFeature 'ASP.NET 4.5'
     {
       Ensure = "Present"
       Name = "Web-ASP-Net45"
     }
 WindowsFeature 'IIS ISAPI Filters'
     {
       Ensure = "Present"
       Name = "Web-ISAPI-Filter"
     }
 WindowsFeature 'IIS ISAPI Extensions'
     {
       Ensure = "Present"
       Name = "Web-ISAPI-Ext"
     }
 WindowsFeature 'IIS Management Tools'
     {
       Ensure = "Present"
       Name = "Web-Mgmt-Tools"
     }
 WindowsFeature 'IIS Management Console'
     {
       Ensure = "Present"
       Name = "Web-Mgmt-Console"
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
 WindowsFeature "HTPP Activation"
     {
       Ensure = "Present"
       Name = "NET-WCF-HTTP-Activation45"
     }
 WindowsFeature "WCF TCP Port Sharing"
     {
       Ensure = "Present"
       Name = "NET-WCF-TCP-PortSharing45"
     }
   }
 } 

  

SCSM_Portal_Prereq –MachineName "localhost"

Start-DscConfiguration "path_to_mof" -verbose -wait
```
