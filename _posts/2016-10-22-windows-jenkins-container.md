---
id: 5671
title: Windows Jenkins container
date: 2016-10-22T18:24:34+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post5671
permalink: /post5671
categories:
  - Devops
tags:
  - containers
  - docker
  - jenkins
---
In the jenkins folder you would want jenkins.war, jre and git (well, i figured jenkins is useless without git). 
  
For COPY command to work you would have to invoke docker build from the directory containing jenkins directory.

To build I'm using: 

```
docker build -t win/jenkins
```

```
#dockerfile
FROM microsoft/windowsservercore
COPY jenkins c:/jenkins
CMD powershell set-dnsclientserveraddress -InterfaceIndex (get-netadapter).ifindex -serveraddresses 8.8.8.8; java -jar c:\jenkins\jenkins.war
```

Also, currently my windows docker containers are not getting proper dns resolution, so I had to work around that.

So to run that, I use:

```
docker run -p 8080:8080 -e PATH="%PATH%;c:/jenkins/bin;c:/jenkins/git/bin" win/jenkins powershell set-dnsclientserveraddress -InterfaceIndex (get-netadapter).ifindex -serveraddresses 8.8.8.8; git config --global http.sslVerify false; java -jar c:\jenkins\jenkins.war
```

So I'm aware there's the ENV directive in the dockerfile, but it won't work for me with windows containers, for some reason. Or you could specify full path to java executable in the CMD directive of the dockerfile and you would also have to specify full path to git inside Jenkins in that case. Also, there's a hack to skip certificate verification. So probably not suitable for production use 😉