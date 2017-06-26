---
id: 4741
title: Azure Site Recovery умер, да здравствует Azure Site Recovery
date: 2016-01-12T13:02:43+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post4741
permalink: /post4741
categories:
  - Azure
tags:
  - Azure
  - Azure Site Recovery
---
Таки вышла новая версия Azure Site Recovery для VMWare\Физических серверов.

1. Не нужно создавать masterconfiguration сервер в Azure. Дешевле. Удобнее.
  
2. Сделали нормальный (предположительно, еще не тестировал) MSI инсталлер, один на все (с). Далее-Далее-Далее.
  
3. Можно делать "test failover". И появилась возможность выключить виртуальные машины при failover'э.
  
4. ASR-integrated failback. Я так понимаю сие означает что фейлбэк теперь настраивается сам по себе, чудесно. 🙂

Читать [раз](https://azure.microsoft.com/en-us/blog/ga-enhanced-migration-and-disaster-recovery-for-vmware-virtual-machines-and-physical-servers-to-azure-using-asr/) и [два](https://azure.microsoft.com/en-us/documentation/articles/site-recovery-vmware-to-azure-classic/).