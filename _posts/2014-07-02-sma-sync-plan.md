---
id: 1016
title: 'SMA - runbook синхронизации плана'
date: 2014-07-02T00:45:44+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post1016
permalink: /post1016
categories:
  - Azure Pack
  - Virtualization and Cloud
tags:
  - Federation Services
  - Guide
  - Service Management Automation
  - SMA
  - Windows Azure Pack
---
Периодически у пользователей возникает ошибка "Failed to load virtual machine templates for subscription <subscription ID>".
  
**Workaround** - синхронизировать планы.
  
Создаем SMA Runbook (Update-Plans) и связываем его с расписанием или событием.
  
У меня уже создан Asset для подключения к WAPack (WAPack\_Admin\_Connection).

```
workflow Update-Plans
{
# Берем из WAPack Asset 'WAPack_Admin_Connection' и работаем с ним
$con = Get-AutomationConnection -Name 'WAPack_Admin_Connection'
$pwd = ConvertTo-SecureString $con.Password -AsPlainText -Force
$crd = New-Object System.Management.Automation.PSCredential ($con.Username, $pwd)

# Начинаем делать ADFS токен
function Get-AdfsToken([string]$adfsAddress, [PSCredential]$credential)
{
$clientRealm = "http://azureservices/AdminSite'
$allowSelfSignCertificates = $true

Add-Type -AssemblyName 'System.ServiceModel, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089'
Add-Type -AssemblyName 'System.IdentityModel, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089'

$identityProviderEndpoint = New-Object -TypeName System.ServiceModel.EndpointAddress -ArgumentList ($adfsAddress + '/adfs/services/trust/13/usernamemixed')
$identityProviderBinding = New-Object -TypeName System.ServiceModel.WS2007HttpBinding -ArgumentList ([System.ServiceModel.SecurityMode]::TransportWithMessageCredential)
$identityProviderBinding.Security.Message.EstablishSecurityContext = $false
$identityProviderBinding.Security.Message.ClientCredentialType = 'UserName'
$identityProviderBinding.Security.Transport.ClientCredentialType = 'None'

$trustChannelFactory = New-Object -TypeName System.ServiceModel.Security.WSTrustChannelFactory -ArgumentList $identityProviderBinding, $identityProviderEndpoint
$trustChannelFactory.TrustVersion = [System.ServiceModel.Security.TrustVersion]::WSTrust13

    if ($allowSelfSignCertificates)
    {
$certificateAuthentication = New-Object -TypeName System.ServiceModel.Security.X509ServiceCertificateAuthentication
$certificateAuthentication.CertificateValidationMode = ‘None’
$trustChannelFactory.Credentials.ServiceCertificate.SslCertificateAuthentication = $certificateAuthentication
    }

$ptr = [System.Runtime.InteropServices.Marshal]::SecureStringToCoTaskMemUnicode($credential.Password)
$password = [System.Runtime.InteropServices.Marshal]::PtrToStringUni($ptr)
[System.Runtime.InteropServices.Marshal]::ZeroFreeCoTaskMemUnicode($ptr)

$trustChannelFactory.Credentials.SupportInteractive = $false
$trustChannelFactory.Credentials.UserName.UserName = $credential.UserName
$trustChannelFactory.Credentials.UserName.Password = $password #$credential.Password

$rst = New-Object -TypeName System.IdentityModel.Protocols.WSTrust.RequestSecurityToken -ArgumentList ([System.IdentityModel.Protocols.WSTrust.RequestTypes]::Issue)
$rst.AppliesTo = New-Object -TypeName System.IdentityModel.Protocols.WSTrust.EndpointReference -ArgumentList $clientRealm
$rst.TokenType = 'urn:ietf:params:oauth:token-type:jwt'
$rst.KeyType = [System.IdentityModel.Protocols.WSTrust.KeyTypes]::Bearer

$rstr = New-Object -TypeName System.IdentityModel.Protocols.WSTrust.RequestSecurityTokenResponse

$channel = $trustChannelFactory.CreateChannel()
$token = $channel.Issue($rst, [ref] $rstr)

$tokenString = ([System.IdentityModel.Tokens.GenericXmlSecurityToken]$token).TokenXml.InnerText;
$result = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($tokenString))
return $result
}

# Генерируем токен и отправляем запрос
$adfsAddress = 'https://fqdn'
$token = Get-AdfsToken -adfsAddress $adfsAddress -credential $crd
$adminUri = 'https://' + $con.ComputerName + ':30004' - необходимо указать endpoint Admin API
$plans = Get-MgmtSvcPlan -AdminUri $adminUri -Token $token -DisableCertificateValidation

# Синхронизируем план
foreach ($id in $plans) { 
  write-output Syncing $id.DisplayName
  Sync-MgmtSvcPlan -AdminUri $adminUri -Token $token -DisableCertificateValidation -PlanId $id.id
  }
}
```

Если Вам нужно авторизоваться через Windows Credentials вырезаете кусок про ADFS и генерируете токен

```
$Token = Get-MgmtSvcToken –Type Windows –AuthenticationSite https://FQDN_auth_site:30072 – ClientRealm http://azureservices/AdminSite -User $Credentials -DisableCertificateValidation
```