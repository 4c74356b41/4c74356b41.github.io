---
id: 290
title: Установка FIM Reporting на SCSM 2012 R2
date: 2013-12-26T11:33:18+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post290
permalink: /post290
categories:
  - MIM
tags:
  - Copypaste
  - FIM
  - Guide
---
При установке из, прости господи, ГУЯ инсталлер ругается, что ему не хватает KB 2561430 (данный хотфикс необходим для SCSM 2010). Чтож, победим.

Запускаем PowerShell от имени администратора и переходим в папку инсталлера FIM, которая называется "Service and Portal":

```
& '.Service and Portal.msi' /l c:\file.log /qn ACCEPT_EULA=1 MAIL_SERVER="имя_сервера_эксчендж" SERVICE_ACCOUNT_NAME="имя_сервисного_аккаунта_фим" SERVICE_ACCOUNT_PASSWORD="пароль" SERVICE_ACCOUNT_DOMAIN="домен" SERVICE_ACCOUNT_EMAIL="почта" SERVICE_MANAGER_SERVER="FQDN_сервера_SCSM" SQLSERVER_SERVER="FQDN_сервера_SQL" SERVICEADDRESS="адрес_fim_service" ADDLOCAL=FIMReporting SQMOPTINTSETTING=0 SYNCHRONIZATION_SERVER_ACCOUNT="домен\аккаунт_для_общения_с_fim_synch_service" RMS_PORT=5725 STS_PORT=5726 SHAREPOINTUSERS_CONF=1 PASSWORDUSERS_CONF=1 FIREWALL_CONF=1 RESET_FIREWALL_CONF=1 REGISTRATION_FIREWALL_CONF=1 SHAREPOINT_URL=http://FIMPortal_Sharepoint_SiteCollection REGISTRATION_ACCOUNT=Domainuser REGISTRATION_ACCOUNT_PASSWORD="pwd" REGISTRATION_PORT=8905 REGISTRATION_SERVERNAME=fim.test.com IS_REGISTRATION_EXTRANET=1 REGISTRATION_HOSTNAME=pwd.test.com RESET_ACCOUNT=domianuser RESET_ACCOUNT_PASSWORD="pwd" RESET_PORT=8906 RESET_SERVERNAME=fim.test.com IS_RESET_EXTRANET=1 RESET_HOSTNAME=rst.test.com REGISTRATION_PORTAL_URL=http://pwd.test.com
```

Кроме этого, необходимо чтобы на сервере FIM была установлена консоль SCSM 2012 R2, пользователь должен быть локальным администратором на сервере "Data Warehouse" SCSM и администратором SCSM 2012 R2 и обладать всеми необходимыми правами для установки FIM.
  
Естественно DW должен быть зарегистрирован в SCSM. 😉

Если необходимо поставить не только FIM Reporting на сервер, то к ключу "ADDLOCAL=FIMReporting" добавляем через запятую нужные компоненты по вкусу (необходимо соблюдать точность в написании, те учитывать большие и маленькие символы, без кавычек):
  
"CommonServices" (для установки FIM Service)
  
"WebPortals" (для установки FIM Portal)
  
"RegistrationPortal"
  
"ResetPortal"

ПС. Справедливости ради скажу, что в логах инсталятора написано что KB 2561430 не установлен и его необходимо установить 😉