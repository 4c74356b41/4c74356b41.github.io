---
id: 5787
title: How to install AKS with Calico enabled
date: 2019-01-30
author: rootilo
layout: post
guid: http://4c74356b41.com/post5787
permalink: /post5787
categories:
- Azure
- Kubernetes

---

Howdy,

I was eager to try out Calico on AKS before the docs came out, so I used more or less regular way of figuring something out on Azure. REST API reference. [This definition](https://docs.microsoft.com/en-us/rest/api/aks/managedclusters/createorupdate#networkpolicy) clearly mentions you can use `networkPolicy` property as part of the `networkProfile` and set it to Calico, but that doesnt work unless you enable underlying provider feature (AKS creating just times out with all the nodes being in `Not Ready` state):

```
az feature list --query "[?contains(name, 'Container')].{name:name, type:type}" # example to list all features
az feature register --name EnableNetworkPolicy --namespace Microsoft.ContainerService
az provider register -n Microsoft.ContainerService
```

after that, just use REST API\ARM Template to create the cluster (relevant piece included):

```
{
  "location": "location1",
  "properties": {
    "kubernetesVersion": "1.12.4", // has to be 1.12.x, 1.11.x doesnt support calico AFAIK
    "dnsPrefix": "dnsprefix1",
    "agentPoolProfiles": [
      {
        "name": "nodepool1",
        "count": 3,
        "vmSize": "Standard_DS1_v2",
        "osType": "Linux",
        "osDiskSizeGB": 32,
        "maxPods": 110,
        "vnetSubnetID": "[resourceId('Microsoft.Network/virtualNetworks/subnets', 'vnetname', 'subnetname')]" // vnet to use for aks nodes
      }
    ],
    "linuxProfile": {
      "adminUsername": "azureuser",
      "ssh": {
        "publicKeys": [
          {
            "keyData": "keydata"
          }
        ]
      }
    },
    "servicePrincipalProfile": {
      "clientId": "clientid",
      "secret": "secret"
    },
    "enableRBAC": false,
    "networkProfile": {
        "networkPlugin": "azure",
        "networkPolicy": "calico", // set policy here
        "serviceCidr": "xxx", // IP range from which to assign service cluster IPs. It must not overlap with any Subnet IP ranges.
        "dnsServiceIP": "yyy", // IP address assigned to the Kubernetes DNS service. It must be within the Kubernetes service address range specified in serviceCidr.
        "dockerBridgeCidr": "zzz" // IP range assigned to the Docker bridge network. It must not overlap with any Subnet IP ranges or the Kubernetes service address range.
    }
  }
}
```

Unfortunately, helm doesnt seem to work. I suspect this is because `kubectl port-forward` (which helm relies on) doesnt work as well.

More reading:  
1. https://github.com/Azure/AKS/blob/master/previews.md
2. https://docs.microsoft.com/en-us/rest/api/aks/managedclusters/createorupdate#networkpolicy
3. http://4c74356b41.com/post5787

Happy deploying!