---
id: 717
title: Console Connect используя IP адреса
date: 2014-06-24T15:34:18+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post717
permalink: /post717
categories:
  - Azure Pack
  - Virtualization and Cloud
tags:
  - Guide
  - System Center 2012 R2
  - Virtual Machine Manager
  - Windows Azure Pack
---
В продолжении поста о [Console Connect](http://4c74356b41.com/post708) настроим его для работы по IP.

В чем же отличие между подключением по IP и по FQDN?
  
В случае подключение к Hyper-V хосту по IP адресу IP адрес запроса и IP адрес в сертификате не совпадут и Вам будет возращена ощибка An authentication error occurred (0×607). В то время как при подключение по FQDN значения совпадут.

Для начала Вам необходимо будет воспроизвести настройки как в предыдущем посте, но вместо указания типа подключения FQDN необходимо указать IP.
  
Set-SCVMMServer -VMConnectGatewayCertificatePassword $mypwd -VMConnectGatewayCertificatePath $cert -VMConnectHostIdentificationMode IP -VMConnectHyperVCertificatePassword $mypwd -VMConnectHyperVCertificatePath $cert -VMConnectTimeToLiveInMinutes 2 -VMMServer $VMMServer

Вам необходимо будет сгенерировать сертификаты для хостов Hyper-V, но поскольку makecert не может создать сертификат с двумя значениями в поле Subject мы используем powershell. Эту процедуру необходимо выполнить на каждом хосте Hyper-V, кроме того, в случае смены IP адреса Hyper-V хоста, Вам необходимо будет сгенерировать сертификат снова.

```
$name = new-object -com "X509Enrollment.CX500DistinguishedName.1"
$name.Encode("CN=FQDN, CN=IP адрес", 0)
$key = new-object -com "X509Enrollment.CX509PrivateKey.1"
$key.ProviderName = "Microsoft RSA SChannel Cryptographic Provider"
$key.KeySpec = 1
$key.Length = 2048
$key.SecurityDescriptor = "D:PAI(A;;0xd01f01ff;;;SY)(A;;0xd01f01ff;;;BA)(A;;0×80120089;;;NS)"
$key.MachineContext = 1
$key.Create()
$serverauthoid = new-object -com "X509Enrollment.CObjectId.1"
$serverauthoid.InitializeFromValue("1.3.6.1.5.5.7.3.2")
$ekuoids = new-object -com "X509Enrollment.CObjectIds.1"
$ekuoids.add($serverauthoid)
$ekuext = new-object -com "X509Enrollment.CX509ExtensionEnhancedKeyUsage.1"
$ekuext.InitializeEncode($ekuoids)
$kuext = new-object -com "X509Enrollment.CX509ExtensionKeyUsage.1"
$kuext.InitializeEncode(0×30)
$cert = new-object -com "X509Enrollment.CX509CertificateRequestCertificate.1"
$cert.InitializeFromPrivateKey(2, $key, "")
$cert.Subject = $name
$cert.Issuer = $cert.Subject
$cert.NotBefore = (Get-Date).ToUniversalTime()
$cert.NotAfter = $cert.NotBefore.AddDays(900)
$cert.X509Extensions.Add($ekuext)
$cert.X509Extensions.Add($kuext)
$cert.Encode()
$enrollment = new-object -com "X509Enrollment.CX509Enrollment.1"
$enrollment.InitializeFromRequest($cert)
$certdata = $enrollment.CreateRequest(0)
$enrollment.InstallResponse(2, $certdata, 0, "")
```

Получаем отпечатки сертификатов
  
$thumbprints = @(dir cert:localmachineMy | Where-Object { $_.subject -eq "CN=FQDN, CN=IP адрес"} ).thumbprint
  
$thumbprints

Скопируйте отпечаток нужного сертификата и используйте его в следующем скрипте

```
$thumbprint = "отпечаток"
$certs = dir cert: -recurse | ? { $_.Thumbprint -eq $thumbprint }
$cert = @($certs)[0]
$location = $cert.PrivateKey.CspKeyContainerInfo.UniqueKeyContainerName
$folderlocation = gc env:ALLUSERSPROFILE
$folderlocation = $folderlocation + "MicrosoftCryptoRSAMachineKeys"
$filelocation = $folderlocation + $location
$filelocation
icacls $filelocation /grant "*S-1-5-83-0:(R)"
$cert.thumbprint
reg add "HKLMSoftwareMicrosoftWindows NTCurrentVersionVirtualization" /v "AuthCertificateHash" /f /t REG_BINARY /d $thumbprint
reg add "HKLMSoftwareMicrosoftWindows NTCurrentVersionVirtualization" /v "DisableSelfSignedCertificateGeneration" /f /t REG_QWORD /d 1
```

Данный скрипт сконфигурирует Hyper-V. Он "импортирует" созданный сертификат в Hyper-V и запретит Hyper-V генерировать новые сертификаты. После этого службу Hyper-V нужно перезапустить, а виртуальные машины смигрировать на другой хост.

К сожалению, в данном случае у пользователей будет "выскакивать" еще одно окно вопрощающее доверяет ли пользователь хосту Hyper-V. Чтобы обойти это необходимо отредактировать RDP файл и добавить значение "authentication level:i:0". Ну, естественно, делать это руками бред, тем более если Вы планируете предоставлять виртуальные машины как услуги, это не приемлимо.

Для того чтобы делать это автоматически необходимо с помощью URL Rewrite (устанавливается с помощью Web Platform Installer) на хосте где насположен SPF создать мнимое правило URL Rewrite (Outbound) заполнить название и написать что-либо в поле Pattern Field, после чего отредактировать web.config файл  (c:inetpubspf по умолчанию) следующим образом

```
outboundRules&gt;
 &lt;clear /&gt;
 &lt;rule name="Remote Console on IP Address" preCondition="VMConsole RDP File" enabled="true"&gt;
 &lt;match filterByTags="None" pattern="negotiate security layer:i:1" /&gt;
 &lt;conditions logicalGrouping="MatchAll" trackAllCaptures="true" /&gt;
 &lt;action type="Rewrite" value="negotiate security layer:i:1 &#xD;&#xA;authentication level:i:0" /&gt;
 &lt;/rule&gt;
 &lt;preConditions&gt;
 &lt;preCondition name="VMConsole RDP File"
 &lt;add input="{REQUEST_URI}" pattern="^.*(/VMConnection)$" /&gt;
 &lt;add input="{RESPONSE_CONTENT_TYPE}" pattern="^application/x-rdp$" /&gt;
 &lt;/preCondition&gt;
 &lt;/preConditions&gt;
 &lt;/outboundRules&gt;
 ```

Напоминаю, что для передачи "Ctrl+Alt+Delete" необходимо использовать комбинацию "Ctrl+Alt+End". 😉