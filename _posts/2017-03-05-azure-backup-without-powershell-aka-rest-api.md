---
id: 5722
title: Azure Backup without Powershell aka REST API
date: 2017-03-05T21:52:45+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post5722
permalink: /post5722
categories:
  - Azure
tags:
  - Azure
  - Backup
  - Python
---
Lets say you wanted to manage Azure Backup programmatically, but you are using Azure Cli, or Cli 2, or Python SDK, well, not Powershell, you only resort would be [Azure Rest API](http://stackoverflow.com/questions/42274160/how-to-manage-azure-backup-with-azure-python-sdk-or-azure-cli/42303540#42303540) (sigh). Well let's use what we can.

Rest Api calls are documented, but pretty poorly.

Lets say you want to delete a VM from protection. Seems easy enough:

```
DELETE
/Subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.RecoveryServices/vaults/{vaultName}/backupFabrics/{fabricName}/protectionContainers/{containerName}/protectedItems/{protectedItemName}?api-version=2016-06-01
```

Well, only several slight nuances. WTH is fabricname? containername?  Notice how it doesn't give any hint at ALL how to construct a proper query. Well, turns out you either have to guess, or get a list of protectable items (if you would want to get a single item you would be facing the same challenge).

Conveniently, a list of Protectable items (https://docs.microsoft.com/en-us/rest/api/recoveryservices/protectableitems) has instructions how to query it (not obvious, but if you scroll down to `filter` you will find those). So after some struggle you come up with this:

```
GET
/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.RecoveryServices/vaults/{vaultName}/backupProtectionContainers?$filter=backupManagementType eq 'AzureIaasVM'?api-version=2016-06-01"
```

I believe those `IaasVMContainer;iaasvmcontainerv2;` and ,code>VM;iaasvmcontainerv2;</code> are constant if you are working with Azure VM's that are added to Azure Backup. Which leads you to this: 

```
DELETE
/Subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.RecoveryServices/vaults/{vaultName}/backupFabrics/Azure/protectionContainers/IaasVMContainer;iaasvmcontainerv2;{resourceGroupName};{vmName}/protectedItems/VM;iaasvmcontainerv2;{resourceGroupName};{vmName}?api-version=2016-12-01
```

You can use armclient (to test) to invoke those (or any other way you like, but arm client seems the most legitimate way for testing). After that it is pretty straight forward. Rough Python SDK code to do that:

```
import requests
from azure.mgmt.resource.resources import ResourceManagementClient
from azure.common.credentials import ServicePrincipalCredentials

credentials = ServicePrincipalCredentials(
    client_id = 'ABCDEFAB-1234-ABCD-1234-ABCDEFABCDEF',
    secret = 'XXXXXXXXXXXXXXXXXXXXXXXX',
    tenant = 'ABCDEFAB-1234-ABCD-1234-ABCDEFABCDEF'
)
access_token = credentials.token['access_token']
vm_ids = [resource.id for resource in arm_client.resource_groups.list_resources(resource_group) if 'Microsoft.Compute' in resource.id]

for vm in vm_ids:
    vm_name = vm.split('/')[-1]
    headers = {"Authorization": 'Bearer ' + access_token}
    backup_Vault_id = 'someName'
    endpoint = 'https://management.azure.com/subscriptions/{sub_id}/resourceGroups/{rg_id}/providers/Microsoft.RecoveryServices/vaults/{vault_id}/backupFabrics/Azure/protectionContainers/IaasVMContainer;iaasvmcontainerv2;{resource_group_name};{vm_name}/protectedItems/VM;iaasvmcontainerv2;{resource_group_name};{vm_name}?api-version=2016-12-01'.format(sub_id=subscription_id, rg_id=resource_group, vault_id=backup_Vault_id, resource_group_name=resource_group, vm_name=vm_name)

    req = requests.delete(endpoint, headers=headers)
    if req.status_code != 202:
        #throw something here
```