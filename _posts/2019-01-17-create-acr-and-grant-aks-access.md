---
id: 5782
title: Create ACR and grant AKS access to pull images
date: 2019-01-17
author: rootilo
layout: post
guid: http://4c74356b41.com/post5782
permalink: /post5782
categories:
  - Azure
  - Kubernetes
  - Containers
---

Howdy,

I needed to create ACR along with AKS and grant AKS access to pull ACR images with a template. This isn't particularly tricky, the only caveat is that you have to give it service principal objectId, not applicationId of your AKS application. Template cannot find that out - so you need to calculate that outside of the template.

```
{
    "$schema": "https://schema.management.azure.com/schemas/2015-01-01/deploymentTemplate.json#",
    "contentVersion": "1.0.0.0",
    "parameters": {
        "deploymentPrefix": {
            "type": "string"
        },
        "acrId": {
            "type": "string"
        },
        "azureClientObjectId": {
            "type": "secureString"
        }
    },
    "variables": {
        "acrSplit": "[split(parameters('acrId'), '/')]",
        "acrName": "[concat(replace(parameters('deploymentPrefix'), '-', ''), 'cr')]",
        "acrGuid": "[resourceId('Microsoft.ContainerRegistry/registries', variables('acrName'))]"
    },
    "resources": [
        {
            "condition": "[contains(parameters('acrId'), 'fake')]",
            "name": "[variables('acrName')]",
            "type": "Microsoft.ContainerRegistry/registries",
            "apiVersion": "2017-10-01",
            "location": "[resourceGroup().location]",
            "sku": {
                "name": "Basic",
                "tier": "Basic"
            },
            "properties": {
                "adminUserEnabled": false
            }
        },
        {
            "type": "Microsoft.Resources/deployments",
            "name": "acr-role-assignment",
            "apiVersion": "2017-05-10",
            "resourceGroup": "[if(contains(parameters('acrId'), 'fake'), resourceGroup().name, variables('acrSplit')[4])]",
            "subscriptionId": "[if(contains(parameters('acrId'), 'fake'), subscription().subscriptionId, variables('acrSplit')[2])]",
            "dependsOn": [
                "[variables('acrName')]"
            ],
            "properties": {
                "mode": "Incremental",
                "template": {
                    "$schema": "https://schema.management.azure.com/schemas/2015-01-01/deploymentTemplate.json#",
                    "contentVersion": "1.0.0.0",
                    "resources": [
                        {
                            "type": "Microsoft.ContainerRegistry/registries/providers/roleAssignments",
                            "apiVersion": "2017-05-01",
                            "name": "[concat(if(contains(parameters('acrId'), 'fake'), variables('acrName'), variables('acrSplit')[8]), '/Microsoft.Authorization/', guid(resourceGroup().id, 'acr'))]",
                            "properties": {
                                "roleDefinitionId": "[concat(subscription().Id, '/providers/Microsoft.Authorization/roleDefinitions/', '7f951dda-4ed3-4680-a7ca-43fe172d538d')]",
                                "principalId": "[parameters('azureClientObjectId')]",
                                "scope": "[if(contains(parameters('acrId'), 'fake'), variables('acrGuid'), parameters('acrId'))]"
                            }
                        }
                    ]
                }
            }
        }
    ]
}
```

The above would create a registry or use an existing one depending on the input. if you pass in "real" ACR resourceId it will grant ACR service principal access to that, if you pass in resourceId containing "fake" anywhere it will create a new ACR and grant AKS access to that. Note: when passing in fake resourceId you still have have to mimic real resourceId, as it will use that value to try and build different things in the template

Happy deploying!