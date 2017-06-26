---
id: 5766
title: Azure Functions + Logic Apps + Twitter + Telegram
date: 2017-04-15T21:55:54+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post5766
permalink: /post5766
categories:
  - Azure
tags:
  - Azure
  - Azure Functions
  - Azure Logic Apps
  - Bots
---
I was a bit bored and decided to create this setup 🙂

My function code is hosted on [github](https://github.com/4c74356b41/tryh4rder/tree/master/sharpito). You can use that to setup an Azure Function which can accept calls from a [Telegram bot](http://4c74356b41.com/post5712). You would need to create App Settings to represent you Telegram bot key and Logic Apps key (which you would obtain after creating the app).

After that you would create a Logic App in Azure with the [following definition](https://github.com/4c74356b41/tryh4rder/blob/master/logicapp.definition). You would need to adjust the `xxx` to proper values for your subscription.

Right now this bot works the following way:

You send anything to it (to the bot in telegram) it responds with an inline keyboard and then you press either "MrLlamaSC" or Placeholder. That sends a response to the Function App.

When you push the "MrLlamaSC" button it would send a response, that would get processed by the Azure Functions that would send a request to a Logic App that would send a request back to Azure Function which would send the tweet back to the Bot.

If you go through the code you would easily understand how the function works. I've decided against using the [SDK](https://github.com/MrRoundRobin/telegram.bot) just to illustrate that its possible to do with plain HTTP requests and a bit of Logic Apps magic. I will do a post on Logic Apps a bit down the road.

&nbsp;

[<img class="alignnone size-medium wp-image-5768" src="http://4c74356b41.com/wp-content/uploads/2017/04/Untitled-300x232.png" alt="Bot Picture" width="300" height="232" srcset="http://4c74356b41.com/wp-content/uploads/2017/04/Untitled-300x232.png 300w, http://4c74356b41.com/wp-content/uploads/2017/04/Untitled-768x594.png 768w, http://4c74356b41.com/wp-content/uploads/2017/04/Untitled.png 973w" sizes="(max-width: 300px) 100vw, 300px" />](http://4c74356b41.com/wp-content/uploads/2017/04/Untitled.png)