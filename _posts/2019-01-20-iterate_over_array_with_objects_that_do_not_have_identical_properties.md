---
id: 5784
title: Iterate over array with objects that do not have identical properties inside ARM Templates
date: 2019-01-20
author: rootilo
layout: post
guid: http://4c74356b41.com/post5784
permalink: /post5784
categories:
- Azure
- Arm Templates

---

Howdy,

I needed to come up with a solution on how to iterate an array where objects have different properties, here's what I came up with:

```
{
    "$schema": "https://schema.management.azure.com/schemas/2015-01-01/deploymentTemplate.json#",
    "contentVersion": "1.0.0.0",
    "parameters": {
        "deploymentPrefix": {
            "type": "string"
        },
        "subnets": {
            "type": "array",
            "defaultValue": [
                {
                    "name": "GatewaySubnet",
                    "addressPrefix": "10.2.0.0/24",
                    "networkSecurityGroup": "NSG-AllowAll", // these have to be different only because I'm creating them in the same template, these can be identical
                    "routeTable": "UDR-Default"
                },
                {
                    "name": "UnTrusted",
                    "addressPrefix": "10.2.1.0/24",
                    "networkSecurityGroup": "NSG-AllowAll1" // these have to be different only because I'm creating them in the same template, these can be identical
                },
                {
                    "name": "routed",
                    "addressPrefix": "10.2.2.0/24",
                    "routeTable": "UDR-Default1"
                }
            ]
        }
    },
    "variables": {
        "copy": [
            {
                "name": "subnetsBase",
                "count": "[length(parameters('subnets'))]",
                "input": {
                    "name": "[concat('subnet-', parameters('subnets')[copyIndex('subnetsBase')].name)]",
                    "properties": {
                        "addressPrefix": "[parameters('subnets')[copyIndex('subnetsBase')].addressPrefix]"
                    }
                }
            },
            {
                "name": "subnetsUDR",
                "count": "[length(parameters('subnets'))]",
                "input": {
                    "routeTable": {
                        "id": "[if(contains(parameters('subnets')[copyIndex('subnetsUDR')], 'routeTable'), resourceId('Microsoft.Network/routeTables', parameters('subnets')[copyIndex('subnetsUDR')].routeTable), 'skip')]"
                    }
                }
            },
            {
                "name": "subnetsNSG",
                "count": "[length(parameters('subnets'))]",
                "input": {
                    "networkSecurityGroup": {
                        "id": "[if(contains(parameters('subnets')[copyIndex('subnetsNSG')], 'networkSecurityGroup'), resourceId('Microsoft.Network/networkSecurityGroups', parameters('subnets')[copyIndex('subnetsNSG')].networkSecurityGroup), 'skip')]"
                    }
                }
            }
        ]
    },
    "resources": [
        {
            "condition": "[not(contains(variables('subnetsNSG')[copyIndex()].networkSecurityGroup.id, 'skip'))]",
            "apiVersion": "2017-06-01",
            "name": "[if(contains(parameters('subnets')[copyIndex()], 'networkSecurityGroup'), parameters('subnets')[copyIndex()].networkSecurityGroup, 'skip')]",
            "location": "[resourceGroup().location]",
            "type": "Microsoft.Network/networkSecurityGroups",
            "copy": {
                "name": "nsg",
                "count": "[length(parameters('subnets'))]"
            },
            "properties": {
                "securityRules": []
            }
        },
        {
            "condition": "[not(contains(variables('subnetsUDR')[copyIndex()].routeTable.id, 'skip'))]",
            "type": "Microsoft.Network/routeTables",
            "name": "[if(contains(parameters('subnets')[copyIndex()], 'routeTable'), parameters('subnets')[copyIndex()].routeTable, 'skip')]",
            "apiVersion": "2017-10-01",
            "location": "[resourceGroup().location]",
            "copy": {
                "name": "udr",
                "count": "[length(parameters('subnets'))]"
            },
            "properties": {
                "routes": []
            }
        },
        {
            "apiVersion": "2017-06-01",
            "type": "Microsoft.Network/virtualNetworks",
            "name": "[concat(parameters('deploymentPrefix'), '-vNet')]",
            "location": "[resourceGroup().location]",
            "dependsOn": [
                "nsg",
                "udr"
            ],
            "properties": {
                "addressSpace": {
                    "addressPrefixes": [
                        "10.2.0.0/16"
                    ]
                },
                "copy": [
                    {
                        "name": "subnets",
                        "count": "[length(parameters('subnets'))]",
                        "input": {
                            "name": "[concat('subnet-', parameters('subnets')[copyIndex('subnets')].name)]",
                            "properties": "[union(variables('subnetsBase')[copyIndex('subnets')].properties, if(equals(variables('subnetsUDR')[copyIndex('subnets')].routetable.id, 'skip'), variables('subnetsBase')[copyIndex('subnets')].properties, variables('subnetsUDR')[copyIndex('subnets')]), if(equals(variables('subnetsNSG')[copyIndex('subnets')].networkSecurityGroup.id, 'skip'), variables('subnetsBase')[copyIndex('subnets')].properties, variables('subnetsNSG')[copyIndex('subnets')]))]"
                        }
                    }
                ]
            }
        }
    ]
}
```

What happens here is we assemble all the needed objects (together with unneeded) and then we discard unneeded objects using `if()` and `union()` functions. More context:

1. https://stackoverflow.com/questions/54291778/how-to-use-jagged-objects-in-azure-resource-manger-templates-to-iterate-over-t/54292381#54292381
2. https://stackoverflow.com/questions/54277322/iterate-over-not-existing-azure-resource-manager-arm-object-properties/54278741#54278741

Happy deploying!