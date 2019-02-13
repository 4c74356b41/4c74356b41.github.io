---
id: 5789
title: "Azure AKS: SignalR AspNetCore Unable to connect to the remote server ---> System.Net.WebException"
date: 2019-02-13
author: rootilo
layout: post
guid: http://4c74356b41.com/post5789
permalink: /post5789
categories:
- Kubernetes
- Containers
- Azure

---

Howdy,

I've encountered a weird situation recently. Containerized AspNetCore application deployed to AKS was failing to reach SignalR service on Azure. This was previously working on Azure WebApp just fine, some research led me to these github issues:

- https://github.com/aspnet/SignalR/issues/1389
- https://github.com/aspnet/SignalR/issues/1607

and several other topics online. One of these issues mentioned:

```
Also, please note that SignalR requires that all requests from the client go to the same server (often referred to as Load Balancer Affinity), if any request goes to a different server, the client will fail. That could be why your system is working locally but not in the cluster.
```

So it appears you can just set kubernetes service session affinity to ClientIP and it will start working :)

```
"sessionAffinity": "ClientIP"
```

Happy deploying!