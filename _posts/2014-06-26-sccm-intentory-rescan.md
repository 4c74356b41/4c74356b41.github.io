---
id: 804
title: Запуск Hardware Inventory на клиенте SCCM
date: 2014-06-26T11:13:08+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post804
permalink: /post804
categories:
  - SCCM
tags:
  - Configuration Manager
  - Copypaste
  - Guide
---
Иногда Вам необходимо осуществить запуск не делты, а полного обнаружения Hardware Inventory.

1. Запустите wbemtest от имени администратор;<a href="http://4c74356b41.com/wp-content/uploads/2016/02/sccm_hw_full_01.png" rel="attachment wp-att-4832"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/sccm_hw_full_01-300x233.png" alt="sccm_hw_full_01" width="300" height="233" /></a>

2. Нажмите "Connect';
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/sccm_hw_full_02.png" rel="attachment wp-att-4835"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/sccm_hw_full_02-289x300.png" alt="sccm_hw_full_02" width="289" height="300" /></a>

3. Введите "rootccminvagt" в поле "Namespace"
  
4. Нажмите "Enum Classes"
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/sccm_hw_full_03.png" rel="attachment wp-att-4839"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/sccm_hw_full_03-300x233.png" alt="sccm_hw_full_03" width="300" height="233" /></a>

5. Выберите "Recursive" и нажмите "OK"
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/sccm_hw_full_04.png" rel="attachment wp-att-4842"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/sccm_hw_full_04-300x134.png" alt="sccm_hw_full_04" width="300" height="134" /></a>

6. Найдите "InventoryActionStatus" и дважды кликните по нему мышкой;
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/sccm_hw_full_00.png" rel="attachment wp-att-4829"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/sccm_hw_full_00-300x182.png" alt="sccm_hw_full_00" width="300" height="182" /></a>

7. Выберите "Instances"
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/sccm_hw_full_05.png" rel="attachment wp-att-4845"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/sccm_hw_full_05-300x258.png" alt="sccm_hw_full_05" width="300" height="258" /></a>

8. Выберите соответствующий ващем нуждам GUID и сотрите его;
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/sccm_hw_full_06.png" rel="attachment wp-att-4848"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/sccm_hw_full_06-300x179.png" alt="sccm_hw_full_06" width="300" height="179" /></a>
  
Hardware Inventory - {00000000-0000-0000-0000-000000000001}
  
Software Inventory - {00000000-0000-0000-0000-000000000002}
  
Data Discovery Record - {00000000-0000-0000-0000-000000000003}
  
File Collection - {00000000-0000-0000-0000-000000000010}

9. Удостоверьтесь что происходит полное обновление Hardware Inventory;
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/sccm_hw_full_07.png" rel="attachment wp-att-4851"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/sccm_hw_full_07-300x121.png" alt="sccm_hw_full_07" width="300" height="121" /></a>

Наслаждайтесь! 😉