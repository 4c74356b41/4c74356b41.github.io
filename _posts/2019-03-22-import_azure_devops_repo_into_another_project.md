---
id: 5791
title: Import Azure Devops repo into another project
date: 2019-03-22
author: rootilo
layout: post
guid: http://4c74356b41.com/post5791
permalink: /post5791
categories:
  - Azure
  - Devops
  - Powershell

---

Howdy,

I needed to "migrate" a bunch of repos from different projects to a new unified project, so I came up with this script. it has some assumptions, like repo name matches project name, same user\token can access both organizations so on so fourth, but you can easily customize it to your needs. Also, if you want to import public github repo, you can just skip the endpoint creation part and slightly edit the json you send to the importRequests endpoint (i didnt find any docs on this, sadly). you just need to pass in `null` to the `serviceEndpointId`.

```
function Import-AzureDevopsRepository {
    [CmdletBinding()]
    Param(
        [Parameter(Mandatory)]
        [string]$sourceName,
        [Parameter(Mandatory)]
        [string]$token,
        
        [string]$targetName = 'my_new_project',
        [string]$username = 'default@organization.com',
        [string]$organization = 'my_organization'
    )
    $base64AuthInfo = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("${username}:$token"))

    $targetUrl = "https://dev.azure.com/$organization/$targetName/_apis"
    $projects = irm "https://dev.azure.com/$organization/_apis/projects?api-version=5.0" -Headers @{Authorization = "Basic $base64AuthInfo"} -ContentType "application/json"
    $targetId = $projects.value | Where-Object { $_.name -eq $targetName } | Select-Object -ExpandProperty id

    # create repo
    $newRepo = irm "$targetUrl/git/repositories?api-version=5.0-preview" -Method:Post -ContentType "application/json" `
        -Headers @{Authorization = "Basic $base64AuthInfo"} `
        -Body ( '{{"name":"{0}","project":{{"id":"{1}"}}}}' -f $sourceName, $targetId )

    # create endpoint
    $endpoint = irm "$targetUrl/serviceendpoint/endpoints?api-version=5.0-preview" -Method:Post -ContentType "application/json" `
        -Headers @{Authorization = "Basic $base64AuthInfo"} `
        -Body ( '{{"name":"temporary-script-git-import","type":"git","url":"https://{3}@dev.azure.com/{3}/{0}/_git/{0}","authorization":{{"parameters":{{"username":"{1}","password":"{2}"}},"scheme":"UsernamePassword"}}}}' -f $sourceName, $username, $token, $organization )

    # import repo
    $importRepo = irm "$targetUrl/git/repositories/$sourceName/importRequests?api-version=5.0-preview" -Method:Post -ContentType "application/json" `
        -Headers @{Authorization = "Basic $base64AuthInfo"} `
        -Body ( '{{"parameters":{{"deleteServiceEndpointAfterImportIsDone":true,"gitSource":{{"url":"https://{2}@dev.azure.com/{2}/{0}/_git/{0}","overwrite":false}},"tfvcSource":null,"serviceEndpointId":"{1}"}}}}' -f $sourceName, $endpoint.id, $organization )

    $newRepo
    $importRepo
    $endpoint
}
```

Happy deploying!