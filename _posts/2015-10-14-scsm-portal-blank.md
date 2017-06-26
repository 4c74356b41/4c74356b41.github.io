---
id: 3511
title: 'портал самообслуживания SCSM "белый"'
date: 2015-10-14T12:21:40+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post3511
permalink: /post3511
categories:
  - System Center
tags:
  - Copypaste
  - Service Manager
  - Troubleshooting
---
1. Проверьте сертификат, он не должен выдавать ошибок на клиенте. На клиенте должна успешно открываться ссылка https://<scsmportalname>/contenthost/clientbin/settings.xml
  
<img src="https://msdnshared.blob.core.windows.net/media/TNBlogsFS/prod.evol.blogs.technet.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/62/41/metablogapi/3326.image_7CE0683A.png" alt="" width="574" height="327" />
  
2. В менеджере IIS проверьте Application Settings у сайта Service Manager, поле SMPortal\_WebContentServer\_URL должно соответствовать тому адресу, по-которому Вы открываете портал (если FQDN - то FQDN, если NETBIOS то и в этом поле тоже NETBIOS). В конфиг файле сайта (диск:inetpubwwwrootwssVirtualDirectoriesService Manager Portal) тот же самый ключ должен иметь точно такое же значение "value"
  
<img id="7918120a-a928-4720-8dc4-381ae77b386f" title="Editing SharePoint Web Config File for the WCS URL" src="https://i-technet.sec.s-msft.com/dynimg/IC559634.jpeg" alt="Editing SharePoint Web Config File for the WCS URL" />
  
3. Проверьте что MIME Type .xap соответствует значению "application/x-silverligh-app".
  
Ссылки:
  
https://technet.microsoft.com/en-us/library/hh667345.aspx<br /> https://technet.microsoft.com/en-us/library/hh667343.aspx<br /> https://technet.microsoft.com/en-us/library/hh667347.aspx<br /> http://blogs.technet.com/b/servicemanager/archive/2012/05/04/faq-why-is-my-self-service-portal-service-catalog-blank.aspx - почти тоже самое подробно.

Ну и еще по мелочи, как настроить переадресацию портала:
  
https://memoexp.wordpress.com/2011/03/30/changing-scsm-portal-address/<br /> http://blogs.msdn.com/b/kaushal/archive/2013/05/23/http-to-https-redirects-on-iis-7-x-and-higher.aspx<br /> http://systemcenterservicemanager.blogspot.ru/2011/07/four-scsm-self-service-portal-solution.html

пс. Натыкал картинок из интернетов, свои делать лень, прощенья просим.