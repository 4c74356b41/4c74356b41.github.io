---
id: 5712
title: Send message to Telegram Channel with Azure Function
date: 2017-02-21T22:42:38+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post5712
permalink: /post5712
categories:
  - Azure
tags:
  - Azure
  - Azure Functions
  - 'C#'
---
Turns out its pretty easy and straight forward:

  1. Create a bot (https://core.telegram.org/bots#6-botfather)
  2. Join it to a chat and get chat id
  3. Send messages 😉

First two are pretty straight forward, I've added the link to the Bot creation tutorial, to get the chat ID after you've added the bot do this: `https://api.telegram.org/bot<YourBOTToken>/getUpdates` and look for the chat object in the resulting JSON, it will have a `node` property, chatid is a negative number.

To work with Bot I've created the following Function using C# (you can use anything you want), this function will take http input and send it to Telegram chat, you can create any trigger you like:

```
using System.Net;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using Newtonsoft.Json;

public static async Task&lt;HttpResponseMessage> Run(HttpRequestMessage req, string arg1, string arg2, string arg3, TraceWriter log)
{
    log.Info("C# HTTP trigger function processed a request.");
    var text = String.Format("arg1: {0}\narg2: {1}\narg3: {2}", arg1, arg2, arg3);
    log.Info(text);

    var results = await SendTelegramMessage(text);
    log.Info(String.Format("{0}", results));

    return req.CreateResponse(HttpStatusCode.OK);
}

public static async Task&lt;string> SendTelegramMessage(string text)
{
    using (var client = new HttpClient())
    {

        Dictionary&lt;string, string> dictionary = new Dictionary&lt;string, string>();
        dictionary.Add("chat_id", "CHATID");
        dictionary.Add("text", text);

        string json = JsonConvert.SerializeObject(dictionary);
        var requestData = new StringContent(json, Encoding.UTF8, "application/json");

        var response = await client.PostAsync(String.Format("https://api.telegram.org/bot224430478:AAGBjzNWDHcu96UG8oPgTMX7f52GU2aD060/sendMessage"), requestData);
        var result = await response.Content.ReadAsStringAsync();

        return result;
    }
}

```

My Config for Function:

```
{
  "bindings": [
    {
      "authLevel": "anonymous",
      "name": "req",
      "type": "httpTrigger",
      "direction": "in",
      "methods": [
        "get"
      ],
      "route": "event/{arg1:maxlength(50)}/{arg2:maxlength(50)}/{arg3:maxlength(50)}/"
    },
    {
      "name": "$return",
      "type": "http",
      "direction": "out"
    }
  ],
  "disabled": false
}
```

You would also need to configure CORS, to allow for requests from your site\source and add projects.json (should be in your function directory, refer: https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference#a-idfileupdatea-how-to-update-function-app-files) to install dependency:

```
{
   "frameworks": {
   "net46":{
      "dependencies": {
          "Newtonsoft.Json": "9.0.1"
      }
   }
  }
}
```