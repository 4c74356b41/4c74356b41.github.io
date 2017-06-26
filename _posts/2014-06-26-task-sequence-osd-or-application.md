---
id: 853
title: 'Task Sequence - OSD или Application?'
date: 2014-06-26T23:18:48+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post853
permalink: /post853
categories:
  - SCCM
tags:
  - Configuration Manager
  - Copypaste
  - Guide
---
Как изменить тип таск сиквенса с OSD на Application или наоборот. Чтож, выясняется что это очень просто.
  
Любой таск сиквенс что содержит следующие "шаги" будет иметь значение 2 в свойстве Type **WMI **класса **SMS_TaskSequencePackage**.

<a href="http://4c74356b41.com/wp-content/uploads/2016/02/SCCM_TS_Type.png" rel="attachment wp-att-4854"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/SCCM_TS_Type-300x162.png" alt="SCCM_TS_Type" width="300" height="162" /></a>

**Собственно шаги:**
  
General – Join Domain or Workgroup;
  
General – Restart Computer (Only “The boot image assigned to this task sequence” option);
  
Disks – Format and Partition Disk;
  
User State – Request State Store;
  
User State – Release State Store;
  
Images – Apply Operating System Image;
  
Images – Setup Windows and ConfigMgr.