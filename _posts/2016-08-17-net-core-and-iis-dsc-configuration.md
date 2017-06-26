---
id: 5664
title: .NET core and IIS DSC Configuration
date: 2016-08-17T10:45:35+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post5664
permalink: /post5664
categories:
  - random
tags:
  - DSC
  - PowerShell
---
Ok, so I've put together a DSC Configuration to setup basic .NET core app on IIS.

```
Configuration Payload
{

Param ( [string] $nodeName )

Import-DscResource -ModuleName PSDesiredStateConfiguration
Import-DscResource -ModuleName @{ModuleName="xPSDesiredStateConfiguration" ModuleVersion="3.0.3.4"}
Import-DscResource -ModuleName @{ModuleName="xWebAdministration" ModuleVersion="1.13.0.0"}

Node $nodeName
  {

    LocalConfigurationManager 
    { 
        # This is false by default
        RebootNodeIfNeeded = $true
    } 

    WindowsFeature WebServerRole
    {
        Name = "Web-Server"
        Ensure = "Present"
    }

    WindowsFeature WebManagementConsole
    {
        Name = "Web-Mgmt-Console"
        Ensure = "Present"
    }


    xRemoteFile Payload {
        Uri             = ">>> url_to_your_app_goes_here &lt;&lt;&lt;" 
        DestinationPath = "C:\Setup\website.zip" 
    }


    xRemoteFile InstallDotNetCoreWindowsHosting {
        Uri             = "https://go.microsoft.com/fwlink/?LinkId=817246" 
        DestinationPath = "C:\Setup\InstallDotNetCoreWindowsHosting.exe" 
    }


    Archive WebAppExtract
    {              
         Path = "C:\Setup\website.zip"
         Destination = "C:\inetpub\webapp\wwwroot"
         DependsOn = "[xRemoteFile]Payload"            
    }


    Package InstallDotNetCoreWindowsHosting
    {
           Ensure = "Present"
           Path = "C:\WindowsAzure\DotNetCore.1.0.0-WindowsHosting.exe"
           Arguments = "/q /norestart"
           Name = "DotNetCore"
           ProductId = "4ADC4F4A-2D55-442A-8655-FBF619F94A69"
           DependsOn = "[xRemoteFile]InstallDotNetCoreWindowsHosting"
    }
   

	xWebsite DefaultSite   
    {  
            Ensure          = "Present"
            Name            = "Default Web Site"
            State           = "Stopped"
            PhysicalPath    = "C:\inetpub\wwwroot" 
            DependsOn       = "[WindowsFeature]WebServerRole"
    }


	xWebAppPool WebAppAppPool   
    {  
            Ensure          = "Present"  
            Name            = "web-app" 
            State           = "Started"
            managedRuntimeVersion = ""
      }  


	xWebsite WebAppWebSite   
        {  
            Ensure          = "Present"  
            Name            = "web-app" 
            State           = "Started"
            PhysicalPath    = "C:\inetpub\webapp\wwwroot"
            ApplicationPool = "web-app"
            BindingInfo = MSFT_xWebBindingInformation
                    {
                        Port = '8080'
                        IPAddress = '*'
                        Protocol = 'HTTP'
                    }
            DependsOn = "[xWebAppPool]WebAppAppPool"
        }
  }
}

payload -nodename localhost
```

So to run this just copy it to the target server, copy dependencies (xPSDesiredStateConfiguration and xWebAdministration) and put them into "C:\Program Files\WindowsPowerShell\Modules". After that, you open powershell_ise and load this DSC configuration there and run it. Tt will créate a mof and meta.mof files (the output will show where they were created), after that you invoke: 

```
Start-DSCConfiguration -Path insert_path_to_mofs -Wait -Verbose -Force
```

It should work fine after all of this if you've assembled it properly. Check this link for details https://weblog.west-wind.com/posts/2016/Jun/06/Publishing-and-Running-ASPNET-Core-Applications-with-IIS