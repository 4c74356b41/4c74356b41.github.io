---
id: 4321
title: Hotfix для нового портала SCSM
date: 2015-12-11T21:41:15+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post4321
permalink: /post4321
categories:
  - random
tags:
  - Service Manager
---
<a href="https://www.microsoft.com/en-us/download/details.aspx?id=50362" target="_blank">Очень круто</a>.

New features that re included in this release –
  
Nested enumeration lists are now supported inside the Request offering forms
  
Portal now allows you to share and access different objects inside the portal with direct URLs. You can refer individual items inside the portal with following URL formats –
  
Request Offerings:
  
https://[website\_name]/Home/Makeform?BMEID=[bme\_id]
  
Incident type requests:
  
https://[website\_name]/MyRequests/RequestDetails?type=IncidentRequest&id=[incident\_id]
  
Service Request type requests:
  
https://[website\_name]/MyRequests/RequestDetails?type=ServiceRequest&id=[service\_request_id]
  
Manual Activities:
  
https://[website\_name]/MyActivities/ActivityDetails?type=ManualActivity&id=[manual\_activity_id]
  
Review Activities:
  
https://[website\_name]/MyActivities/ActivityDetails?type=ReviewActivity&id=[review\_activity_id]
  
Help Articles:
  
https://[website\_name]/KnowledgeBase/article/[id\_of\_knowledge\_article]

Issues which are fixed in this release–
  
Affected user and Created by user is getting set to the service account
  
Query type form element is not working for the Incident and User classes
  
Request Offering forms are failing to load if a Query type form element is part of the form
  
Username token is not passing values to the mapped field
  
Cancelling request form does not work
  
Text is overlapping for long strings inside the list in the middle pane
  
Related activities inside My Requests always show state as active
  
Filters inside My Requests and My Activities is not working for some languages
  
Announcement is showing “Invalid Date” in Expired Date column for some languages
  
Comments in the request are using incorrect class
  
Required (mandatory) restriction is not working on query type form element
  
Query form element allows multiple selection even when it is configured for single item selection
  
Scroll bar does not work on some lower screen resolutions
  
Double scroll bar appears while browsing Help Articles
  
Some areas of portal are not rendering in Mozilla Firefox web browser
  
My Activities shows 0 instead of removing the notification sticker when no activity is in progress
  
With SSL enabled, the browser regularly prompts the message “Only secure content is displayed” with a button to “Show all content” while browsing the portal
  
“Added by” inside the action logs show domainusername instead of the display name of the user

Some key known issues which are not fixed in this update
  
Un-favorite does not work for Request Offerings
  
Portal does not filter Request Offerings based on the language
  
Query form element with filter criteria depending on selection from another query in same form does not work
  
Multiple query form elements inside same request offering form cannot add same relationship types
  
Action logs do not expand when any request is opened via direct URL

PS – The fixes for these issues will be taken in next update release. We will keep you posted about them.