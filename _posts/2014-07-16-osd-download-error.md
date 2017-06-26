---
id: 1397
title: Ошибка Task Sequence (сценарий OSD) при скачивании файлов
date: 2014-07-16T11:15:13+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post1397
permalink: /post1397
categories:
  - SCCM
tags:
  - Configuration Manager
  - Copypaste
  - Guide
---
**Ошибки**
  
WinHttpSendRequest failed
  
WinHttpRequest failed 80072ee2
  
DownloadFile failed 80072ee2
  
Error downloading file from http://<package location>:80
  
DownloadFiles failed 80072ee2

В случае, если Вы точно уверены что все настроено правильно и проблема не в сети или доступе к файлам, попробуйте добавить в Task Sequnce (где угодно до скачивания файлов) 2 переменные:
  
SMSTSDownloadRetryCount = 5
  
SMSTSDownloadRetryDelay = 15

После этого ошибки пропадут.