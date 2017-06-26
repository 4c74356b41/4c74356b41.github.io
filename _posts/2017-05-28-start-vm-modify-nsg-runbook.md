---
id: 5771
title: Start a VM and modify NSG with a Runbook
date: 2017-05-28T11:20:53+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post5771
permalink: /post5771
categories:
  - Azure
tags:
  - Azure
  - Azure Automation
  - Azure Portal
  - Azure Resource Manager
  - PowerShell
---
So I decided to move my development machine to Azure and I'm a bit worried by the fact that the RDP is wide open to all the evil guys out there (as I ofter work from different places and the IP is never static in those places, I cannot just pre create NSG rule to fix that).

Also, I felt like running the VM 24\7 is a bit of an overkill, so I decided to fix myself a runbook to take care of those concerns. You could also use autoshutdown as part of the solution (I'm using both)
  
The runbook would turn the VM on or off (depending on the state of the VM), and edit the NSG rule with my current external IP address.

Prereq: the VM you want to toggle and the NSG created for the VM with the rule to edit with your external IP.
  
I won't go through all the steps with extreme detail, but I will give out links and code to achieve the end goal.

  1. [Create a powershell runbook](https://docs.microsoft.com/en-us/azure/automation/automation-creating-importing-runbook) (not workflow).
  2. [Insert](https://docs.microsoft.com/en-us/azure/automation/automation-edit-textual-runbook) the code snippet (at the end of the post), adjust it to your values.
  3. [Publish the runbook](https://docs.microsoft.com/en-us/azure/automation/automation-creating-importing-runbook#to-publish-a-runbook-using-the-azure-portal)
  4. [Create a webhook for your runbook](https://docs.microsoft.com/en-us/azure/automation/automation-webhooks)
  5. Create a powershell function to launch it (or alternatively create function in your preferred language, basically all you have to do is call an URL and pass in json as parameter)

Add this function to you powershell profile and you could run it to start\stop the VM when you need.

```
function develop-me {
	$webhook = 'url-from-when-you-create-the-webhook'
	$whbody  = @{ tada = ((iwr httpbin.org/ip).content | convertfrom-json).origin } | ConvertTo-Json
	Invoke-RestMethod -Method Post -Uri $webhook -Body $whbody
}
```

You could also create an [auto-shutdown resource for the vm](http://4c74356b41.com/post5698), so it always shuts off when you go to sleep.

And the runbook code:

```
param (
        [object]$WebhookData
    )

$weeha = ( $WebhookData.RequestBody | ConvertFrom-Json ).tada
function toggleVM($inputto) {
    $connectionName = "AzureRunAsConnection" # this is the default connection created when you provision the Automation account,
                                             # you might need to change this to your own connection name
    $servicePrincipalConnection = Get-AutomationConnection -Name $connectionName         

    $null = Add-AzureRmAccount `
        -ServicePrincipal `
        -TenantId $servicePrincipalConnection.TenantId `
        -ApplicationId $servicePrincipalConnection.ApplicationId `
        -CertificateThumbprint $servicePrincipalConnection.CertificateThumbprint

    $null = Select-AzureRmSubscription -SubscriptionId 'SUB_GUID' ` # Needed if you have more than 1 subscription
    $vm = Get-AzureRmVM -ResourceGroupName %rg_name% -Name %vm_name% -Status
    if ($vm.Statuses.code -contains 'powerstate/deallocated') {
        Start-AzureRmVM -Name $vm.Name -ResourceGroupName $vm.ResourceGroupName
        $nsg = Get-AzureRmNetworkSecurityGroup -ResourceGroupName $vm.ResourceGroupName -Name %nsg_name%
        Set-AzureRmNetworkSecurityRuleConfig -NetworkSecurityGroup $nsg `
            -Name %rule-name% `
            -Access Allow `
            -Protocol Tcp `
            -Direction Inbound `
            -Priority 777 `
            -SourceAddressPrefix $inputto `
            -SourcePortRange * `
            -DestinationAddressPrefix * `
            -DestinationPortRange 3389
        $null = Set-AzureRmNetworkSecurityGroup -NetworkSecurityGroup $nsg
    }
    else {
        Stop-AzureRmVM -Name $vm.Name -ResourceGroupName $vm.ResourceGroupName -Force
    }
}
toggleVM $weeha
```

You could easily parametrize this to start-stop any VM (and edit rules as well).
  
Happy developing.
