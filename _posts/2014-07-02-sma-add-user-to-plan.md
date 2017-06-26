---
id: 1027
title: 'SMA - автоматическое добавление пользователя в план'
date: 2014-07-02T12:50:25+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post1027
permalink: /post1027
categories:
  - Azure Pack
  - Virtualization and Cloud
tags:
  - Guide
  - Service Management Automation
  - SMA
  - Windows Azure Pack
---
На базе [предыдущего поста](http://4c74356b41.com/post1016), немного изменив ранбук можно получить ранбук, который будет автоматически добавлять нового пользователя в план. Для этого пользователю необходимо будет просто зайти на портал.

Помните, что если Вы не используете ADFS при регистрации можно указать любые учетные данные и, таким образом, получить доступ к любому плану.
  
**Что потребуется:**
  
1. Работающий [SPF](http://4c74356b41.com/post466), [SMA](http://4c74356b41.com/post678) и [WAP](http://4c74356b41.com/post422)
  
2. SPF и SMA доверяющие друг-другу (сертификаты endpoint'ов)
  
3. Пользователь spf-app-pool в группе smaAdmingroup (на веб сервис ролях SMA)
  
4. Готовый ассет для подключения к AdminAPI
  
Кроме этого, Вам необходимо будет создать триггер, триггер срабатывает когда пользователь подписывается на существующий план. Логика такая - У Вас есть публичный план, на него могу подписываться все пользователи, но определенные пользователи (скажем, определенного домена) будут автоматически добавлены во второй план.
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/sma-new-tenant.png" rel="attachment wp-att-5346"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/sma-new-tenant-300x205.png" alt="sma-new-tenant" width="300" height="205" /></a>

```
workflow New-Tenant
{
# Получаем данные о пользователе
param([object]$resourceObject)    
$NewUserEmail = $resourceObject.Name -split "_" | select -first 1

# Берем из WAPack Asset 'WAPack_Admin_Connection' и работаем с ним
$con = Get-AutomationConnection -Name 'WAPack_Admin_Connection'
$pwd = ConvertTo-SecureString $con.Password -AsPlainText -Force
$crd = New-Object System.Management.Automation.PSCredential ($con.Username, $pwd)

# Начинаем делать ADFS токен
function Get-AdfsToken([string]$adfsAddress, [PSCredential]$credential)
{
$clientRealm = 'http://azureservices/AdminSite'
$allowSelfSignCertificates = $true

Add-Type -AssemblyName 'System.ServiceModel, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089'
Add-Type -AssemblyName 'System.IdentityModel, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089'

$identityProviderEndpoint = New-Object -TypeName System.ServiceModel.EndpointAddress -ArgumentList ($adfsAddress + ‘/adfs/services/trust/13/usernamemixed’)
$identityProviderBinding = New-Object -TypeName System.ServiceModel.WS2007HttpBinding -ArgumentList ([System.ServiceModel.SecurityMode]::TransportWithMessageCredential)
$identityProviderBinding.Security.Message.EstablishSecurityContext = $false
$identityProviderBinding.Security.Message.ClientCredentialType = 'UserName'
$identityProviderBinding.Security.Transport.ClientCredentialType = 'None'

$trustChannelFactory = New-Object -TypeName System.ServiceModel.Security.WSTrustChannelFactory -ArgumentList $identityProviderBinding, $identityProviderEndpoint
$trustChannelFactory.TrustVersion = [System.ServiceModel.Security.TrustVersion]::WSTrust13

    if ($allowSelfSignCertificates)
    {
$certificateAuthentication = New-Object -TypeName System.ServiceModel.Security.X509ServiceCertificateAuthentication
$certificateAuthentication.CertificateValidationMode = 'None'
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

# Генерируем токен и подключение (Необходимо изменить FQDN)
$adfsAddress = 'https://ADFS_server_FQDN'
$token = Get-AdfsToken -adfsAddress $adfsAddress -credential $crd
$adminUri = 'https://' + $con.ComputerName + ':30004'

$newuser = Get-MgmtSvcUser -Token $token -AdminUri $adminUri -DisableCertificateValidation -Name $NewUserEmail
$uname=$newuser.name
 
# Проверка валидности пользователя (Необходимо изменить домены)
    if (($uname -like "*@tailspintoys.com") -or ($uname -like "*@tailspin.local")) {
    # Пользователь валиден
 
# Получаем план (Необходимо изменить имя плана)
        $plan = Get-MgmtSvcPlan -Token $token -AdminUri $adminUri -DisableCertificateValidation -DisplayName "Default" | where State -notlike "Decommissioned" | select -first 1
        $planname=$plan.DisplayName
 
        # Получаем подписки 
        $currentsubs = Get-MgmtSvcSubscription -Token $token -AdminUri $adminUri -DisableCertificateValidation | where AccountAdminLiveEmailId -like "$uname" | where OfferFriendlyName -like "$planname"
 
        if ($currentsubs.count -lt $plan.MaxSubscriptionsPerAccount){
            $newsubscription = Add-MgmtSvcSubscription -Token $token -AdminUri $adminUri -DisableCertificateValidation -AccountAdminLiveEmailId $uname -AccountAdminLivePuid $uname -PlanId $plan.id -FriendlyName $plan.DisplayName
            write-output "$uname has been added to $planname with subscriptionid $newsubscription"
        }
        else {
            Write-Output "User already has a subscriptions for $planname"
        }
    }
else {
    write-output "Not a Valid Employee, did not add user to any plan."  
    }
  }
```