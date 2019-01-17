---
id: 5781
title: Start\stop Azure resources based on tags
date: 2019-01-13T19:10:00+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post5781
permalink: /post5781
categories:
  - Azure
  - Powershell
---

Howdy,

I needed to come up with a solution to start\stop resources in Azure based on tags. The solutions that existed there I didnt really like due to various reasons (like, the official MS way to do it requires you to have tags that are absolutely incomprehensible ), and none of the ones I've found would work with anything except virtual machines. The runbook isnt perfect, it could use better error handling\reporting, but this worked fine for me for quite a long time with next to no errors. Another neat thing about this runbook - it allows to delay start up of some resources (think webservers after database servers).

My solution is a fairly simple runbook (that runs hourly) that can start\stop classic virtual machines, virtual machines, virtual machine scale sets, and application gateways based on a really simple\intuitive tag:

```
{
    "UTC": "+3",
    "weekdays": "8-20",
    "weekends": "7-22",
    "ignore": "weekdays,weekends",
    "delayed": "yes"
}
```

The tag has to be in English. You can only edit the values of the properties. Property names cannot be changed.
If the entity doesnt need to be a part of the process simply do not create a schedule tag for the entity. If the tag exists, it will get evaluated and the entity will be shutdown or started depending on the current time and tag data. You can choose 2 sets of schedules for your entity: one for weekdays (Monday-Friday), one for weekends
(Saturday-Sunday). You can also choose to ignore certain days, certain days of the week, weekends, weekdays or combination of those.

## Properties

**UTC** = hour offset from UTC 0 you want to use in calculations (put your current UTC offset and you can use your local time for shutdown-startup time), this is implemented for user convenience. You can use positive or negative offset  
**weekdays** = start-stop (24hr) time for Monday-Friday  
**weekends** = start-stop (24hr) time for Saturday-Sunday  
**delayed** = apply a 10 minute delay before starting the entity, assigning any value to this tag applies this behavior, you can omit this property for a resource if its not needed    
**ignore** = what to ignore. you can choose to ignore weekends or weekdays, specific day(s) of the week (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday),
and you can use any specific date (23 february, 12 jun, 1 jan). They have to be comma separated (strictly) or the ignore tag will not work.
You may also choose to ignore start or stop operation using "start" and\or "stop".  
To ignore schedule tag completely you can use this value: "weekends, weekdays" or delete the tag.
 
The actual json used in the tag should be minified.
Schedule tag wont pass verification if time difference between start and stop is greater than 20 hours.

## Tagging

Azure Cli:
You can use the following command to add tag to an existing vm.
```
az vm update -g MyRG -n MyVM --set tags.schedule='{"UTC":"+5","weekdays":"7-22","weekends":"7-22","ignore":"29 dec, weekends, monday"}'
```

ARM Template:
You can use the `tags` property in the ARM Template resource definition to add\create a tag to a resource.
```
{
    "apiVersion": "2017-03-30",
    "type": "Microsoft.Compute/virtualMachines",
    "name": "MyVM", 
    "location": "location",
    "dependsOn": [ ... ],
    "tags": {
        "schedule": "{\"UTC\":\"+3\",\"weekdays\":\"7-19\",\"weekends\":\"10-16\",\"ignore\":\"weekends, 25 dec, Monday\"}"
    },
    "properties": { ... }
}
```

Powershell:
You can use the following powershell snippet to add a tag to existing VM. Adjust first 3 lines to your specific needs.
```
$vmName = 'MyVM'
$rg = 'MyRG'
$schedule = @{ UTC = "+5"; weekdays = "7-22"; weekends = "7-22"; ignore = "29 dec, weekends, monday" } | ConvertTo-Json -Compress
  $tags = (Get-AzureRmResource -ResourceGroupName $rg -Name $vmName -ResourceType "Microsoft.Compute/VirtualMachines").Tags
$tags += @{schedule=$schedule}
Set-AzureRmResource -ResourceGroupName $rg -Name $vmName -ResourceType "Microsoft.Compute/VirtualMachines" -Tag $tags
``` 
This example creates minified json from the hash representing the proper json object
```
$schedule = @{ UTC = "+5"; weekdays = "7-22"; weekends = "7-22"; ignore = "29 dec, weekends, monday" } | convertto-json -compress
$schedule
```

Portal:
1. Create a valid json ressembling the example above in any editor of your choice:
2. Minify it. Use any minifying service. Usually they will validate the json as well (if it throws validation errors - fix it). The reason for this is that you cannot use linebreaks in the tag name or value, and value is limited to 256 characters, so minifying json works around both of these limitations.
3. Create a tag with the name `schedule` and use minified json string as the value for the tag

## Runbook

