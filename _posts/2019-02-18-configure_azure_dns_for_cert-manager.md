---
id: 5790
title: Configure Azure DNS for Cert-Manager
date: 2019-02-18
author: rootilo
layout: post
guid: http://4c74356b41.com/post5790
permalink: /post5790
categories:
- Azure
- Kubernetes
- Powershell

---

Howdy,

here's all you need to configure Azure DNS for Cert-Manager. This would also help you create a lest priviledge role in Azure.

Make Cert-Manager happy with CAA records on your domain:
```
$caaRecords = New-Object System.Collections.ArrayList
$caaRecords.Add(New-AzureRmDnsRecordConfig -CaaFlag "0" -CaaTag "iodef" -CaaValue "mailto:admin@example.com")
$caaRecords.Add(New-AzureRmDnsRecordConfig -CaaFlag "0" -CaaTag "issue" -CaaValue "letsencrypt.org")
#for wildcard uncomment next line
#$caaRecords.Add(New-AzureRmDnsRecordConfig -CaaFlag "0" -CaaTag "issuewild" -CaaValue "letsencrypt.org")

New-AzureRmDnsRecordSet -Name "@" -RecordType CAA -ZoneName zone.com -ResourceGroupName rgName -Ttl 3600 -DnsRecords $caaRecords
```

Least priviledge role in Azure to manage TXT records:
```
{
    "Name": "DNS TXT Contributor",
    "Id": "",
    "IsCustom": true,
    "Description": "Can manage DNS TXT records only.",
    "Actions": [
        "Microsoft.Network/dnsZones/TXT/*",
        "Microsoft.Network/dnsZones/read"
    ],
    "NotActions": [],
    "AssignableScopes": [
        "scopes_go_here" // I like to put all dns zones in the same rg and allow this role only to that RG and assign that role
    ]
}
```

Azure DNS config for Cert-Manager Cluster Issuer:
```
apiVersion: certmanager.k8s.io/v1alpha1
kind: ClusterIssuer
metadata:
  name: letsencrypt-production
spec:
  acme:
    dns01:
      providers:
      - azuredns:
          clientID: xxx
          clientSecretSecretRef:
            key: CLIENT_SECRET
            name: azuredns-config
          hostedZoneName: dns_zone_name
          resourceGroupName: resource_group_name
          subscriptionID: yyy
          tenantID: zzz
        name: azure
    email: cert@domain.com
    http01: {}
    privateKeySecretRef:
      key: ""
      name: letsencrypt-production
    server: https://acme-v02.api.letsencrypt.org/directory
```

Happy deploying!