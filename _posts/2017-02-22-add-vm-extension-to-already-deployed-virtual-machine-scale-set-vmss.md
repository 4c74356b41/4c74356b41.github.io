---
id: 5714
title: Add VM extension to VMSS (Virtual Machine Scale Set)
date: 2017-02-22T12:38:04+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post5714
permalink: /post5714
categories:
  - Azure
tags:
  - Azure
  - VM extension
  - VMSS
---
Basically, I'm going to show 2 ways of doing that powershell and ARM.

Powershell:

```
$vmss = Get-AzureRmVmss -ResourceGroupName $resourceGroupName
$vmss = $vmss.ToPSVirtualMachineScaleSet()

Add-AzureRmVmssExtension -VirtualMachineScaleSet $vmss -Name “IaaSAntimalware” -Publisher "Microsoft.Azure.Security" -Type "IaaSAntimalware" `
    -TypeHandlerVersion 1.5 -AutoUpgradeMinorVersion $true
Update-AzureRmVmss -ResourceGroupName $resourceGroupName -Name $vmss.name -VirtualMachineScaleSet $vmss -ErrorAction Stop
```

ARM:

```
{
    "$schema": "http://schema.management.azure.com/schemas/2015-01-01-preview/deploymentTemplate.json",
    "contentVersion": "1.0.0.0",
    "parameters": {
        "vmSSName": {
            "type": "string"
        },
        "extensionName": {
            "type": "string",
            "allowedValues": [
                "MSAntiMalware",
                "MSTrendMicro",
                "LinuxTrendMicro"
            ]
        }
    },
    "variables": {
        "MSAntiMalware": [
            {
                "name": "Microsoft.Azure.Security",
                "properties": {
                    "publisher": "Microsoft.Azure.Security",
                    "settings": {
                        "RealtimeProtectionEnabled": "true"
                    },
                    "type": "IaasAntimalware",
                    "typeHandlerVersion": "1.5"
                }
            }
        ],
        "MSTrendMicro": [
            {
                "name": "TrendMicro.DeepSecurity",
                "properties": {
                    "publisher": "TrendMicro.DeepSecurity",
                    "type": "TrendMicroDSA",
                    "typeHandlerVersion": "9.6"
                }
            }
        ],
        "LinuxTrendMicro": [
            {
                "name": "TrendMicro.DeepSecurity",
                "properties": {
                    "publisher": "TrendMicro.DeepSecurity",
                    "type": "TrendMicroDSALinux",
                    "typeHandlerVersion": "9.6"
                }
            }
        ],
        "extensionReference": "[variables(parameters('extensionName'))]"
    },
    "resources": [
        {
            "type": "Microsoft.Compute/virtualMachineScaleSets",
            "apiVersion": "2016-04-30-preview",
            "name": "[parameters('vmSSName')]",
            "location": "[resourceGroup().location]",
            "properties": {
                "overprovision": "true",
                "upgradePolicy": {
                    "mode": "Manual"
                },
                "virtualMachineProfile": {
                    "extensionProfile": {
                        "extensions": "[variables('extensionReference')]"
                    }
                }
            }
        }
    ]
}
```