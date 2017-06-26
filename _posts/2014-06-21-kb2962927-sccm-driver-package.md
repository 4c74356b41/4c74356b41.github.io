---
id: 623
title: 'KB2962927 SCCM: Невозможно распространить driver package на pull DP'
date: 2014-06-21T15:32:24+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post623
permalink: /post623
categories:
  - SCCM
tags:
  - Configuration Manager
  - Copypaste
  - Guide
---
Если Вы встречаете подобные ошибки при попытке распространить пакет драйвера на pull DP (только)
  
CreateFolder failed; 0x8007007b
  
CContentDefinition::ExpandContentDefinitionItems failed; 0x8007007b
  
CContentDefinition::Expand failed; 0x8007007b
  
Проблема проявляется если в пути используется "" и используется кастомное имя сетевой папки.
  
В этом случае Вам вот [сюда](http://support.microsoft.com/kb/2962927).