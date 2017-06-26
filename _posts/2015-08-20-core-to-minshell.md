---
id: 2991
title: Core to MinShell
date: 2015-08-20T14:59:04+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post2991
permalink: /post2991
categories:
  - random
tags:
  - Copypaste
  - PowerShell
---
Create a folder to mount a Windows Imaging File (WIM) in with the command mkdir c:\mountdir
  
Determine the index number for Server Datacenter using this command at an elevated command prompt: Dism /get-wiminfo /wimfile:<drive>:\sources\install.wim
  
Mount the WIM file using this command at an elevated command prompt:
  
Dism /mount-wim /WimFile:<drive>:\sources\install.wim /Index:<#\_from\_step_2> /MountDir:c:\mountdir /readonly
  
Then run your PowerShell command - Install-WindowsFeature Server-Gui-Mgmt-Infra –Restart –Source c:\mountdir\windows\winsxs

ps. Просто надоело это искать раз в год 😉