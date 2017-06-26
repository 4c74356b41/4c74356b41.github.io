---
id: 5731
title: Azure Disk Encryption + Linux VM = ??
date: 2017-03-12T20:45:22+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post5731
permalink: /post5731
categories:
  - Azure
tags:
  - Azure
  - Backup
  - Encryption
  - Linux
---
Just a quick script to automate creating a linux VM and excrypting it. Requires you to be logged with proper rights (to create all the things and access KeyVault)

```
$appName = 'appName'
$appPwd = '!Q2w3e4r5t6y'
$bogusHttp = 'http://localhost/test'
$location = 'northeurope'

$app = New-AzureRmADApplication -DisplayName $appname -HomePage $bogusHttp -IdentifierUris $bogusHttp -Password $appPwd
New-AzureRmADServicePrincipal -ApplicationId $app.ApplicationId

$rg = New-AzureRmResourceGroup -Name $appName -Location $location
$kv = New-AzureRmKeyVault -VaultName $appName -ResourceGroupName $rg.ResourceGroupName -Location $location -Sku Premium -EnabledForDiskEncryption:$true
#New-AzureRmRecoveryServicesVault -Name $appName -ResourceGroupName $rg.ResourceGroupName -Location $location

Set-AzureRmKeyVaultAccessPolicy -VaultName $kv.VaultName -ResourceGroupName $rg.ResourceGroupName -ServicePrincipalName $app.ApplicationId -PermissionsToKeys wrapKey -PermissionsToSecrets set

$kek = Add-AzureKeyVaultKey -VaultName $kv.VaultName -Name 'kek' -Destination HSM

$aesProvider = New-Object System.Security.Cryptography.AesCryptoServiceProvider
$aesProvider.KeySize = 256
$aesProvider.GenerateKey()
$base64Array = [Convert]::ToBase64String($aesProvider.Key)

$vmParams = @{
    adminUsername  = 'testo'
    adminPassword  = (ConvertTo-SecureString -AsPlainText -Force $appPwd)
    dnsLabelPrefix = 'qscwdvzsexdr'
}

$params = @{
    aadClientId = $app.ApplicationId
    aadClientSecret = (ConvertTo-SecureString -AsPlainText -Force $appPwd)
    VolumeType = 'OS'
    keyEncryptionKeyURL = $kek.key.kid
    keyVaultName = $kv.VaultName
    keyVaultResourceGroup = $kv.VaultName
    passphrase = (ConvertTo-SecureString -AsPlainText -Force $base64Array)
    usekek = 'kek'
    vmname = 'MyUbuntuVM'
}

# this does create a A1 VM, so its no going to work, but I'm using my own template here, just use any way to create a VM with more than 2 cores\4 gb RAM
New-AzureRMResourceGroupDeployment -Name $appName -ResourceGroupName $rg.ResourceGroupName -TemplateUri https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/101-vm-simple-linux/azuredeploy.json @vmParams

New-AzureRmResourceGroupDeployment -Name $appName -ResourceGroupName $rg.ResourceGroupName -TemplateUri https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/201-encrypt-running-linux-vm/azuredeploy.json @params
```

Reference:

https://docs.microsoft.com/en-us/azure/security/azure-security-disk-encryption  
https://github.com/Azure/azure-quickstart-templates/tree/master/201-encrypt-running-linux-vm  
https://blogs.msdn.microsoft.com/cclayton/2017/01/03/creating-a-key-encrypting-key-kek/  
https://blogs.msdn.microsoft.com/cclayton/2016/12/30/self-signed-certificate-creation/  
https://blogs.msdn.microsoft.com/azuresecurity/2015/11/16/explore-azure-disk-encryption-with-azure-powershell/  
https://blogs.msdn.microsoft.com/azuresecurity/2015/11/21/explore-azure-disk-encryption-with-azure-powershell-part-2/