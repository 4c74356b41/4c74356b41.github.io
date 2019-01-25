---
id: 5785
title: How to create AKS with multiple node pools
date: 2019-01-25
author: rootilo
layout: post
guid: http://4c74356b41.com/post5785
permalink: /post5785
categories:
- Azure
- Kubernetes
- Arm Templates

---

Howdy,

recently I got asked how to create AKS cluster with multiple nodetypes. I'm doing this using ARM Templates, you just have to provide proper json array to the AKS definition. You would pass something like that to the `k8sReference` parameter:

Input:
```
{
    "types": [
        {
            "name": "type1"
            "count": "2"
            "worker_size": "Standard_B2s"
        },
        {
            "name": "type2"
            "count": "2"
            "worker_size": "Standard_B2s"
        }
    ]
}
```
Template:
```
"parameters": {
    redacted
    "k8sReference": {
        "type": "object"
    },
},
"resources": [
    {
        "name": "[concat(parameters('deploymentPrefix'), '-k8s')]",
        "apiVersion": "2018-03-31",
        "location": "[resourceGroup().location]",
        "type": "Microsoft.ContainerService/managedClusters",
        "properties": {
            "kubernetesVersion": "[parameters('k8sReference').version]",
            "dnsPrefix": "[concat(parameters('deploymentPrefix'), '-k8s')]",
            "copy": [
                {
                    "name": "agentPoolProfiles",
                    "count": "[length(parameters('k8sReference').types)]",
                    "input": {
                        "name": "[parameters('k8sReference').types[copyIndex('agentPoolProfiles')].name]",
                        "count": "[parameters('k8sReference').types[copyIndex('agentPoolProfiles')].count]",
                        "vmSize": "[parameters('k8sReference').types[copyIndex('agentPoolProfiles')].worker_size]",
                        "osType": "Linux",
                        "osDiskSizeGB": 32,
                        "maxPods": 110,
                        "vnetSubnetID": "[if(contains(parameters('k8sReference').vnetId, 'fake'), resourceId('Microsoft.Network/virtualNetworks/subnets', concat(parameters('deploymentPrefix'), '-k8s-vnet'), 'default'), parameters('k8sReference').vnetId)]"
                    }
                }
            ],
            "linuxProfile": redacted,
            "servicePrincipalProfile": redacted,
            "enableRBAC": true,
            "networkProfile": redacted
        }
    }
]
```

Happy deploying!