```powershell
function send-teamsmessage( $message ) {
    $message
    $splat = @{
        uri         = $uri
        method      = 'Post'
        body        = ConvertTo-Json -Compress @{ text = $message }
        erroraction = 'Ignore'
    }
    Invoke-RestMethod @splat | Out-Null
}

function compare-time( $actual ) {
    if ( $actual -match ',' ) {
        $result = $actual.Split(',').Trim() | ForEach-Object { parse-time $_ }
    }
    else {
        $result = parse-time $actual
    }
    if ($result) { $true }
}

function parse-time( $inputillo ) {
    try {
        $inputillo = (Get-Date $inputillo).DayOfYear
    } 
    catch {
        "Not Datetime" | Out-Null
    }
    if ( $inputillo -eq $timeDate.week -or $inputillo -eq $timeDate.day -or $inputillo -eq $timeDate.year ) {
        $true
    }
    if ( $inputillo -eq 'start') {
        $global:entityStart = $false
    }
    if ( $inputillo -eq 'stop') {
        $global:entityStop = $false
    }
}

function parse-entity( $inputillo ) {
    try {
        $action = $null; $global:entityStop = $global:entityStart = $true
        $schedule = $inputillo.schedule | ConvertFrom-Json -ErrorAction Stop
        if ( compare-time $schedule.ignore ) {
            "Skipped: {0}." -f $inputillo.Id
            continue
        }
        $data = $schedule.($timeDate.week)
        [int]$start, [int]$stop = $data.Split("-")
        $currentHour = $timeDate.hour + [int]$schedule.UTC
        if ( $currentHour -lt 0 ) { # there is possibly a better way of doing this, but this works
            $currentHour = $currentHour + 24
        }
        if ( $currentHour -gt 23 ) {
            $currentHour = $currentHour - 24
        }
        if ( ( $start - $stop ) -eq 0 -or ( $start - $stop ) -ge 20 ) {
            $global:messages += "Error: Malformed Start\Stop at {0}" -f $inputillo.Id
            continue
        }
        if ( $currentHour -eq $stop -and $global:entityStop ) {
            $action = $mapper[$inputillo.Type].action
        }
        elseif ( $currentHour -eq $start -and $global:entityStart ) {
            $action = "Start"
        }
        if ( $action ) { 
            $global:processed += New-Object -TypeName psobject -Property @{
                action = $action
                apiVer = $mapper[$inputillo.Type].apiver
                delay  = $( if ( $schedule.delayed ) { $true } else { $false } )
                id     = $inputillo.id
            }
        }
    }
    catch {
        $global:messages += "Error: Malformed JSON at {0}" -f $inputillo.Id
    }
}

function process-entity( $inputillo, $header ) {
    try {
        "Performing action {0} on {1}" -f $inputillo.action, $inputillo.Id
        $uri = "https://management.azure.com{0}/{1}?api-version={2}" -f $inputillo.Id, $inputillo.action, $inputillo.apiVer
        $global:requests += Invoke-WebRequest -Headers $header -Method Post -Uri $uri -UseBasicParsing | Add-Member @{ id = $inputillo.Id } -PassThru
    }
    catch {
        Write-Error $_
        $global:messages += "Error: start\stop operation failed at {0}" -f $inputillo.id
        $retries += $inputillo
    }
}

# Initialize variables 
$uri = Get-AutomationVariable -Name 'teamsWebhookUri' # this is needed to send notification to teams
$all = $processed = $requests = $messages = $retries = @(); $startTime = Get-Date; [Int32]$maxRetry = 5; [Int32]$retry = 0
$mapper = @{
    'Microsoft.Network/applicationGateways'     = @{
        action = 'stop'
        apiver = '2017-04-01'
    }
    'Microsoft.Compute/virtualMachines'         = @{
        action = 'deallocate'
        apiver = '2017-03-30'
    }
    'Microsoft.Compute/virtualMachineScaleSets' = @{
        action = 'deallocate'
        apiver = '2017-03-30'
    }
    'Microsoft.ClassicCompute/virtualMachines'  = @{
        action = 'shutdown'
        apiver = '2017-04-01'
    }
}
$timeDate = New-Object psobject -Property @{
    hour = $startTime.ToUniversalTime().Hour
    day  = $startTime.DayOfWeek
    week = if ($startTime.DayOfWeek -notin "Sunday", "Saturday") { "weekdays" } else { "weekends" }
    year = $startTime.DayOfYear
}

do { # Connect to Azure
    $Error.Clear(); $retry++;
    $servicePrincipalConnection = Get-AutomationConnection -Name "vm-start-stop"
    Add-AzureRmAccount -ServicePrincipal -TenantId $servicePrincipalConnection.TenantId `
        -CertificateThumbprint $servicePrincipalConnection.CertificateThumbprint `
        -ApplicationId $servicePrincipalConnection.ApplicationId | Out-Null
    $token = (Get-AzureRmContext).TokenCache.ReadItems() | Select-Object -First 1 -ExpandProperty AccessToken
    $header = @{ Authorization = "Bearer $token" }

    (Get-AzureRmSubscription).Where{ $_.name -notmatch 'prd|prod' }.foreach{ # Get resources except production\stale subs
        Select-AzureRmSubscription $PSItem | Out-Null
        $resources = Get-AzureRmResource -ODataQuery "`$filter=tagname eq 'schedule'" -ExpandProperties
        $cvms = (Get-AzureRmResourceGroup).Where{ $_.tags.classicSchedule }.foreach{
            $schedule = $_.tags.classicSchedule
            Get-AzureRmResource -ResourceType Microsoft.ClassicCompute/virtualMachines -ResourceGroupName $_.ResourceGroupName |
                Add-Member @{ Tags = @{ schedule = $schedule } } -PassThru -Force
        }
        $all += ($resources, $cvms).foreach{ # Build array of resources to iterate over
            $PSItem | ForEach-Object {
                [psobject]@{
                    Type     = $_.ResourceType
                    Id       = $_.ResourceId
                    Schedule = $_.Tags.schedule
                }   
            }
        }
    }
} while ( $Error.Count -gt 0 -and $maxRetry -ge $retry)

