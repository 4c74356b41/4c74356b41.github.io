---
id: 5778
title: Update all kubernetes deployments in vsts release
date: 2018-07-24T23:40:00+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post5778
permalink: /post5778
categories:
  - Azure
  - VSTS
  - Kubernetes
---

Howdy,

I was looking for a way to update various number of kubernetes deployments using a single release step, unfortunately VSTS doesnt allow any scripting in the native kubernetes steps. So I had to hack my way through. You can obviosly tweak this solution to match your needs.

I used the native kubernetes step to get credential to the release agent and than find the config and use it in the script step. I did not make any changes to the kubernetes step, just used proper namespace along with meaningful get command. After that I used this script step to get the job done:

```
config=`find . -name config`

kubectl --kubeconfig $config get -n $(namespaceVariable) deploy --selector=type=$(containerType) -o json | jq '.items[].metadata.name' | xargs -L 1 -i kubectl --kubeconfig $config set -n $(namespaceVariable) image deploy/{} mydockerregistry.azurecr.io/$(containerImage):$(BUILD.BUILDNUMBER) --record=true
```

Also modified script step to start in this location on the agent: `/opt/vsts/work/_temp/kubectlTask`. Let me break down this command in parts, each part is a new line or everything between pipes `|`:

```
all the $() expressions are being evaluated by VSTS before being passed to the agent, so those are just VSTS release variables
config=`find . -name config` # get the config location here and store it as we need to use it two times

kubectl --kubeconfig $config get -n $(namespaceVariable) deploy --selector=type=$(containerType) -o json # get all the deployments that satisfy my criteria of deployment having a label of type equals to some value defined in the build variables; --kubeconfig $config is needed to authenticate kubectl to kubernetes cluster
jq '.items[].metadata.name' # use jq to get only the deployments names frmo the resulting json to pass them to xargs
xargs -L 1 -i kubectl --kubeconfig $config set -n $(namespaceVariable) image deploy/{} mydockerregistry.azurecr.io/containerName:$(BUILD.BUILDNUMBER) --record=true # use xargs to call kubectl set image once for each deployment name and pass in new container image version; --kubeconfig $config is needed to authenticate kubectl to kubernetes cluster
```

resuls looks something like this:
```
2018-07-21T20:23:39.7557121Z kubectl --kubeconfig ./1532204607859/config get -n prod deploy --selector=type=bot -o json | jq '.items[].metadata.name' | xargs -L 1 -i kubectl --kubeconfig ./1532204607859/config set -n prod image deploy/{} ***=&&&.azurecr.io/masked:0.4.0-unstable0010 --record=***
2018-07-21T20:23:39.7826166Z deployment.apps "masked0-prod" image updated
2018-07-21T20:23:39.8090063Z deployment.apps "masked1-prod" image updated
2018-07-21T20:23:39.8358514Z deployment.apps "masked2-prod" image updated
2018-07-21T20:23:39.8616256Z deployment.apps "masked3-prod" image updated
2018-07-21T20:23:39.8869703Z deployment.apps "masked4-prod" image updated
2018-07-21T20:23:39.9132259Z deployment.apps "masked5-prod" image updated
2018-07-21T20:23:39.9405051Z deployment.apps "masked6-prod" image updated
2018-07-21T20:23:39.9687205Z deployment.apps "masked7-prod" image updated
2018-07-21T20:23:39.9948890Z deployment.apps "masked8-prod" image updated
2018-07-21T20:23:40.0208855Z deployment.apps "masked9-prod" image updated
2018-07-21T20:23:40.0465033Z deployment.apps "maskedA-prod" image updated
2018-07-21T20:23:40.0716968Z deployment.apps "maskedB-prod" image updated
```

Happy deploying!