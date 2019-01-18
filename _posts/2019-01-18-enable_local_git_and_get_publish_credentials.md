---
id: 5783
title: Enable Local Git and get Publish Credentials
date: 2019-01-18
author: rootilo
layout: post
guid: http://4c74356b41.com/post5783
permalink: /post5783
categories:
- Azure
- Powershell

---

Howdy,

answering random questions about web apps (I totally hate webapps).


Get publish profile to learn ftp user\password
```
$rg = 'xxx'
$webAppName = 'yyy'
[xml]$publishProfile = Get-AzWebAppPublishingProfile -ResourceGroupName $rg -Name $webAppName
```

Enable local git on the web app
```
$webApp = Get-AzResource -ResourceGroupName $rg -ResourceType Microsoft.Web/sites/config -ResourceName "$webAppName/web" -ApiVersion 2018-02-01 -ExpandProperties
$webApp.properties.scmtype = 'localgit'
Set-AzResource -PropertyObject $webApp.properties -ResourceId $webApp.ResourceId -ApiVersion 2018-11-01
```

Data:

```
url: https://$webAppName.scm.azurewebsites.net:443/$webAppName.git
userName: $publishProfile.publishData.publishProfile[1].userName
password: $publishProfile.publishData.publishProfile[1].userPWD
```

Happy deploying!