if ( $Error.Count -gt 0 ) { send-teamsmessage ( "{0} FATAL: runbook failed. {1}" -f (Get-Date), $Error[0] ) } # possibly exit here

try {
    "Parsing {0} resource entities" -f $all.Count
    # Runbook payload begins here
    foreach ( $entity in $all ) { parse-entity $entity }
    $processed.where{ $_.Delay -ne $true -or $_.Action -ne 'Start' }.foreach{ process-entity $PSItem $header}
    if ( $processed.where{ $_.Delay -eq $true -and $_.Action -eq 'Start' } ) {
        # Waiting before processing delayed resources
        Start-Sleep -Seconds 600
        $processed.where{ $_.Delay -eq $true -and $_.Action -eq 'Start' }.foreach{ process-entity $PSItem $header }
    }
}
catch {
    # Possibly restart runbook and\or determine state and restart failed
    Write-Error $_
    send-teamsmessage ( "{0} FATAL: runbook failed. {1}" -f (Get-Date), $PSItem )
}

if ( $retries ) {
    $retries.foreach{ process-entity $PSItem $header }
}

if ( $messages ) {
    $messages
    send-teamsmessage ("examine start\stop job state at {1}" -f (Get-Date))
}

```

Powershell snippet to create a role with minimum required permissions:

```powershell
$subs = Get-AzureRmSubscription

# Resource start\stop role
$role = Get-AzureRmRoleDefinition "Virtual Machine Contributor"
$role.Id = $null
$role.Name = "Resource Start/Stop (Scheduled)"
$role.Description = "Can read\start\stop VMs, VMSSs, Application Gateways, and read resource groups"
$role.Actions.Clear()
$role.Actions.Add("Microsoft.ClassicCompute/virtualMachines/read")
$role.Actions.Add("Microsoft.ClassicCompute/virtualMachines/start/action")
$role.Actions.Add("Microsoft.ClassicCompute/virtualMachines/shutdown/action")
$role.Actions.Add("Microsoft.ClassicCompute/virtualMachines/operationStatuses/read")
$role.Actions.Add("Microsoft.Compute/virtualMachines/deallocate/action")
$role.Actions.Add("Microsoft.Compute/virtualMachines/read")
$role.Actions.Add("Microsoft.Compute/virtualMachines/restart/action")
$role.Actions.Add("Microsoft.Compute/virtualMachines/start/action")
$role.Actions.Add("Microsoft.Compute/virtualMachineScaleSets/read")
$role.Actions.Add("Microsoft.Compute/virtualMachineScaleSets/start/action")
$role.Actions.Add("Microsoft.Compute/virtualMachineScaleSets/deallocate/action")
$role.Actions.Add("Microsoft.Network/applicationGateways/read")
$role.Actions.Add("Microsoft.Network/applicationGateways/start/action")
$role.Actions.Add("Microsoft.Network/applicationGateways/stop/action")
$role.Actions.Add("Microsoft.Resources/subscriptions/resourceGroups/read")
$role.AssignableScopes.Clear()
$subs | ForEach-Object {
    $scope = "/subscriptions/{0}" -f $_.Id
    $role.AssignableScopes.Add($scope)
}
$def = New-AzureRmRoleDefinition -Role $role

$subs | ForEach-Object {
    $_ | Select-AzureRmSubscription
    New-AzureRmRoleAssignment -ObjectId your_runbook_service_principal_object_id -RoleDefinitionId $def.id -Scope "/subscriptions/$($_.id)"
}
```

Happy deploying!