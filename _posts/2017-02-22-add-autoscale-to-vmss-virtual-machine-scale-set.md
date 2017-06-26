---
id: 5717
title: Add autoscale to VMSS (Virtual Machine Scale Set)
date: 2017-02-22T12:47:38+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post5717
permalink: /post5717
categories:
  - Azure
tags:
  - Azure
  - VMSS
---
A simple way to add autoscale to your VMSS.
Obviously, you can tweak the rules as you want.

Powershell:

```
$vmss = Get-AzureRmVmss -ResourceGroupName $resourceGroupName
$vmss = $vmss.ToPSVirtualMachineScaleSet()
$path = "/subscriptions/$subscription/resourceGroups/$resourceGroupName/providers/Microsoft.Compute/virtualMachineScaleSets/$($vmss.name)"

$r1 = New-AzureRmAutoscaleRule -MetricName "Percentage CPU" -MetricResourceId $path -Operator GreaterThan -MetricStatistic Average -Threshold 0.01 `
    -TimeGrain 00:01:00 -TimeWindow 00:10:00 -ScaleActionCooldown 00:10:00 -ScaleActionDirection Increase -ScaleActionScaleType ChangeCount -ScaleActionValue 1
$r2 = New-AzureRmAutoscaleRule -MetricName "Percentage CPU" -MetricResourceId $path -Operator GreaterThan -MetricStatistic Average -Threshold 2 `
    -TimeGrain 00:01:00 -TimeWindow 00:10:00 -ScaleActionCooldown 00:10:00 -ScaleActionDirection Decrease -ScaleActionScaleType ChangeCount -ScaleActionValue 1
$pr1 = New-AzureRmAutoscaleProfile -DefaultCapacity 2 -MaximumCapacity 10 -MinimumCapacity 2 -Rules $r1,$r2 -Name "MyProfile"
Add-AzureRmAutoscaleSetting -Location $location -Name "Autoscale" -ResourceGroup $resourceGroupName -TargetResourceId $path -AutoscaleProfiles $pr1 -ErrorAction Stop
```

ARM:

```
{
    "$schema": "http://schema.management.azure.com/schemas/2015-01-01/deploymentTemplate.json",
    "contentVersion": "1.0.0.0",
    "parameters": {
        "vmSSName": {
            "type": "string"
        }
    },
    "variables": {
        "insightsApiVersion": "2015-04-01"
    },
    "resources": [
        {
            "type": "Microsoft.Insights/autoscaleSettings",
            "apiVersion": "[variables('insightsApiVersion')]",
            "name": "cpuautoscale",
            "location": "[resourceGroup().location]",
            "properties": {
                "name": "cpuautoscale",
                "targetResourceUri": "[concat('/subscriptions/',subscription().subscriptionId, '/resourceGroups/',  resourceGroup().name, '/providers/Microsoft.Compute/virtualMachineScaleSets/', parameters('vmSSName'))]",
                "enabled": true,
                "profiles": [
                    {
                        "name": "Profile1",
                        "capacity": {
                            "minimum": "1",
                            "maximum": "10",
                            "default": "1"
                        },
                        "rules": [
                            {
                                "metricTrigger": {
                                    "metricName": "Percentage CPU",
                                    "metricNamespace": "",
                                    "metricResourceUri": "[concat('/subscriptions/',subscription().subscriptionId, '/resourceGroups/',  resourceGroup().name, '/providers/Microsoft.Compute/virtualMachineScaleSets/', parameters('vmSSName'))]",
                                    "timeGrain": "PT1M",
                                    "statistic": "Average",
                                    "timeWindow": "PT5M",
                                    "timeAggregation": "Average",
                                    "operator": "GreaterThan",
                                    "threshold": 50
                                },
                                "scaleAction": {
                                    "direction": "Increase",
                                    "type": "ChangeCount",
                                    "value": "1",
                                    "cooldown": "PT5M"
                                }
                            },
                            {
                                "metricTrigger": {
                                    "metricName": "Percentage CPU",
                                    "metricNamespace": "",
                                    "metricResourceUri": "[concat('/subscriptions/',subscription().subscriptionId, '/resourceGroups/',  resourceGroup().name, '/providers/Microsoft.Compute/virtualMachineScaleSets/', parameters('vmSSName'))]",
                                    "timeGrain": "PT1M",
                                    "statistic": "Average",
                                    "timeWindow": "PT5M",
                                    "timeAggregation": "Average",
                                    "operator": "LessThan",
                                    "threshold": 30
                                },
                                "scaleAction": {
                                    "direction": "Decrease",
                                    "type": "ChangeCount",
                                    "value": "1",
                                    "cooldown": "PT5M"
                                }
                            }
                        ]
                    }
                ]
            }
        }
    ]
}
```