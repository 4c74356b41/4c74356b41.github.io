---
id: 5779
title: Testing Kubernetes with Azure Files Premium
date: 2018-07-24T23:40:00+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post5779
permalink: /post5779
categories:
  - Azure
  - VSTS
  - Kubernetes
---

Howdy,

I got into limited public preview of [Azure Files premium](https://azure.microsoft.com/en-us/blog/premium-files-pushes-azure-files-limits-by-100x/) just to test it with Kubernetes. Appears its not that straight forward as you would like it to be :)

It doesnt really work yet, unless you prestage the storage account and you have to use PVC size 100gib or more (Azure File premium limitation). Example:

```
kind: StorageClass
apiVersion: storage.k8s.io/v1
metadata:
  name: azure-premium-files-rwx-delete
provisioner: kubernetes.io/azure-file
mountOptions:
  - dir_mode=0777
  - file_mode=0777
  - uid=1000
  - gid=1000
reclaimPolicy: Retain
parameters:
  skuName: Standard_LRS << has to be this for now
  storageAccount: azurefilespremium << prestage this account

---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: azurefile
spec:
  accessModes:
    - ReadWriteMany
  storageClassName: azure-premium-files-rwx-delete
  resources:
    requests:
      storage: 100Gi
```

There is a [PR](https://github.com/kubernetes/kubernetes/pull/69718) (already) to make Azure Files premium work properly.

Happy deploying!