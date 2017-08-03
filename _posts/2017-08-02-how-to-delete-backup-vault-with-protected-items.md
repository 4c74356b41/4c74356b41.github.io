---
id: 5773
title: How to delete Azure Backup Vault with Azure SQL Long Term retention databases
date: 2017-08-03T11:40:00+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post5773
permalink: /post5773
categories:
  - Azure
---

I've came across this problem where I had a backup vault I want to delete, but it contains Azure SQL long term backup databases.
And you cannot remove them using the portal. Azure Backup is pretty counter-intuitive so I've decided to convert that knowledge into a post.

**Obviously you will lose all your backups if you do this**. But since I was just tinkering around I needed to do that.

What you have to do is remove the backup items and delete the vault after.

```
# We need to set recovery services context to work with recovery vault
$vault = Get-AzureRmRecoveryServicesVault -Name '{VaultName}'
Set-AzureRmRecoveryServicesVaultContext -Vault $vault
# Get protection containers to work with those
$containers = Get-AzureRmRecoveryServicesBackupContainer -ContainerType AzureSQL -Status Registered
foreach ($container in $containers) {
    $item = Get-AzureRmRecoveryServicesBackupItem -Container $container -WorkloadType AzureSQLDatabase
    # possibly need another iterator here
    Disable-AzureRmRecoveryServicesBackupProtection -Item $item -RemoveRecoveryPoints
    Unregister-AzureRmRecoveryServicesBackupContainer -Container $container
}
```
