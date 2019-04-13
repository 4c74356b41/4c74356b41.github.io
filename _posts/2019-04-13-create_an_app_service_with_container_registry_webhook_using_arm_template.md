---
id: 5792
title: Create an App Service with Container Registry webhook using ARM Template
date: 2019-04-13
author: rootilo
layout: post
guid: http://4c74356b41.com/post5792
permalink: /post5792
categories:
- Azure
- Devops

---

Howdy,

I've needed to create a simple release pipeline for an Azure App Service and didnt want to actually manage\create it in Azure Devops, so I've configured Azure Container Registry webhooks together with Azure App Service and it works quite well.  
Main drawback in this "solution" - Basic SKU only supports 2 webhooks, so you pretty much need Standard SKU.

```json
{
    "$schema": "https://schema.management.azure.com/schemas/2015-01-01/deploymentTemplate.json#",
    "contentVersion": "1.0.0.0",
    "parameters": {
        "webapp-name": {
            "type": "string"
        },
        "registry-name": {
            "type": "string"
        }
    },
    "resources": [
        {
            "apiVersion": "2016-03-01",
            "name": "[parameters('webapp-name')]",
            "type": "Microsoft.Web/sites",
            "location": "[resourceGroup().location]",
            "properties": {
                "name": "[parameters('webapp-name')]",
                "serverFarmId": "[resourceId('Microsoft.Web/serverfarms/', 'hardcoded_you_can_use_parameter')]",
                "siteConfig": {
                    "appCommandLine": "",
                    "linuxFxVersion": "[concat('DOCKER|', parameters('registry-name'), '.azurecr.io/', parameters('webapp-name'), ':latest')]",
                    "appSettings": [],
                    "publishingUsername": "[concat('$', parameters('webapp-name'))]" # not sure this is needed
                }
            }
        },
        {
            "apiVersion": "2016-03-01",
            "name": "[concat(parameters('webapp-name'), '/appsettings')]",
            "type": "Microsoft.Web/sites/config",
            "location": "[resourceGroup().location]",
            "dependsOn": [
                "[parameters('webapp-name')]"
            ],
            "properties": {
                "DOCKER_ENABLE_CI": "true",
                "DOCKER_REGISTRY_SERVER_PASSWORD": "[first(listCredentials(resourceId('container_registry_resource_group', 'Microsoft.ContainerRegistry/registries', parameters('registry-name'), '2017-10-01')).passwords).value]",
                "DOCKER_REGISTRY_SERVER_URL": "[concat('https://', parameters('registry-name'), '.azurecr.io')]",
                "DOCKER_REGISTRY_SERVER_USERNAME": "[parameters('registry-name')]",
                "WEBSITES_ENABLE_APP_SERVICE_STORAGE": "false"
            }
        },
        {
            "type": "Microsoft.Resources/deployments",
            "apiVersion": "2018-05-01",
            "name": "[concat('registryWebhook-', parameters('webapp-name'))]",
            "resourceGroup": "container_registry_resource_group",
            "subscription": "container_registry_subscription",
            "dependsOn": [
                "[resourceId('Microsoft.Web/sites/config', parameters('webapp-name'), 'appsettings')]"
            ],
            "properties": {
                "mode": "Incremental",
                "template": {
                    "$schema": "https://schema.management.azure.com/schemas/2015-01-01/deploymentTemplate.json#",
                    "contentVersion": "1.0.0.0",
                    "resources": [
                        {
                            "apiVersion": "2017-10-01",
                            "name": "[concat(parameters('registry-name'), '/webapp_', parameters('webapp-name'))]",
                            "type": "Microsoft.ContainerRegistry/registries/webhooks",
                            "location": "[resourceGroup().location]", # this might not match with the original resource group location
                            "properties": {
                                "status": "enabled",
                                "scope": "[concat(parameters('webapp-name'), ':latest')]", # container:tag in the container registry, when this particular container + tag combination gets updated - webhook is executed
                                "actions": [
                                    "push"
                                ],
                                "serviceUri": "[concat(list(resourceId('Microsoft.Web/sites/config', parameters('webapp-name'), 'publishingcredentials'), '2015-08-01').properties.scmUri, '/docker/hook')]"
                            }
                        }
                    ]
                }
            }
        }
    ]
}
```

I cannot test this exact template version, but its a copy\paste of what I got working, so the only problem you might have with this - typos.

Happy deploying!