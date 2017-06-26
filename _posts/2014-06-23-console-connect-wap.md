---
id: 708
title: 'Настраиваем "Console Connect" в Windows Azure Pack'
date: 2014-06-23T23:37:28+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post708
permalink: /post708
categories:
  - Azure Pack
  - Virtualization and Cloud
tags:
  - Guide
  - Service Provider Foundation
  - SPF
  - System Center 2012 R2
  - Virtual Machine Manager
  - Windows Azure Pack
---
В статье про первые шаги в [настройке WAP](http://4c74356b41.com/post655) я упомянул Console Connect.  
  
Для корректной работы Console Connect вам потребуется:
  
1. хост Hyper-V 2012 R2;
  
2. VMM 2012 R2;
  
3. SPF 2012 R2;
  
4. Windows Azure Pack;
  
5. Windows 8.1 или Windows 7 SP1 и [KB2830477](http://support.microsoft.com/kb/2830477);
  
6. RD Gateway сервер;
  
7. порты 443(TCP) и 2179(TCP) должны быть открыть для клиента, а 3389(TCP) рекомендуется закрыть.
  
DNS имена должны разрешаться из DMZ если Вы хотите использовать разрешение имен, для подключения к Hyper-V хостам по IP адресу необходимо производить немного другие настройки, о них в [следующей статье](http://4c74356b41.com/post717).

На данный момент Remote Console не поддерживает такие функции как передачу звука и буфера обмена, перенаправление принтера и подключение дисков.

**Аутентификация пользователей**
  
Console Connect использует аутентификацию по сертификату. Данная иллюстрация объясняет каким образом тенанты могут получать доступ к виртуальным машинам из интернета или любой другой не доверенной сети.

<a href="http://4c74356b41.com/wp-content/uploads/2016/02/RDGW_overview.gif" rel="attachment wp-att-4817"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/RDGW_overview-300x117.gif" alt="RDGW_overview" width="300" height="117" /></a>
  
1. Пользователь аутентифицируется на WAP Tenant портале;
  
2. WAP Tenant портал связывается с VMM, используя SPF, и просит токен;
  
3. VMM генерирует claim токен, передает его на RD Gateway, RD Gateway генерирует файл RDP соединения и передает обратно клиенту;
  
4. Клиент связывается с Hyper-V хостом через RD Gateway и подключается к виртуальной машине через VMBus;
  
5. Hyper-V хост проверяет claim токен используя публичный ключ сертификата VMM.

**Требования к сертификату**
  
1. Сертификат должен быть действительным;
  
2. Поле "Key Usage" должно содержать цифровую подпись;
  
3. Поле "Enhanced Key Usage" должно содержать объект идентификации клиента (1.3.6.1.5.5.7.3.2);
  
4. Центр сертификации выдавший данный сертификат должен быть доверенным для клиента;
  
5. Должен поддерживаться механизм шифрования SHA256.

Данный сертификат можно получить тремя способами, купить, выписать самоподписанный (в этом случае публичный ключ сертификата необходимо импортировать на RD Gateway и Hyper-V хосты) или использовать Enterprise PKI.

**Подготовка PKI к выдаче сертификата.**
  
В консоли управления PKI необходимо зайти в шаблоны сертификатов и создать копию шаблона "Smartcard Logon". Переименовать её в Remote Console Connect (или во что вам угодно) и изменить в закладке "Cryptography" поля "Minimum Key size" на 2048, "Requests must use one of the following providers" выбрать Microsoft Enhanced RSA and AES Cryptographic Provider. Так же необходимо в закладке "Subject Name" разрешить пользователю самому передавать имя в заявке, после чего разрешить (закладка Security) пользователю, от имени которого Вы собираетесь создавать сертификат, право Enroll.
  
После этого остается только разрешить выдавать сертификаты используя данный шаблон (В консоли управления PKI правой кнопкой мыши на поле Certificate Templates >> New >> Certificate Template to issue).

**Создание сертификата**
  
На сервере VMM создайте папку C:crt и в ней файл cert.inf следующего содержания:

```
[Version]
Signature="$Windows NT$"
[NewRequest]
; необходимо заменить страну. организацию и common name на необходимые вам значения
Subject = "C=RU, O=Company, CN=wap-rdg.contoso.com"
; Шифроваие и подписывание
KeySpec = 1 
; "Длинна" публичного и частного ключа, можно использовать значение от 2048 и выше
KeyLength = 2048
; Сертификат будет установлен в хранилище "Local Computer"
MachineKeySet = TRUE 
PrivateKeyArchive = FALSE
RequestType = PKCS10
UserProtected = FALSE
; Возможность использовать сертификат на несколькоих компьютерах
Exportable = TRUE
SMIME = False
UseExistingKeySet = FALSE 
; Имя и тип провайдера должны указывать на провайдер поддерживающий SHA256
ProviderName = "Microsoft Enhanced RSA and AES Cryptographic Provider"
ProviderType = 24
; Поле "KeyUsage" должно содержать цифровую подпись. 0xA0 включает в себя цифровую подпись и шифрование.
KeyUsage = 0xa0
[EnhancedKeyUsageExtension]
OID=1.3.6.1.5.5.7.3.2
```

После этого запустите командную строку от имени администратора и выполните следующие команды:

```
cd C:Crt
certreq –f new Cert.inf Cert.req
certutil Cert.req – проверка валидности запроса сертификата
certreq -attrib "CertificateTemplate:RemoteConsoleConnect" -submit Cert.req Cert.cer - если Вы указали другое имя шаблона сертификата укажите его тут
certreq -accept Cert.cer
certutil -store my – найдите сгенерированный сертификат и скопируйте Serial Number в буфер обмена
certutil -exportpfx my Serial_Number C:\Crt\Cert.pfx – укажите пароль для данного файла.
$cert = Get-ChildItem C:\Crts\Cert.pfx 
$mypwd = Read-Host -AsSecureString – пароль .pfx файла
$VMMServer = FQDN_VMM
Set-SCVMMServer -VMConnectGatewayCertificatePassword $mypwd -VMConnectGatewayCertificatePath $cert -VMConnectHostIdentificationMode FQDN -VMConnectHyperVCertificatePassword $mypwd -VMConnectHyperVCertificatePath $cert -VMConnectTimeToLiveInMinutes 2 -VMMServer $VMMServer
Get-SCVMHost -VMMServer $VMMServer | Read-SCVMHost – обновление хостов, установка сертификата на них
```

**Установка и настройка RD Gateway**
  
Заходим на сервер RD Gateway и запускаем powershell от имени администратора
  
Install-WindowsFeature -Name RDS-Gateway -IncludeManagementTools

Подключаем ISO с образом VMM и запускаем с него установку RD Gateway Console Connect pluggable authentication and authorization component (PAA)
  
d:AMD64SetupmsiRDGatewayFedAuthRDGatewayFedAuth.msi

**Импортируем сертификат**

```
Import-Certificate -CertStoreLocation cert:LocalMachineMy -Filepath 'vmmhostname\C$\Crts\Cert.cer' – после успешного импорта скопируйте поле Thumbprint в буфер обмена
$Server = "FQDN_RD_Gateway"
$Thumbprint = "Thumbprint”
$TSData = Get-WmiObject -computername $Server -NameSpace "rootTSGatewayFedAuth2" -Class "FedAuthSettings"
$TSData.TrustedIssuerCertificates = $Thumbprint
$TSData.Put();
```

Далее нам необходимо выписать обычный сертификат веб-сервера у нашего центра сертификации и "прикрепить" его к службе RD Gateway. Заходим в Remote Desktop Gateway Manager и шелкаем правой кнопкой мыши на нашем RD Gateway сервере в новом окне и жмем "Properties". На закладке "SSL Certificate" импортируем сертификат.

**Настройка WAP**
  
На админ портале WAP VM Clouds выберите сервер VMM, свойства которого необходимо изменить, и нажмите "Edit". Заполните поле Remote Desktop Gateway FQDN.

Можно использовать powershell

```
Import-Module SPFAdmin
$Stamp = Get-SCSPFStamp
$GWserver="FQDN_RD_Gateway"
New-SCSPFServer -Name $GWserver -ServerType RDGateway -Stamps $Stamp[0];
```

На этом настройка завершена.

**Типичные ошибки**
  
1. Вы получаете JSON файл. вместо файла RDP соединения
  
Это означает что VMM использует самоподписанный сертификат для генерации токенов, а Hyper-V ему не доверяет (не импортирован в хранилище или публичный ключ не импортирован в хранилище).

2. Следующая ошибка в логах VMM
  
Name=System.Security.Cryptography.CryptographicException.ThrowCryptographicException
  
Exception Message=Invalid algorithm specified
  
Использование неправильного провайдера шифрования (не Microsoft Enhanced RSA and AES Cryptographic Provider).

3. <a href="http://4c74356b41.com/wp-content/uploads/2016/02/RDGW_trblsht1.png" rel="attachment wp-att-4820"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/RDGW_trblsht1-300x73.png" alt="RDGW_trblsht1" width="300" height="73" /></a>
  
Отпечаток сертификата VMM не зарегистрирован на сервере RD Gateway или на сервере RD Gateway был изменен сертификат без перезагрузки сервера

4. <a href="http://4c74356b41.com/wp-content/uploads/2016/02/RDGW_trblsht2.png" rel="attachment wp-att-4823"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/RDGW_trblsht2-300x61.png" alt="RDGW_trblsht2" width="300" height="61" /></a>
  
RD Gateway URL на WAP Portal'е не совпадает с Common Name сертификата RD Gateway или в сертификате не заполнено поле "Subject Alternative Name" значением "DNS=FQDN\_RD\_Gateway_сервера". При попытке подключения будет сообщено о не совпадении адреса и subject name сертификата