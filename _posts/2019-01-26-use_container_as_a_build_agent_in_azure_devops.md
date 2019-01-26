---
id: 5786
title: Use container as a build agent in Azure Devops
date: 2019-01-26
author: rootilo
layout: post
guid: http://4c74356b41.com/post5786
permalink: /post5786
categories:
- Azure
- Containers
- VSTS

---

Howdy,

when running builds on hosted agents sometimes it lacks little things, sometimes big things. Also, to ensure consistency between development, test and production, its better to use the same container. What I was doing previously:

1. docker pull
2. docker run xxx 

And there is nothing wrong with this, except you need to mount your code to the container and you have to do all the commands in one go or issue several near identical docker run commands which is suboptimal. Turns out Azure Devops can run your pipeline inside the container on the hosted agent, which is really neat. Additionally, all your tasks will run in the root of the repo and all your build variables will be available inside container as is. So you dont need to mount the repo inside container and you dont need to declare variables for the docker run command.  

```
resources:
  containers:
  - container: my_container # can be anything
    image: image_name
    endpoint: endpoint_name

jobs:
  - job: job_name
    container: my_container # has to be the container name from resources
    pool:
      vmImage: 'Ubuntu-16.04'
    steps:
    - checkout: self
      fetchDepth: 1
      clean: true

    - script: do something here
    - script: or here

    - task: PublishTestResults@2
      inputs:
        testResultsFiles: '**/test_*.xml'
        searchFolder: '$(Build.Repository.LocalPath)/pathX'
      condition: always()

    - task: PublishBuildArtifacts@1
      inputs:
        pathtoPublish: '$(Build.Repository.LocalPath)/pathY'
        artifactName: 'drop' 
        publishLocation: 'Container' # this is not related to running inside container
      condition: always()

```

Additional reading:

1. [Container jobs official doc](https://docs.microsoft.com/en-us/azure/devops/pipelines/process/container-phases?view=azdevops&tabs=yaml&viewFallbackFrom=vsts)
2. [Yaml Job schema](https://docs.microsoft.com/en-us/azure/devops/pipelines/yaml-schema?view=azdevops&tabs=schema&viewFallbackFrom=vsts#job)

Happy deploying!