---
id: 5683
title: How to work with ARM Templates without going mad
date: 2017-02-04T21:56:09+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post5683
permalink: /post5683
categories:
  - Azure
  - Azure Stack
tags:
  - Azure
  - Azure Portal
  - Azure Resource Manager
  - Azure Stack
---
ARM Templates are meant for automating deployments, for better understanding of the ARM concepts consult [this document](https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-group-overview). I'm writing this under the assumption that you are interested in writing your own ARM templates and got lost at some point.

Obviously [consult ARM syntax](https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-group-template-functions). And general [ARM guidelines](https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-group-authoring-templates). But this shouldn't be your case. But this document might help you, [design patterns for Azure Resource Manager templates when deploying complex solutions](https://docs.microsoft.com/en-us/azure/azure-resource-manager/best-practices-resource-manager-design-templates).

**Basics. Where do I start?**

Well, if you are not interested in inventing the wheel again, I'd recommend starting by finding some relevant examples on the web.

There are 3 main sources of ARM Templates:

  1. [Github ARM examples repository](https://github.com/Azure/azure-quickstart-templates)
  2. Search engine (thou, seldom this does work)
  3. Your own collection of templates (well&#8230;)

Once you've found something that looks like what you need (or almost looks like that) you can start working on it. If not, try other ways of making your life easier:

  1. ["Automation Script" button on the Azure Portal](https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-manager-export-template#export-the-template-from-resource-group)
  2. [Look through already deployed templates and export them](https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-manager-export-template#view-a-template-from-deployment-history)
  3. [Azure Explorer](https://resources.azure.com)
  4. Azure Automation option

All of these are doing exactly the same, they are giving you a way to export existing resources you have in Azure into ARM Template. So obviously you should have those resources in Azure before you export them, but that is pretty easy to do.

But bear in mind, all of these ways are nowhere near perfect, they cannot export certain things\properties\parameters, so after you've exported a template, read through it (or try deploying) and figure out if something is missing from the template.

Working with Azure Explorer is pretty intuitive, so I won't explain it. It could help you out if you are looking for some specific property that didn't get exported with "Automation Script", also looking at already deployed templates could work when "Automation Script" doesn't.

Azure automation option can be used when you are creating resource in Azure using the portal, when you are about to deploy it, you can notice "Automation option" button near the deploy button.

[<img class="alignnone size-medium wp-image-5726" src="http://4c74356b41.com/wp-content/uploads/2017/02/unnamed-file-2-101x300.png" alt="Azure Automation Options" width="101" height="300" srcset="http://4c74356b41.com/wp-content/uploads/2017/02/unnamed-file-2-101x300.png 101w, http://4c74356b41.com/wp-content/uploads/2017/02/unnamed-file-2.png 311w" sizes="(max-width: 101px) 100vw, 101px" />](http://4c74356b41.com/wp-content/uploads/2017/02/unnamed-file-2.png)

The thing with "Automation option" most of the time it uses a slightly different template to deploy stuff, which can help you.

### How do I fix missing properties?

Option | Should I use it?
--- | ---
<del>[ARM Schemas?](https://github.com/Azure/azure-resource-manager-schemas)</del> | no, just no.  
<del>[Documentation by examples?](https://docs.microsoft.com/en-us/azure/templates)</del> | yes, if it helps.  
[Rest API!](https://docs.microsoft.com/en-us/rest/api/) | always works, a bit cumbersome, but never fails.

ARM Templates have a JSON schema, and that schema is well defined (*take this with a grain of salt and read further*), I've linked the schema definitions repository. You can work your way through the schema to create a Template from scratch, but I doubt any sane person could handle all the humiliation they would have to go through to do that. Luckily, there are ways to ease the pain:

  1. [Visual Studio code](https://code.visualstudio.com) with [Azure Resource Manager Tools](https://marketplace.visualstudio.com/items?itemName=msazurermtools.azurerm-vscode-tools) and [ARM Snippets](https://marketplace.visualstudio.com/items?itemName=artofshell.armsnippet)
  2. [Visual Studio](https://www.visualstudio.com) with [Azure SDK](https://azure.microsoft.com/en-us/downloads/)

Also some usefull hotkeys for VS Code: Alt+Shift+F - format the JSON template, so it looks pretty and easier to read, Ctrl+Shift+M - find errors and show them. If you select the language of the file as JSON, VS Code will offer intellisense when working with ARM Templates (if you've installed extensions). Pretty sure Visual Studio has the same capabilities, I haven't really worked with it a lot.

What is convenient with Visual Studio it allows to navigate between resources in the template (similar to what you can do in the portal). This is pretty useful when you are working with a big template.

[<img class="alignnone size-medium wp-image-5763" src="http://4c74356b41.com/wp-content/uploads/2017/02/Untitled-2-300x136.png" alt="Template Documentation example 6" width="300" height="136" srcset="http://4c74356b41.com/wp-content/uploads/2017/02/Untitled-2-300x136.png 300w, http://4c74356b41.com/wp-content/uploads/2017/02/Untitled-2-768x349.png 768w, http://4c74356b41.com/wp-content/uploads/2017/02/Untitled-2-1024x465.png 1024w" sizes="(max-width: 300px) 100vw, 300px" />](http://4c74356b41.com/wp-content/uploads/2017/02/Untitled-2.png)

More information on both: [VS Code](https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-manager-vs-code) and [Visual Studio](https://docs.microsoft.com/en-us/azure/azure-resource-manager/vs-azure-tools-resource-groups-deployment-projects-create-deploy).

**This section is left only for historical purposes**  
Sometimes, intellisense doesn't help, and to fix that you could consult the schema. Say you want to know, what parameters are there for VM OSProfile, you go to the "[schema master](https://github.com/Azure/azure-resource-manager-schemas/blob/0a7a9768de80ba5e57583f503debd160f4bccfbc/schemas/2015-01-01/deploymentTemplate.json)" and search for the entity you are interested in. Since we want a Virtual Machine property we will look for virtual machine schema under "resources" and there we will find reference schema ("http://schema.management.azure.com/schemas/2015-08-01/Microsoft.Compute.json#/resourceDefinitions/virtualMachines"). You download that schema and look through it to find relevant information, this time its OSProfile (this is where Alt+Shift+F hotkey comes in handy, as those definitions are minimized, so not readable):

```
"osProfile": {
    "properties": {
        "computerName": {
            "type": "string"
        },
        "adminUsername": {
            "type": "string"
        },
        "adminPassword": {
            "type": "string"
        },
        "customData": {
            "type": "string"
        },
        "windowsConfiguration": {
            "$ref": "#/definitions/windowsConfiguration"
        },
        "linuxConfiguration": {
            "$ref": "#/definitions/linuxConfiguration"
        },
        "secrets": {
            "type": "array",
            "items": {
                "$ref": "#/definitions/secret"
            }
        }
    },
    "type": "object",
    "required": [
        "computerName",
        "adminUsername",
        "adminPassword"
    ]
},
```

As you probably noticed, some of those are links to another objects in the schema, they could easily be located with a quick Ctrl+F, unless they link to another schema file, in that case, look in that file.

**This section above is left only for historical purposes**   
Right now your best bet is to use new [Azure Template](https://docs.microsoft.com/en-us/azure/templates) documentation. It offers a more convenient way to achieve the same result you would with ARM Schemas and much faster.

[<img class="alignnone size-medium wp-image-5757" src="http://4c74356b41.com/wp-content/uploads/2017/02/unnamed-file-3-188x300.png" alt="Template Documentation example" width="188" height="300" srcset="http://4c74356b41.com/wp-content/uploads/2017/02/unnamed-file-3-188x300.png 188w, http://4c74356b41.com/wp-content/uploads/2017/02/unnamed-file-3.png 507w" sizes="(max-width: 188px) 100vw, 188px" />](http://4c74356b41.com/wp-content/uploads/2017/02/unnamed-file-3.png)

As you can see, this is an example of a [Key Vault resource Schema](https://docs.microsoft.com/en-us/azure/templates/microsoft.keyvault/vaults), but as you can see this example doesn't offer a way to create a Key Vault secret (**neither does schema at the time of writing**), which basically makes this pretty useless. Why would you need a Key Vault without any entities stored in it? Why would you need to use Powershell or something else to create secrets? Well, it turns out you don't need to do that, you can do that with an ARM Template, [here's an example](https://github.com/Azure/azure-quickstart-templates/blob/master/201-key-vault-secret-create/azuredeploy.json) (ironicly enough this is official Microsoft example):

[<img class="alignnone size-medium wp-image-5758" src="http://4c74356b41.com/wp-content/uploads/2017/02/unnamed-file-4-300x94.png" alt="__" width="300" height="94" srcset="http://4c74356b41.com/wp-content/uploads/2017/02/unnamed-file-4-300x94.png 300w, http://4c74356b41.com/wp-content/uploads/2017/02/unnamed-file-4-768x239.png 768w, http://4c74356b41.com/wp-content/uploads/2017/02/unnamed-file-4.png 927w" sizes="(max-width: 300px) 100vw, 300px" />](http://4c74356b41.com/wp-content/uploads/2017/02/unnamed-file-4.png)

Let's take that one step further, We know that "anything" is possible using Azure REST API. But what if we want to create a secret that is disabled (not that there is a reason for that, but we are just using that as an **example**) or not usable after certain date. Looking at the [REST Api reference](https://docs.microsoft.com/en-us/rest/api/keyvault/setsecret) for creating a Key Vault secret we can notice that there are properties to do that.

[<img class="alignnone size-medium wp-image-5759" src="http://4c74356b41.com/wp-content/uploads/2017/02/unnamed-file-5-211x300.png" alt="Template Documentation example 3" width="211" height="300" srcset="http://4c74356b41.com/wp-content/uploads/2017/02/unnamed-file-5-211x300.png 211w, http://4c74356b41.com/wp-content/uploads/2017/02/unnamed-file-5.png 479w" sizes="(max-width: 211px) 100vw, 211px" />](http://4c74356b41.com/wp-content/uploads/2017/02/unnamed-file-5.png)

Well, lets try adding that to the template:

[<img class="alignnone size-medium wp-image-5761" src="http://4c74356b41.com/wp-content/uploads/2017/02/Untitled-300x136.png" alt="Template Documentation example 4" width="300" height="136" srcset="http://4c74356b41.com/wp-content/uploads/2017/02/Untitled-300x136.png 300w, http://4c74356b41.com/wp-content/uploads/2017/02/Untitled-768x348.png 768w, http://4c74356b41.com/wp-content/uploads/2017/02/Untitled.png 771w" sizes="(max-width: 300px) 100vw, 300px" />](http://4c74356b41.com/wp-content/uploads/2017/02/Untitled.png)

If you test it you will see something like this:

[<img class="alignnone size-medium wp-image-5762" src="http://4c74356b41.com/wp-content/uploads/2017/02/Untitled-1-300x53.png" alt="Template Documentation example 5" width="300" height="53" srcset="http://4c74356b41.com/wp-content/uploads/2017/02/Untitled-1-300x53.png 300w, http://4c74356b41.com/wp-content/uploads/2017/02/Untitled-1-768x137.png 768w, http://4c74356b41.com/wp-content/uploads/2017/02/Untitled-1-1024x183.png 1024w" sizes="(max-width: 300px) 100vw, 300px" />](http://4c74356b41.com/wp-content/uploads/2017/02/Untitled-1.png)

In other words, it worked. Well, that gives us an idea on how to extend ARM Templates despite the fact that neither ARM Schema, nor official ARM Templates documentation list those fields\properties as possible.

## TLDR \ Short Summary

<img src="http://4c74356b41.com/wp-content/uploads/2017/06/armtemplateworkflow.png" />

I recommend using this "workflow" when working with ARM Templates:

  1. Look for existing examples on the web
  2. Export existing resources to create a base template (if you cant find an example, or if you are missing a lot of properties)
  3. Create and export resources if they don't exist yet. Remember that there are at least 4 ways to export resource when\after creating, some of those might not work for your particular case.
  3. Consult <del>the schema</del> REST API\Resource Explorer\Powershell\Azure CLI 2.0 and intellisense (**notice that intellisense CAN BE MISTAKEN**) when working your way through the template, use appropriate free tools, don't make your life harder (all described in this article)
  4. Try deploying your template and [see what the errors are](https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-manager-deployment-operations) and fix them, errors can be obtained in the portal or using powershell\cli (and probably all the sdk's)

### Debug

  1. [Always check for known errors](https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-manager-common-deployment-errors)
  2. [Enable debug mode](https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-manager-common-deployment-errors#troubleshooting-tricks-and-tips)
  3. Sometimes ARM engine will throw something like: "Error at line 1, column 2356", easiest way to handle such an error - [minify your JSON](http://www.httputility.net/json-minifier.aspx) and look for character 2356 in the result.
  4. Use official [MS guidance](https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-manager-common-deployment-errors#troubleshooting-other-services) to troubleshoot ARM deployments

### Hints:

1. Sometimes you have to play with the API version to deploy what you really need. If you template looks right, but the resource in question is throwing weird errors, try changing API versions
2. ARM Functions can be chained, so the output of one function is the input to the next one. `listKeys(resourceId(concat(bla-bla-bla)))`
3. You can use dot notation or `[]` to access object properties. This is important to understand because `variable('x').parameter('y')` doesn't work, whereas `variable('x')[parameter('y')]` does. You can also access array members by their number `[0]`, sadly `[-1]` doesn't work, but there's `last()` function for that.

### Fancy:

[**ArmWiz**](http://old.armviz.io/#/) (and an [old version](http://old.armviz.io/#/)) <del>fancy thing which might help someone someday, I do not see much value in it</del>  
I have to take my words back on this one, this is pretty useful if you are just starting to work with a big template that you didn't put together (or maybe you did but long time ago). So it can be really useful. [Reference](https://blog.kloud.com.au/2017/02/21/a-brief-intro-to-azure-resource-visualiser-armviz-io/).

**Fiddler**  
This tool can be used to capture existing calls from the portal to convert them to ARM Templates, I've used it a couple of times for automating various things. I won't describe how to work with it, as this is not the main point of this article (and there are tons of resources explaining how to do so).

### Minor:

I've heard several times that you cannot use reference to other resource in the template outside of the output section. This is false. You can do that (but you also need to pass in "api-version" to the reference function). <del>The only requirement is that the resource should be deployed after the resource it is referencing, which is quite logical.</del>  
[Reference function](https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-group-template-functions-resource?toc=%2fazure%2ftemplates%2ftoc.json&bc=%2Fazure%2Ftemplates%2Fbreadcrumb%2Ftoc.json#reference) implies dependancy, so no need to declare `dependsOn` if you use `reference`.


> By using the reference function, you implicitly declare that one resource depends on another resource if the referenced resource is provisioned within same template. You do not need to also use the dependsOn property. The function is not evaluated until the referenced resource has completed deployment.


*to be continued...*

Last update - 17.06.2017
