---
id: 5659
title: Azure App Service AlwaysOn webjob
date: 2016-08-17T10:34:45+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post5659
permalink: /post5659
categories:
  - Azure
tags:
  - Azure
---
so yeah, i got really greedy and converted my blog to a shared tier, but it doesn't support AlwaysOn. Well, lets fix that.

Just créate a webjob with the following script (you have to name it something.ps1)

```
$url = 'url goes here'
while ($url) {

    $wc = New-Object System.Net.WebClient
    [void]$wc.DownloadString($url)
    Write-Output "Info:Success"
    Start-Sleep 550

}
```